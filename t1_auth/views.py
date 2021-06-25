from django.shortcuts import render, redirect
from siruco.db import Database


def login(request):
    request.session.clear_expired()
    if session(request, 'peran'):
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = get_user(username, password)

        if len(user) != 0:
            user = user[0]
            # session(request, 'nama', user[0]) nama != username
            session(request, 'username', username)
            session(request, 'peran', user[1])
            if is_admin(username, password):
                session(request, 'su', 1)
            return redirect('/account/dashboard')

        return render(request, 'login.html', {"error": True})

    elif request.method == 'GET':
        return render(request, 'login.html')


def dashboard(request):
    peran = session(request, 'peran')
    username = session(request, 'username')
    response = {'peran': peran, 'username': username}
    if session(request, 'peran') == 'pengguna_publik':
        return render(request, 'dashboard.html', response)
    elif session(request, 'peran') == 'admin_dokter':
        return render(request, 'dashboard.html', response)
    elif session(request, 'peran') == 'admin_sistem':
        return render(request, 'dashboard.html', response)
    elif session(request, 'peran') == 'admin_satgas':
        return render(request, 'dashboard.html', response)
    else:
        return redirect('/')


def register(request):
    request.session.clear_expired()
    if session(request, 'peran'):
        return redirect('/')

    if request.method == 'POST':

        # response = render(request)
        # TODO: validation, record original form path, redirect to original form path
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = is_exist(username)

        if len(user) == 0:
            status = record_new_user(request.POST)
            if not status:
                return render(request, "register.html", {"error": True})

            if request.POST.get('peran') == 'pengguna_publik':
                status = record_as_pengguna_publik(request.POST)
            else:
                status = record_as_admin(request.POST)
                if request.POST.get('peran') == 'admin_dokter':
                    status = record_as_admin_dokter(request.POST)
                elif request.POST.get('peran') == 'admin_satgas':
                    status = record_as_admin_satgas(request.POST)
                else:
                    # TODO: proper redirect to form
                    return redirect('/account/register')

            session(request, 'nama', request.POST.get('nama'))
            session(request, 'username', request.POST.get('email'))
            session(request, 'peran', request.POST.get('peran'))
            return redirect('/')  # TODO: proper redirect to homepage

        else:
            print("register failed")
            # TODO: proper redirect to form
            return render(request, "register.html", {"exist": True})

    elif request.method == 'GET':
        # halaman milih formulir, redirect ke form masing-masing
        return render(request, 'register.html')


def logout(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect('t1_auth:login')  # redirect ke homepage


def register_admin_sistem(request):
    return render(request, 'register_admin_sistem.html')


def register_user(request):
    return render(request, 'register_user.html')


def register_admin_satgas(request):
    response = {'fakseslist': get_kode_faskes()}
    return render(request, 'register_admin_satgas.html', response)


def register_dokter(request):
    return render(request, 'register_dokter.html')


def pasien_create(request):
    peran = session(request, 'peran')
    username = session(request, 'username')
    if (peran != 'pengguna_publik'):
        return redirect('/')

    if (request.method == 'GET'):
        response = {
            "username": username
        }
        return render(request, 'pasien_create.html', response)
    else:
        res = request.POST
        db = Database(schema='siruco')
        db.query(f'''
        INSERT INTO PASIEN VALUES
        ('{res.get('nik')}', 
        '{res.get('pendaftar')}', 
        '{res.get('nama')}', 
        '{res.get('jalanK')}', 
        '{res.get('kelurahanK')}', 
        '{res.get('kecamatanK')}', 
        '{res.get('kotaK')}', 
        '{res.get('provinsiK')}', 
        '{res.get('jalanD')}', 
        '{res.get('kelurahanD')}', 
        '{res.get('kecamatanD')}', 
        '{res.get('kotaD')}', 
        '{res.get('provinsiD')}', 
        '{res.get('noTelp')}', 
        '{res.get('noHP')}')
        ''')

        db.close()
        return redirect('/account/pasien')


def pasien(request):
    peran = session(request, 'peran')
    username = session(request, 'username')
    if (peran != 'pengguna_publik'):
        return redirect('/')

    db = Database(schema='siruco')
    pasiens = db.query(f'''
    SELECT nik, nama
    FROM PASIEN
    WHERE idpendaftar = '{username}'
    ''')

    response = {
        "pasien": [{"nik": pasiens[p][0],
                    "nama": pasiens[p][1]}
                   for p in range(len(pasiens))]
    }
    db.close()
    return render(request, 'pasien.html', response)


def pasien_update(request, nik):
    peran = session(request, 'peran')
    username = session(request, 'username')

    if (peran != 'pengguna_publik'):
        return redirect('/')

    if (request.method == 'GET'):

        db = Database(schema='siruco')
        pasien = db.query(f'''
        SELECT nik, nama
        FROM PASIEN         
        WHERE nik = '{nik}'    
        ''')
        response = {
            "pasien": {"nik": pasien[0][0],
                       "nama": pasien[0][1]},
            "username": username
        }
        db.close()
        return render(request, 'pasien_update.html', response)

    else:
        res = request.POST
        db = Database(schema='siruco')
        db.query(f'''
        UPDATE PASIEN
        SET nama = '{res.get('nama')}',
        ktp_jalan = '{res.get('jalanK')}',
        ktp_kelurahan = '{res.get('kelurahanK')}',
        ktp_kecamatan = '{res.get('kecamatanK')}',
        ktp_kabkot = '{res.get('kotaK')}',
        ktp_prov = '{res.get('provinsiK')}',
        dom_jalan = '{res.get('jalanD')}',
        dom_kelurahan = '{res.get('kelurahanD')}',
        dom_kecamatan = '{res.get('kecamatanD')}',
        dom_kabkot = '{res.get('kotaD')}',
        dom_prov = '{res.get('provinsiD')}',
        notelp = '{res.get('noTelp')}',
        nohp = '{res.get('noHP')}'
        WHERE nik = '{nik}'
        ''')

        db.close()
        return redirect('/account/pasien')


def pasien_detail(request, nik):
    peran = session(request, 'peran')
    username = session(request, 'username')

    if (peran != 'pengguna_publik'):
        return redirect('/')

    db = Database(schema='siruco')
    pasien = db.query(f'''
    SELECT *
    FROM PASIEN         
    WHERE nik = '{nik}'    
    ''')
    response = {
        "nik": pasien[0][0],
        "pendaftar": pasien[0][1],
        "nama": pasien[0][2],
        "jalanK": pasien[0][3],
        "kelurahanK": pasien[0][4],
        "kecamatanK": pasien[0][5],
        "kotaK": pasien[0][6],
        "provinsiK": pasien[0][7],
        "jalanD": pasien[0][8],
        "kelurahanD": pasien[0][9],
        "kecamatanD": pasien[0][10],
        "kotaD": pasien[0][11],
        "provinsiD": pasien[0][12],
        "notelp": pasien[0][13],
        "nohp": pasien[0][14],
    }
    db.close()
    return render(request, 'pasien_detail.html', response)


def pasien_delete(request, nik):

    db = Database(schema='siruco')
    db.query(f'''
    DELETE FROM PASIEN
    WHERE nik = '{nik}'
    ''')

    db.close()
    return redirect('/account/pasien')

# Helper functions


def is_admin(username, password):
    db = Database(schema='siruco')
    admin = db.query(f'''
                      SELECT a.username FROM admin a
                      LEFT JOIN akun_pengguna p
                        ON a.username = p.username
                      WHERE a.username='{username}' AND
                            p.password='{password}';
                      ''')
    db.close()
    return len(admin) > 0


def is_exist(username):
    db = Database(schema='siruco')
    user = db.query(f'''
                      SELECT username, peran FROM AKUN_PENGGUNA
                      WHERE username='{username}'
                      ''')
    db.close()
    return user


def get_user(username, password):
    db = Database(schema='siruco')
    user = db.query(f'''
                      SELECT username, peran FROM AKUN_PENGGUNA
                      WHERE username='{username}' AND
                            password='{password}';
                      ''')
    db.close()  # harus di-close
    print(user)
    return user


def record_new_user(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO AKUN_PENGGUNA VALUES (
                          '{data.get('email')}',
                          '{data.get('password')}',
                          '{data.get('peran')}'
                      );
                      ''')
    db.close()
    return len(result) > 0


def record_as_admin(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO ADMIN VALUES (
                          '{data.get('email')}'
                      );
                      ''')
    db.close()
    return len(result) > 0


def record_as_pengguna_publik(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO PENGGUNA_PUBLIK VALUES (
                          '{data.get('email')}',
                          '{data.get('nik')}',
                          '{data.get('nama')}',
                          'AKTIF',
                          '{data.get('peran')}',
                          '{data.get('no_hp')}'
                      );
                      ''')
    db.close()
    return len(result) > 0


def record_as_admin_dokter(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO DOKTER VALUES (
                          '{data.get('email')}',
                          '{data.get('no_str')}',
                          '{data.get('nama')}',
                          '{data.get('no_hp')}',
                          '{data.get('gelar_depan')}',
                          '{data.get('gelar_belakang')}'
                      );
                      ''')
    db.close()
    return len(result) > 0


def record_as_admin_satgas(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO ADMIN_SATGAS VALUES (
                          '{data.get('email')}',
                          '{data.get('id_faskes')}'
                      );
                      ''')
    db.close()
    return len(result) > 0


def get_kode_faskes():
    db = Database(schema='siruco')
    kode = db.query(f'''
                      SELECT kode FROM FASKES;
                      ''')
    db.close()
    result = []
    for item in kode:
        result.append(item[0])
    print(result)
    return result


def session(http_handler, key, value=None):
    if value:
        http_handler.session[key] = value
        return http_handler
    else:
        returning = None
        try:
            returning = http_handler.session[key]
        except Exception:
            pass
        return returning
