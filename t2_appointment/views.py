from django.shortcuts import render,redirect
from siruco.db import Database

# Create your views here.

def create_jadwal(request):
    db = Database(schema='siruco')
    data = {}

    if(request.method == 'GET'):
        list_jadwal = db.query(f'''
                                SELECT *
                                FROM JADWAL
                                WHERE (kode_faskes, shift, tanggal)
                                NOT IN (SELECT kode_faskes, shift, tanggal
                                FROM JADWAL_DOKTER);
                                ''')

        list_jadwal = [{
        "kode_faskes" : v[0],
        "shift" : v[1],
        "tanggal" : v[2]
        } for v in list_jadwal]

        data = {
            "jadwal" : list_jadwal
        }

        db.close()

    elif(request.method == 'POST'):

        username = request.COOKIES.get('username')
        faskes = request.POST.get('faskes')
        shift = request.POST.get('shift')
        tanggal = request.POST.get('tanggal')

        no_str = db.query(f'''
                            SELECT D.no_str
                            FROM DOKTER D, ADMIN A, AKUN_PENGGUNA AP
                            WHERE AP.username = {username} 
                            AND A.username = AP.username
                            AND D.username = A.username;
                            ''')
        
        db.query('''
            INSERT INTO JADWAL_DOKTER
            VALUES('%s','%s','%s','%s','%s',0);
        ''' % (no_str, username, faskes, shift, tanggal))

        db.close()
        return redirect('/appointment/jadwal')

    return render(request, "create-jadwal.html", data)

def read_jadwal(request):
    db = Database(schema='siruco')

    username = request.COOKIES.get('username')
    role = request.COOKIES.get('peran')
    query = ''
    if(role == 'dokter'):
        query = "SELECT * FROM JADWAL_DOKTER WHERE username = '" + username + "';"
    else:
        query = "SELECT * FROM JADWAL_DOKTER;"
    list_jadwal = db.query(query)

    list_jadwal = [{
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
    
    # todo : buat selain dokter doang bisanya

    list_jadwal = db.query("SELECT * FROM JADWAL_DOKTER;")

    list_jadwal = [{
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

    pass
