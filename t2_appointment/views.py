from django.http import JsonResponse
from django.shortcuts import render,redirect
from siruco.db import Database

# Create your views here.

def create_jadwal(request):
    db = Database(schema='siruco')
    data = {}

    role = request.session.get('peran')
    if(role != 'admin_dokter'):
        return redirect("/")

    if(request.method == 'GET'):
        list_jadwal = db.query(f'''
                                SELECT *
                                FROM JADWAL
                                WHERE (kode_faskes, shift, tanggal)
                                NOT IN (SELECT kode_faskes, shift, tanggal
                                FROM JADWAL_DOKTER);
                                ''')
        list_jadwal = [{
        "no" : list_jadwal.index(v) + 1,
        "kode_faskes" : v[0],
        "shift" : v[1],
        "tanggal" : v[2]
        } for v in list_jadwal]
        data = {
            "jadwal" : list_jadwal
        }
        db.close()

    elif(request.method == 'POST'):
        username = request.session.get('username')
        faskes = request.POST.get('faskes')
        shift = request.POST.get('shift')
        tanggal = request.POST.get('tanggal')
        no_str = db.query(f'''
                            SELECT D.no_str
                            FROM DOKTER D, ADMIN A, AKUN_PENGGUNA AP
                            WHERE AP.username = '{username}'
                            AND A.username = AP.username
                            AND D.username = A.username;
                            ''')
        db.query("""
            INSERT INTO JADWAL_DOKTER
            VALUES('%s','%s','%s','%s','%s',0);
        """ % (no_str, username, faskes, shift, tanggal))
        db.close()
        return redirect('/appointment/jadwal')

    return render(request, "create-jadwal.html", data)

def read_jadwal(request):
    db = Database(schema='siruco')
    username = request.session.get('username')
    role = request.session.get('peran')
    query = ''
    if(role == 'admin_dokter'):
        query = "SELECT * FROM JADWAL_DOKTER WHERE username = '" + username + "';"
    else:
        query = "SELECT * FROM JADWAL_DOKTER;"
    list_jadwal = db.query(query)
    list_jadwal = [{
        "no" : list_jadwal.index(v)+1,
        "no_str" : v[0],
        "dokter" : v[1],
        "faskes" : v[2],
        "shift" : v[3],
        "tanggal" : v[4],
        "jml_pasien" : v[5]
    } for v in list_jadwal]
    data = {
        "jadwal" : list_jadwal
    }
    db.close()

    return render(request, 'read-jadwal.html', data)

def create_appointment(request):
    db = Database(schema='siruco')
    
    role = request.session.get('peran')
    if(role == 'admin_dokter'):
        return redirect("/")

    list_jadwal = db.query("SELECT * FROM JADWAL_DOKTER;")

    list_jadwal = [{
        "no" : list_jadwal.index(v)+1,
        "no_str" : v[0],
        "dokter" : v[1],
        "faskes" : v[2],
        "shift" : v[3],
        "tanggal" : v[4]
    } for v in list_jadwal]
    data = {
        "jadwal" : list_jadwal
    }
    db.close()

    return render(request, 'create-appointment.html', data)

def form_appointment(request, email, faskes, tanggal, shift):
    db = Database(schema='siruco')
    list_nik_pasien = []
    username = request.session.get('username')
    role = request.session.get('peran')

    if(role == 'admin_dokter'):
        return redirect("/")
    elif(role == 'pengguna_publik'):
        list_nik_pasien = db.query(f"SELECT NIK FROM PASIEN WHERE IdPendaftar = '{username}';")
    else:
        # admin satgas
        list_nik_pasien = db.query('SELECT NIK FROM PASIEN;')
    

    list_nik_pasien = [{
        "nik" : v[0]
    } for v in list_nik_pasien]

    data = {
        "list_nik" : list_nik_pasien,
        "email" : email,
        "faskes" : faskes,
        "tanggal" : tanggal,
        "shift" : shift
    }

    if(request.method == 'POST'):
        # todo : cek trigger >= 30 pasien
        nik = request.POST.get('nik')
        db.query("""
            INSERT INTO MEMERIKSA VALUES
            ('%s','%s','%s','%s','%s',NULL);
        """ % (nik, email, faskes, tanggal, shift))
        return redirect('/appointment/read-appointment')

    db.close()
    return render(request, 'form-appointment.html', data)

def read_appointment(request):
    db = Database(schema='siruco')
    username = request.session.get('username')
    role = request.session.get('peran')

    list_appointment = []
    if(role == 'pengguna_publik'):
        list_appointment = db.query(f"""
            SELECT * FROM MEMERIKSA LEFT JOIN 
            (SELECT NIK, IdPendaftar FROM PASIEN) as P ON NIK_Pasien = NIK
            WHERE idPendaftar = '{username}';
        """)
    elif(role == 'admin_dokter'):
        list_appointment = db.query(f"""
            SELECT * FROM MEMERIKSA
            WHERE Username_Dokter = '{username}';
        """)
    else:
        list_appointment = db.query('SELECT * FROM MEMERIKSA;')

    list_appointment = [{
        "no" : list_appointment.index(v)+1,
        "nik" : v[0],
        "no_str" : v[1],
        "dokter" : v[2],
        "faskes" : v[3],
        "shift" : v[4],
        "tanggal" : v[5],
        "rekomendasi" : v[6] if v[6] != None else "-"
    } for v in list_appointment]

    data = {
        "list_appointment" : list_appointment,
        "role" : role
    }
    db.close()
    return render(request, 'read-appointment.html', data)

def update_appointment(request, nik, email, shift, tanggal, faskes):
    db = Database(schema='siruco')
    
    # usenamenya dokter itu email, isi attr Username_Dokter = email

    rekomendasi = db.query(f"""
        SELECT rekomendasi FROM MEMERIKSA
        WHERE NIK_Pasien = '{nik}'
        AND Username_Dokter = '{email}'
        AND Kode_Faskes = '{faskes}'
        AND Praktek_shift = '{shift}'
        AND Praktek_tgl = '{tanggal}';
    """)
    rekomendasi = [{
        "r" : v[0] if v[0] != None else ""
    } for v in rekomendasi]
    rekomendasi = rekomendasi[0].get("r")

    data = {
        'nik' : nik,
        'email' : email,
        'shift' : shift,
        'tanggal' : tanggal,
        'faskes' : faskes,
        'rekomendasi' : rekomendasi
    }

    if(request.method == 'POST'):       
        rekomendasi = request.POST.get('rekomendasi')
        db.query(f"""
            UPDATE MEMERIKSA
            SET rekomendasi = '{rekomendasi}'
            WHERE NIK_Pasien = '{nik}' AND Username_Dokter = '{email}'
            AND Kode_Faskes = '{faskes}' AND Praktek_shift = '{shift}'
            AND Praktek_tgl = '{tanggal}';
        """)
        return redirect('/appointment/read-appointment')

    db.close()
    return render(request, 'update-appointment.html', data)

def delete_appointment(request, nik, email, faskes, shift, tanggal):
    db = Database(schema='siruco')
    db.query(f"""
        DELETE FROM MEMERIKSA
        WHERE NIK_Pasien = '{nik}' AND Username_Dokter = '{email}'
        AND Kode_Faskes = '{faskes}' AND Praktek_shift = '{shift}'
        AND Praktek_tgl = '{tanggal}';
    """)
    db.close()
    return redirect('/appointment/read-appointment')

def create_ruangan_rs(request):
    db = Database(schema='siruco')

    role = request.session.get('peran')
    if(role != 'admin_satgas'):
        return redirect("/")

    list_kodeRS = db.query(f"""
        SELECT Kode_Faskes FROM RUMAH_SAKIT;
    """)
    list_kodeRS = [{
        "kodeRS" : v[0]
    } for v in list_kodeRS]

    data = {
        "list_kodeRS" : list_kodeRS,
        "kodeRuangan" : 'Rxx'
    }

    if(request.method == 'POST'):
        kodeRS = request.POST.get('kodeRS')
        kodeRuangan = request.POST.get('kodeRuangan')
        tipe = request.POST.get('tipe')
        harga = request.POST.get('harga')
        db.query("""
            INSERT INTO RUANGAN_RS VALUES
            ('%s','%s','%s',0,'%s');
        """ % (kodeRS, kodeRuangan, tipe, harga))
        return redirect('/appointment/read-ruangan-rs')
    
    db.close()
    return render(request, 'form-ruangan-rs.html', data)

def get_next_ruang(request, kodeRS):
    db = Database(schema='siruco')
    kodeRuangan = db.query(f"""
        SELECT TO_CHAR(MAX(TO_NUMBER(KodeRuangan,'L9999'))+1, 'FM0000') FROM RUANGAN_RS
        WHERE KodeRS = '{kodeRS}';
    """)
    kodeRuangan = [{
        "r" : v[0]
    } for v in kodeRuangan]
    kodeRuangan = kodeRuangan[0].get("r")

    kodeRuangan = "R" + str(kodeRuangan)
    data = {
        "kodeRuangan" : kodeRuangan
    }
    db.close()
    return JsonResponse(data)

def create_bed_rs(request):
    db = Database(schema='siruco')

    role = request.session.get('peran')
    if(role != 'admin_satgas'):
        return redirect("/")

    list_kodeRS = db.query(f"""
        SELECT Kode_Faskes FROM RUMAH_SAKIT;
    """)
    list_kodeRS = [{
        "kodeRS" : v[0]
    } for v in list_kodeRS]

    data = {
        'list_kodeRS' : list_kodeRS,
        'kodeBed' : 'Bxx'
    }

    if (request.method == 'POST'):
        kodeRS = request.POST.get('kodeRS')
        kodeBed = request.POST.get('kodeBed')
        kodeRuangan = request.POST.get('kodeRuangan')
        db.query("""
            INSERT INTO BED_RS VALUES
            ('%s','%s','%s');
        """ % (kodeRuangan, kodeRS, kodeBed))
        return redirect('/appointment/read-bed-rs')

    db.close()
    return render(request, 'form-bed-rs.html', data)

def get_ruang_rs(request, kodeRS):
    db = Database(schema='siruco')
    list_kodeRuangan = db.query(f"""
        SELECT kodeRuangan FROM RUANGAN_RS
        WHERE KodeRS = '{kodeRS}';
    """)
    list_kodeRuangan = [{
        "kodeRuangan" : v[0]
    } for v in list_kodeRuangan]
    data = {
        "list_kodeRuangan" : list_kodeRuangan
    }
    db.close()
    return JsonResponse(data)

def get_next_bed(request, kodeRS, kodeRuangan):
    db = Database(schema='siruco')
    kodeBed = db.query(f"""
        SELECT TO_CHAR(MAX(TO_NUMBER(KodeBed,'L9999'))+1,'FM0000') FROM BED_RS
        WHERE KodeRS= '{kodeRS}' AND KodeRuangan = '{kodeRuangan}';
    """)
    kodeBed = [{
        "r" : v[0]
    } for v in kodeBed]
    kodeBed = kodeBed[0].get("r")

    kodeBed = "B" + str(kodeBed)
    data = {
        "kodeBed" : kodeBed
    }
    db.close()
    return JsonResponse(data)

def read_ruangan_rs(request):
    db = Database(schema='siruco')

    role = request.session.get('peran')
    if(role != 'admin_satgas'):
        return redirect("/")

    # list_ruangan_rs = db.query('SELECT * FROM RUANGAN_RS;')
    list_ruangan_rs = db.query("""
        SELECT KodeRS, KodeRuangan, tipe, jmlBed, 'Rp'||TO_CHAR(harga, 'FM999G999G999G999G999')
        FROM RUANGAN_RS;
    """)
    list_ruangan_rs = [{
        "no" : list_ruangan_rs.index(v)+1,
        "kodeRS" : v[0],
        "kodeRuangan" : v[1],
        "tipe" : v[2],
        "jmlBed" : v[3],
        "harga" : v[4]
    } for v in list_ruangan_rs]
    data = {
        "list_ruang" : list_ruangan_rs
    }
    db.close()
    return render(request, "read-ruangan-rs.html", data)

def read_bed_rs(request):
    db = Database(schema='siruco')

    role = request.session.get('peran')
    if(role != 'admin_satgas'):
        return redirect("/")


    delete = db.query("""
        SELECT * FROM BED_RS WHERE KodeBed NOT IN (SELECT KodeBed FROM RESERVASI_RS)
        OR KodeBed IN (SELECT KodeBed from RESERVASI_RS WHERE TglKeluar < CURRENT_DATE);
    """)
    delete = [{
        "no" : delete.index(v)+1,
        "kodeRS" : v[0],
        "kodeRuangan" : v[1],
        "kodeBed" : v[2]
    } for v in delete]

    nodelete = db.query("""
        SELECT * FROM BED_RS WHERE KodeBed NOT IN
        (SELECT KodeBed FROM BED_RS WHERE KodeBed NOT IN (SELECT KodeBed FROM RESERVASI_RS)
        OR KodeBed IN (SELECT KodeBed from RESERVASI_RS WHERE TglKeluar < CURRENT_DATE));
    """)
    nodelete = [{
        "no" : nodelete.index(v)+len(delete),
        "kodeRS" : v[0],
        "kodeRuangan" : v[1],
        "kodeBed" : v[2]
    } for v in nodelete]

    data = {
        "delete" : delete,
        "nodelete" : nodelete
    }
    db.close()
    return render(request, "read-bed-rs.html", data)

def update_ruangan_rs(request, kodeRS, kodeRuangan):
    db = Database(schema='siruco')

    role = request.session.get('peran')
    if(role != 'admin_satgas'):
        return redirect("/")

    tipe_harga = db.query(f"""
        SELECT tipe, harga FROM RUANGAN_RS
        WHERE KodeRS = '{kodeRS}'
        AND KodeRuangan = '{kodeRuangan}';
    """)
    tipe_harga = [{
        "tipe" : v[0],
        "harga" : v[1]
    } for v in tipe_harga]
    tipe = tipe_harga[0].get("tipe")
    harga = tipe_harga[0].get("harga")
    data = {
        "kodeRS" : kodeRS,
        "kodeRuangan" : kodeRuangan,
        "tipe" : tipe,
        "harga" : harga
    }

    if(request.method == 'POST'):
        tipe = request.POST.get("tipe")
        harga = request.POST.get("harga")
        db.query(f"""
            UPDATE RUANGAN_RS
            SET tipe = '{tipe}', harga = '{harga}'
            WHERE KodeRS = '{kodeRS}' AND KodeRuangan = '{kodeRuangan}';
        """)
        return redirect('/appointment/read-ruangan-rs')
    db.close()
    return render(request, "update-ruangan-rs.html", data)

def delete_bed_rs(request, kodeRS, kodeRuangan, kodeBed):
    db = Database(schema='siruco')

    role = request.session.get('peran')
    if(role != 'admin_satgas'):
        return redirect("/")

    db.query(f"""
        DELETE FROM BED_RS
        WHERE KodeRS = '{kodeRS}' AND KodeRuangan = '{kodeRuangan}' AND KodeBed = '{kodeBed}';
    """)
    db.close()
    return redirect('/appointment/read-bed-rs')