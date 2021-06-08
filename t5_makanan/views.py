from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from siruco.db import Database
import json


def tr_makan(request):
    response = render(request)
    database = Database(schema='siruco')
    result = database.query('''
    SELECT TM.idtransaksi, TM.idtransaksimakan, TM.totalbayar, TH.statusbayar 
    FROM TRANSAKSI_MAKAN TM JOIN
    TRANSAKSI_HOTEL TH ON TM.idtransaksi = TH.idtransaksi
    ''')

    role = response.get_cookie('peran')
    content = {
        "result": [{"idtransaksi": result[v][0],
                    "idtransaksimakan": result[v][1],
                    "totalbayar": result[v][2],
                    "status": result[v][3]}
                   for v in range(len(result))],
        "role": role
    }
    database.close()
    return render(request, 'tr-makan.html', content)


def tr_makan_create(request):
    response = render(request)
    database = Database(schema='siruco')
    resIdHotel = database.query("SELECT idtransaksi FROM TRANSAKSI_HOTEL")
    resIdMakan = database.query('''
    SELECT idtransaksimakan 
    FROM TRANSAKSI_MAKAN
    WHERE idtransaksimakan LIKE 'TRM%'
    ORDER BY idtransaksimakan DESC
    LIMIT 1
    ''')
    noUrut = '001'
    if (len(resIdMakan) > 0):
        noUrut = str(int(resIdMakan[0][0][3:]) + 1).zfill(3)

    role = response.get_cookie('peran')
    content = {
        "result": {"idhotel": [resIdHotel[v][0] for v in range(len(resIdHotel))],
                   "idmakan": 'TRM' + noUrut},
        "role": role
    }
    database.close()
    return render(request, 'tr-makan-create.html', content)


def getKodeHotel(request, id_t):
    response = render(request)
    database = Database(schema='siruco')
    resKodeHotel = database.query('''
    SELECT kodehotel
    FROM TRANSAKSI_HOTEL TH JOIN
    TRANSAKSI_BOOKING TB ON TB.idtransaksibooking = TH.idtransaksi JOIN
    RESERVASI_HOTEL RH ON RH.kodepasien = TB.kodepasien
    WHERE TH.idtransaksi = '{}'
    '''.format(id_t))

    content = {
        "kodehotel": resKodeHotel[0][0]
    }
    database.close()
    return JsonResponse(content)


def getKodePaket(request, kode):
    database = Database(schema='siruco')
    resKodePaket = database.query('''
    SELECT kodepaket
    FROM PAKET_MAKAN PM
    WHERE PM.kodehotel = '{}'
    '''.format(kode))

    content = {
        "data": [resKodePaket[v][0] for v in range(len(resKodePaket))]
    }
    database.close()
    return JsonResponse(content)


def save_tr_makan(request):
    result = dict(request.POST)
    result.pop('csrfmiddlewaretoken')
    idHotel = result.pop('id_h')[0]
    idTM = result.pop('id_tm')[0]
    kode = result.pop('kodeHotel')[0]
    paket = [v[0] for v in result.values()]

    database = Database(schema='siruco')
    database.query('''
    INSERT INTO TRANSAKSI_MAKAN VALUES
    ('{}', '{}', {})
    '''.format(idHotel, idTM, 0))
    ins = 'INSERT INTO DAFTAR_PESAN VALUES '
    seq = 1
    for p in paket:
        ins += "('{}', '{}', '{}', '{}', {}), ".format(idHotel,
                                                       idTM, kode, p, seq)
        seq += 1
    ins = ins[:-2]
    database.query(ins)

    database.close()
    return HttpResponseRedirect('/makanan/tr-makan')


def tr_makan_detail(request, id_t, id_tm):
    response = render(request)
    database = Database(schema='siruco')
    resDetail = database.query('''
    SELECT * 
    FROM TRANSAKSI_MAKAN 
    WHERE (idtransaksi='{}' AND idtransaksimakan='{}')
    '''.format(id_t, id_tm))
    resKodeHotel = database.query('''
    SELECT kodehotel
    FROM TRANSAKSI_HOTEL TH JOIN
    TRANSAKSI_BOOKING TB ON TB.idtransaksibooking = TH.idtransaksi JOIN
    RESERVASI_HOTEL RH ON RH.kodepasien = TB.kodepasien
    WHERE TH.idtransaksi='{}'
    '''.format(id_t))
    resDaftarPesan = database.query('''
    SELECT id_pesanan, kodepaket, harga
    FROM DAFTAR_PESAN DP NATURAL JOIN PAKET_MAKAN PM
    WHERE (id_transaksi='{}' AND idtransaksimakan='{}')
    '''.format(id_t, id_tm))

    role = response.get_cookie('peran')
    content = {
        "result": {"idtransaksi": resDetail[0][0],
                   "idtransaksimakan": resDetail[0][1],
                   "totalbayar": resDetail[0][2],
                   "kodehotel": resKodeHotel[0][0],
                   "daftarpesan": [{"idpesanan": resDaftarPesan[v][0],
                                   "kodepaket": resDaftarPesan[v][1],
                                    "harga": resDaftarPesan[v][2]}
                                   for v in range(len(resDaftarPesan))]},
        "role": role
    }
    database.close()
    return render(request, 'tr-makan-detail.html', content)


def tr_makan_update(request, id_t, id_tm):
    response = render(request)
    database = Database(schema='siruco')
    resKodeHotel = database.query('''
    SELECT kodehotel
    FROM TRANSAKSI_HOTEL TH JOIN
    TRANSAKSI_BOOKING TB ON TB.idtransaksibooking = TH.idtransaksi JOIN
    RESERVASI_HOTEL RH ON RH.kodepasien = TB.kodepasien
    WHERE TH.idtransaksi = '{}'
    '''.format(id_t))
    resPaketS = database.query('''
    SELECT kodepaket
    FROM TRANSAKSI_MAKAN TM JOIN
    DAFTAR_PESAN DP ON (TM.idtransaksi = DP.id_transaksi AND TM.idtransaksimakan = DP.idtransaksimakan)
    WHERE (TM.idtransaksi = '{}' AND TM.idtransaksimakan = '{}')
    '''.format(id_t, id_tm))
    resPaketT = database.query('''
    SELECT kodepaket
    FROM PAKET_MAKAN PM
    WHERE PM.kodehotel = '{}'
    '''.format(resKodeHotel[0][0]))

    role = response.get_cookie('peran')
    content = {
        "result": {"idhotel": id_t,
                   "idmakan": id_tm,
                   "kodehotel": resKodeHotel[0][0],
                   "paketS": [resPaketS[v][0] for v in range(len(resPaketS))],
                   "paketT": [resPaketT[v][0] for v in range(len(resPaketT))]},
        "role": role
    }
    database.close()
    return render(request, 'tr-makan-update.html', content)


def update_tr_makan(request):
    result = dict(request.POST)
    result.pop('csrfmiddlewaretoken')
    idHotel = result.pop('id_h')[0]
    idTM = result.pop('id_tm')[0]
    kode = result.pop('kodeHotel')[0]
    paket = [v[0] for v in result.values()]

    database = Database(schema='siruco')
    seq = database.query('''
    SELECT id_pesanan
    FROM DAFTAR_PESAN
    WHERE (id_transaksi = '{}' AND idtransaksimakan = '{}')
    ORDER BY id_pesanan DESC
    LIMIT 1
    '''.format(idHotel, idTM))[0][0] + 1
    ins = 'INSERT INTO DAFTAR_PESAN VALUES '
    for p in paket:
        ins += "('{}', '{}', '{}', '{}', {}), ".format(idHotel,
                                                       idTM, kode, p, seq)
        seq += 1
    ins = ins[:-2]
    database.query(ins)
    database.close()
    return HttpResponseRedirect('/makanan/tr-makan')


def tr_makan_delete(request, id_t, id_tm):
    database = Database(schema='siruco')
    red = database.query('''
    SELECT totalbayar
    FROM TRANSAKSI_MAKAN
    WHERE (idtransaksi = '{}' AND idtransaksimakan = '{}')
    '''.format(id_t, id_tm))[0][0]
    database.query('''
    DELETE 
    FROM TRANSAKSI_MAKAN
    WHERE (idtransaksi = '{}' AND idtransaksimakan = '{}')
    '''.format(id_t, id_tm))
    database.query('''
    DELETE
    FROM DAFTAR_PESAN
    WHERE (id_transaksi = '{}' AND idtransaksimakan = '{}')
    '''.format(id_t, id_tm))
    database.query('''
    UPDATE TRANSAKSI_HOTEL
    SET totalbayar = totalbayar - {}
    WHERE idtransaksi = '{}'
    '''.format(red, id_t))

    database.close()
    return HttpResponseRedirect('/makanan/tr-makan')
