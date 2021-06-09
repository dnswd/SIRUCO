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

        return render(request, 'login.html')

    elif request.method == 'GET':
        return render(request, 'login.html')

def dashboard(request):
    print(session(request, 'peran'))
    print(session(request, 'username'))
    if session(request, 'peran') == 'pengguna_publik':
      return render(request, 'dashboard.html')
    elif session(request, 'peran') == 'admin_dokter':
      return render(request, 'dashboard.html')
    elif session(request, 'peran') == 'admin_sistem':
      return render(request, 'dashboard.html')      
    elif session(request, 'peran') == 'admin_satgas':
      return render(request, 'dashboard.html')
    else :
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
        if nama := get_user(username, password) == []:
            status = record_new_user(request.POST)

            if request.POST.get('peran') == 'pengguna_publik':
                status = record_as_pengguna_publik(request.POST)
            else :
                status = record_as_admin(request.POST)
                if request.POST.get('peran') == 'admin_dokter':
                    status = record_as_admin_dokter(request.POST)
                elif request.POST.get('peran') == 'admin_sistem':
                    status = record_as_admin_sistem(request.POST)
                elif request.POST.get('peran') == 'admin_satgas':
                    status = record_as_admin_satgas(request.POST)
                else:
                    return redirect('/account/register')  # TODO: proper redirect to form

            session(request, 'nama', request.POST.get('nama'))
            session(request, 'username', request.POST.get('email'))
            session(request, 'peran', request.POST.get('peran'))
            return redirect('/')  # TODO: proper redirect to homepage

        else:
            print("register failed")
            return redirect('/account/register') # TODO: proper redirect to form

    elif request.method == 'GET':
        return render(request, 'register.html') # halaman milih formulir, redirect ke form masing-masing


def logout(request):
    request.session.flush()
    request.session.clear_expired()
    return redirect('t1_auth:login')  # redirect ke homepage

def register_admin_sistem(request):
    return render(request, 'register_admin_sistem.html')

def register_user(request):
    return render(request, 'register_user.html')

def register_admin_satgas(request):
    response = { 'fakseslist' : get_kode_faskes() }
    return render(request, 'register_admin_satgas.html', response)

def register_dokter(request):
    return render(request, 'register_dokter.html')

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
    return result[0] > 0

def record_as_admin(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO ADMIN VALUES (
                          '{data.get('email')}'
                      );
                      ''')
    db.close()
    return result[0] > 0
  
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


def record_as_admin_sistem(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO ADMIN VALUES (
                          '{data.get('email')}'
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
