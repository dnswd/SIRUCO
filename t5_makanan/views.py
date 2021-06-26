from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from siruco.db import Database
from t1_auth.views import session

##### FITUR 16 #####


def tr_makan_create(request):

    role = session(request, 'peran')
    username = session(request, 'username')
    if role not in ['pengguna_publik', 'admin_satgas']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    if (request.method == 'GET'):
        resIdHotel = None
        if (role == 'admin_satgas'):
            resIdHotel = db.query(
                "SELECT idtransaksi FROM TRANSAKSI_HOTEL")
        else:
            resIdHotel = db.query(f'''
            SELECT idtransaksi
            FROM TRANSAKSI_HOTEL TH JOIN
            TRANSAKSI_BOOKING TB ON TB.idtransaksibooking = TH.idtransaksi JOIN
            RESERVASI_HOTEL RH ON RH.kodepasien = TB.kodepasien JOIN
            PASIEN P ON P.nik = RH.kodepasien
            WHERE P.idpendaftar = '{username}'
            ''')

        resIdMakan = db.query('''
        SELECT idtransaksimakan 
        FROM TRANSAKSI_MAKAN
        WHERE idtransaksimakan LIKE 'TRM%'
        ORDER BY idtransaksimakan DESC
        ''')

        noUrut = '001'
        found = False
        idx = 0
        while (not found) and (idx < len(resIdMakan)):
            try:
                noUrut = str(int(resIdMakan[idx][0][3:]) + 1).zfill(3)
                found = True
            except ValueError:
                idx += 1

        response = {
            "result": {"idhotel": [id[0] for id in resIdHotel],
                       "idmakan": 'TRM' + noUrut},
            "role": role
        }
        db.close()
        return render(request, 'tr-makan-create.html', response)

    else:

        idHotel = request.POST.get('id_h')
        idTM = request.POST.get('id_tm')
        kode = request.POST.get('kodeHotel')
        paket = [request.POST.get(v)
                 for v in request.POST.keys()
                 if v.startswith('paket')]

        db.query(f'''
        INSERT INTO TRANSAKSI_MAKAN VALUES
        ('{idHotel}', '{idTM}', {0})
        ''')
        ins = 'INSERT INTO DAFTAR_PESAN VALUES '
        seq = 1
        for p in paket:
            ins += f"('{idHotel}', '{idTM}', '{kode}', '{p}', {seq}), "
            seq += 1
        ins = ins[:-2]
        db.query(ins)

        db.close()
        return HttpResponseRedirect('/makanan-hotel/#tr-makan')


def getKode(request, id_t):
    db = Database(schema='siruco')
    resKodeHotel = db.query(f'''
    SELECT kodehotel
    FROM TRANSAKSI_HOTEL TH JOIN
    TRANSAKSI_BOOKING TB ON TB.idtransaksibooking = TH.idtransaksi JOIN
    RESERVASI_HOTEL RH ON RH.kodepasien = TB.kodepasien
    WHERE TH.idtransaksi = '{id_t}'
    ''')

    resKodePaket = db.query(f'''
    SELECT kodepaket
    FROM PAKET_MAKAN PM
    WHERE PM.kodehotel = '{resKodeHotel[0][0]}'
    ''')

    response = {
        "kodehotel": resKodeHotel[0][0],
        "kodepaket": [kp[0] for kp in resKodePaket]
    }
    db.close()
    return JsonResponse(response)


def tr_makan_detail(request, id_t, id_tm):

    role = session(request, 'peran')
    if role not in ['pengguna_publik', 'admin_satgas']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    resDetail = db.query(f'''
    SELECT * 
    FROM TRANSAKSI_MAKAN 
    WHERE (idtransaksi='{id_t}' AND idtransaksimakan='{id_tm}')
    ''')

    resKodeHotel = db.query(f'''
    SELECT kodehotel
    FROM TRANSAKSI_HOTEL TH JOIN
    TRANSAKSI_BOOKING TB ON TB.idtransaksibooking = TH.idtransaksi JOIN
    RESERVASI_HOTEL RH ON RH.kodepasien = TB.kodepasien
    WHERE TH.idtransaksi='{id_t}'
    ''')

    resDaftarPesan = db.query(f'''
    SELECT id_pesanan, kodepaket, harga
    FROM DAFTAR_PESAN DP NATURAL JOIN PAKET_MAKAN PM
    WHERE (id_transaksi='{id_t}' AND idtransaksimakan='{id_tm}')
    ''')

    response = {
        "result": {"idtransaksi": resDetail[0][0],
                   "idtransaksimakan": resDetail[0][1],
                   "totalbayar": resDetail[0][2],
                   "kodehotel": resKodeHotel[0][0],
                   "daftarpesan": [{"idpesanan": dp[0],
                                    "kodepaket": dp[1],
                                    "harga": dp[2]}
                                   for dp in resDaftarPesan]},
        "role": role
    }
    db.close()
    return render(request, 'tr-makan-detail.html', response)


def tr_makan_update(request, id_t, id_tm):

    role = session(request, 'peran')
    if role not in ['admin_satgas']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    if (request.method == 'GET'):

        resKodeHotel = db.query(f'''
        SELECT kodehotel
        FROM TRANSAKSI_HOTEL TH JOIN
        TRANSAKSI_BOOKING TB ON TB.idtransaksibooking = TH.idtransaksi JOIN
        RESERVASI_HOTEL RH ON RH.kodepasien = TB.kodepasien
        WHERE TH.idtransaksi = '{id_t}'
        ''')

        resPaketS = db.query(f'''
        SELECT kodepaket
        FROM TRANSAKSI_MAKAN TM JOIN
        DAFTAR_PESAN DP ON (TM.idtransaksi = DP.id_transaksi AND TM.idtransaksimakan = DP.idtransaksimakan)
        WHERE (TM.idtransaksi = '{id_t}' AND TM.idtransaksimakan = '{id_tm}')
        ''')

        resPaketT = db.query(f'''
        SELECT kodepaket
        FROM PAKET_MAKAN PM
        WHERE PM.kodehotel = '{resKodeHotel[0][0]}'
        ''')

        response = {
            "result": {"idhotel": id_t,
                       "idmakan": id_tm,
                       "kodehotel": resKodeHotel[0][0],
                       "paketS": [rs[0] for rs in resPaketS],
                       "paketT": [rt[0] for rt in resPaketT]},
            "role": role
        }
        db.close()
        return render(request, 'tr-makan-update.html', response)
    else:
        idHotel = request.POST.get('id_h')
        idTM = request.POST.get('id_tm')
        kode = request.POST.get('kodeHotel')
        paket = [request.POST.get(v)
                 for v in request.POST.keys()
                 if v.startswith('paket')]

        seq = db.query(f'''
        SELECT id_pesanan
        FROM DAFTAR_PESAN
        WHERE (id_transaksi = '{idHotel}' AND idtransaksimakan = '{idTM}')
        ORDER BY id_pesanan DESC
        LIMIT 1
        ''')[0][0] + 1

        ins = 'INSERT INTO DAFTAR_PESAN VALUES '
        for p in paket:
            ins += f"('{idHotel}', '{idTM}', '{kode}', '{p}', {seq}), "
            seq += 1
        ins = ins[:-2]
        db.query(ins)
        db.close()
        return HttpResponseRedirect('/makanan-hotel/#tr-makan')


def tr_makan_delete(request, id_t, id_tm):

    role = session(request, 'peran')
    username = session(request, 'username')
    if role not in ['admin_satgas']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    red = db.query(f'''
    SELECT totalbayar
    FROM TRANSAKSI_MAKAN
    WHERE (idtransaksi = '{id_t}' AND idtransaksimakan = '{id_tm}')
    ''')[0][0]

    db.query(f'''
    DELETE FROM TRANSAKSI_MAKAN
    WHERE (idtransaksi = '{id_t}' AND idtransaksimakan = '{id_tm}')
    ''')

    db.query(f'''
    DELETE FROM DAFTAR_PESAN
    WHERE (id_transaksi = '{id_t}' AND idtransaksimakan = '{id_tm}')
    ''')

    db.query(f'''
    UPDATE TRANSAKSI_HOTEL
    SET totalbayar = totalbayar - {red}
    WHERE idtransaksi = '{id_t}'
    ''')

    db.close()
    return HttpResponseRedirect('/makanan-hotel/#tr-makan')

##### FITUR 17 #####


def pm_create(request):

    role = session(request, 'peran')
    if role not in ['admin_sistem']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    if (request.method == 'GET'):

        resKodeHotel = db.query("SELECT kode FROM HOTEL")
        response = {
            "result": [kode[0] for kode in resKodeHotel],
            "role": role
        }
        db.close()
        return render(request, 'pm-create.html', response)

    else:

        kodeH = request.POST.get('kodeH')
        kodeP = request.POST.get('kodeP')
        namaP = request.POST.get('namaP')
        harga = request.POST.get('harga')

        db.query(f'''
        INSERT INTO PAKET_MAKAN VALUES 
        ('{kodeH}', '{kodeP}', '{namaP}', {harga})
        ''')

        db.close()
        return HttpResponseRedirect('/makanan-hotel/#paket-makan')


def pm_update(request, kh, kp):

    role = session(request, 'peran')
    if role not in ['admin_sistem']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    if (request.method == 'GET'):
        result = db.query(f'''
        SELECT kodehotel, kodepaket
        FROM PAKET_MAKAN
        WHERE (kodehotel = '{kh}' AND kodepaket = '{kp}') 
        ''')

        response = {
            "result": {"kodehotel": result[0][0],
                       "kodepaket": result[0][1]},
            "role": role
        }
        db.close()
        return render(request, 'pm-update.html', response)

    else:

        namaPaket = request.POST.get('namaP')
        harga = request.POST.get('harga')

        result = db.query(f'''
        UPDATE PAKET_MAKAN
        SET nama = '{namaPaket}',
            harga = {harga}
        WHERE (kodehotel = '{kh}' AND kodepaket = '{kp}')
        ''')

        db.close()
        return HttpResponseRedirect('/makanan-hotel/#paket-makan')


def pm_delete(request, kh, kp):

    role = session(request, 'peran')
    if role not in ['admin_sistem']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    db.query(f'''
    DELETE FROM PAKET_MAKAN
    WHERE (kodehotel = '{kh}' AND kodepaket = '{kp}')
    ''')

    db.close()
    return HttpResponseRedirect('/makanan-hotel/#paket-makan')


##### FITUR 18 #####


def hotel_create(request):

    role = session(request, 'peran')
    if role not in ['admin_sistem']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    if (request.method == 'GET'):

        resKode = db.query('''
        SELECT kode
        FROM HOTEL
        WHERE kode LIKE 'H%'
        ORDER BY kode DESC
        ''')

        noUrut = '01'
        found = False
        idx = 0
        if (resKode != None):
            while (not found) and (idx < len(resKode)):
                try:
                    noUrut = str(int(resKode[idx][0][1:]) + 1).zfill(2)
                    found = True
                except ValueError:
                    idx += 1

        response = {
            "kodehotel": "H" + noUrut
        }

        db.close()
        return render(request, 'hotel-create.html', response)
    else:

        kode = request.POST.get('kode')
        nama = request.POST.get('nama')
        rujuk = 0 if request.POST.get('rujukan') == None else 1
        jalan = request.POST.get('jalan')
        kelurahan = request.POST.get('kelurahan')
        kecamatan = request.POST.get('kecamatan')
        kabkota = request.POST.get('kabkot')
        provinsi = request.POST.get('provinsi')

        db.query(f'''
        INSERT INTO HOTEL VALUES 
        ('{kode}', '{nama}', '{rujuk}', '{jalan}', '{kelurahan}', '{kecamatan}', '{kabkota}', '{provinsi}')
        ''')

        db.close()
        return HttpResponseRedirect('/makanan-hotel/#hotel')


def hotel_update(request, kode):

    role = session(request, 'peran')
    if role not in ['admin_sistem']:
        return HttpResponseRedirect('/')

    db = Database(schema='siruco')
    if (request.method == 'GET'):

        hotel = db.query(f'''
        SELECT *
        FROM HOTEL
        WHERE kode = '{kode}'
        ''')

        response = {
            "kode": kode,
            "nama": hotel[0][1],
            "rujukan": hotel[0][2],
            "jalan": hotel[0][3],
            "kelurahan": hotel[0][4],
            "kecamatan": hotel[0][5],
            "kabkot": hotel[0][6],
            "provinsi": hotel[0][7]
        }

        db.close()
        return render(request, "hotel-update.html", response)

    else:

        kode = request.POST.get('kode')
        nama = request.POST.get('nama')
        rujuk = 0 if request.POST.get('rujukan') == None else 1
        jalan = request.POST.get('jalan')
        kelurahan = request.POST.get('kelurahan')
        kecamatan = request.POST.get('kecamatan')
        kabkota = request.POST.get('kabkot')
        provinsi = request.POST.get('provinsi')

        result = db.query(f'''
        UPDATE HOTEL
        SET nama = '{nama}',
            isrujukan = '{rujuk}',
            jalan = '{jalan}',
            kelurahan = '{kelurahan}',
            kecamatan = '{kecamatan}',
            kabkot = '{kabkota}',
            prov = '{provinsi}'
        WHERE kode = '{kode}'
        ''')

        db.close()
        return HttpResponseRedirect('/makanan-hotel/#hotel')


def makanan_index(request):

    role = session(request, 'peran')
    username = session(request, 'username')

    db = Database(schema='siruco')
    response = {"role": role}

    resultTM = []
    if (role == 'admin_satgas'):
        resultTM = db.query('''
        SELECT TM.idtransaksi, TM.idtransaksimakan, TM.totalbayar, TH.statusbayar 
        FROM TRANSAKSI_MAKAN TM JOIN
        TRANSAKSI_HOTEL TH ON TM.idtransaksi = TH.idtransaksi
        ''')
    elif (role == 'pengguna_publik'):
        resultTM = db.query(f'''
        SELECT TM.idtransaksi, TM.idtransaksimakan, TM.totalbayar, TH.statusbayar 
        FROM TRANSAKSI_MAKAN TM JOIN
        TRANSAKSI_HOTEL TH ON TM.idtransaksi = TH.idtransaksi JOIN
        TRANSAKSI_BOOKING TB ON TB.idtransaksibooking = TH.idtransaksi JOIN
        RESERVASI_HOTEL RH ON RH.kodepasien = TB.kodepasien JOIN
        PASIEN P ON P.nik = RH.kodepasien
        WHERE P.idpendaftar = '{username}'
        ''')

    response["resultTM"] = [{"idtransaksi": tm[0],
                             "idtransaksimakan": tm[1],
                             "totalbayar": tm[2],
                             "status": tm[3]}
                            for tm in resultTM]

    resultPM = []
    if role in ['admin_sistem', 'pengguna_publik', 'admin_satgas', 'admin_sistem']:
        resultPM = db.query("SELECT * FROM PAKET_MAKAN")

    response["resultPM"] = [{"kodeHotel": r[0],
                             "kodePaket": r[1],
                             "namaPaket": r[2],
                             "harga": r[3]}
                            for r in resultPM]

    resultH = []
    if role in ['admin_sistem', 'pengguna_publik', 'admin_satgas', 'admin_sistem']:
        resultH = db.query("SELECT * FROM HOTEL")

    response["resultH"] = [{"kode": h[0],
                            "nama": h[1],
                            "rujukan": h[2],
                            "alamat": ", ".join(h[3:])}
                           for h in resultH]

    db.close()
    return render(request, "makanan_index.html", response)
