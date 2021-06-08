from django.shortcuts import render
from siruco.db import Database

# Create your views here.

def get_jadwal(request):
    db = Database(schema='siruco')
    list_jadwal = db.query(f'''
                            SELECT * 
                            FROM JADWAL
                            ''')
    db.close()

    list_jadwal = [{
        "kode_faskes" : v[2],
        "shift" : v[1],
        "tanggal" : v[0]
    } for v in list_jadwal]

    data = {
        "jadwal" : list_jadwal
    }

    return render(request, 'get_jadwal.html', data)

def get_jadwal_dokter(request):

    db = Database(schema='siruco')
    list_jadwal = db.query(f'''
                            SELECT * 
                            FROM JADWAL_DOKTER
                            ''')
    db.close()

    list_jadwal = [{
        "no_str" : v[0],
        "dokter" : v[1],
        "faskes" : v[5],
        "shift" : v[4],
        "tanggal" : v[3],
        "jml_pasien" : v[2]
    } for v in list_jadwal]

    data = {
        "jadwal" : list_jadwal
    }

    return render(request, 'get_jadwal_dokter.html', data)


def create_jadwal(request):
    db = Database(schema='siruco')
    data = {}

    if(request.method == 'GET'):
        list_jadwal = db.query(f'''
                                SELECT *
                                FROM JADWAL
                                WHERE (kode_faskes, shift, tanggal)
                                NOT IN (SELECT kode_faskes, shift, tanggal
                                FROM JADWAL_DOKTER)
                                ''')

        list_jadwal = [{
        "kode_faskes" : v[2],
        "shift" : v[1],
        "tanggal" : v[0]
        } for v in list_jadwal]

        data = {
            "jadwal" : list_jadwal
        }

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
                            AND D.username = A.username
                            ''')
        
        # db.query()



    return render(request, "create-appointment-get.html", data)
