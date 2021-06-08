from django.shortcuts import render
from siruco.db import Database
# Create your views here.

def login(request):
    if request.method == 'POST':
        response = render(request)
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        if user := get_user(username, password) != '':
            response.set_cookie('nama', user[0])
            response.set_cookie('username', username)
            if is_admin(username, password):
                response.set_cookie('su', 1)
            return response
        
        return response
    
    elif request.method == 'GET':
        return render(request)


def register(request):
    if request.method == 'POST':
        response = render(request)
        # TODO validation
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        if nama := get_user(username, password) == '':
            status = record_new_user(request.POST)
            print("record_new_user:", status, username, password)
            
            if request.POST.get('peran') == 'pengguna_publik':
                status = record_as_pengguna_publik(request.POST)
            elif request.POST.get('peran') == 'admin_dokter':
                status = record_as_admin_dokter(request.POST)
            elif request.POST.get('peran') == 'admin_sistem':
                status = record_as_admin_sistem(request.POST)
            elif request.POST.get('peran') == 'admin_satgas':
                status = record_as_admin_satgas(request.POST)
                
            response.set_cookie('username', username)
            response.set_cookie('peran', 'admin')
            return response
        
        else:
            return response
    
    elif request.method == 'GET':
        return render(request)

# Helper functions
def is_admin(username, password):
    db = Database(schema='siruco')
    admin = db.query(f'''
                      SELECT a.username FROM admin a
                      LEFT JOIN akun_pengguna p
                        ON a.username = p.username
                      WHERE a.username={username} AND
                            p.password={password};
                      ''')
    db.close()
    return len(admin) > 0

def get_user(username, password):
    db = Database(schema='siruco')
    user = db.query(f'''
                      SELECT a.nama, p.peran FROM PENGGUNA_PUBLIK a
                      LEFT JOIN akun_pengguna p
                        ON a.username = p.username
                      WHERE a.username={username} AND
                            p.password={password};
                      ''')
    db.close() # harus di-close
    return user

def record_new_user(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO AKUN_PENGGUNA VALUES (
                          {data.get('email')},
                          {data.get('password')},
                          {data.get('peran')}
                      );
                      ''')
    db.close()
    return result[0] > 0

def record_as_pengguna_publik(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO PENGGUNA_PUBLIK VALUES (
                          {data.get('email')},
                          {data.get('nik')},
                          {data.get('nama')},
                          TIDAKAKTIF,
                          {data.get('peran')},
                          {data.get('no_hp')}
                      );
                      ''')
    db.close()
    return len(result) > 0

def record_as_admin_dokter(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO DOKTER VALUES (
                          {data.get('email')},
                          {data.get('no_str')},
                          {data.get('nama')},
                          {data.get('no_hp')},
                          {data.get('gelar_depan')},
                          {data.get('gelar_belakang')}
                      );
                      ''')
    db.close()
    return len(result) > 0

def record_as_admin_sistem(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO ADMIN VALUES (
                          {data.get('email')}
                      );
                      ''')
    db.close()
    return len(result) > 0

def record_as_admin_satgas(data):
    db = Database(schema='siruco')
    result = db.query(f'''
                      INSERT INTO ADMIN_SATGAS VALUES (
                          {data.get('email')},
                          {data.get('id_faskes')}
                      );
                      ''')
    db.close()
    return len(result) > 0