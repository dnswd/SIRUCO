from django.shortcuts import render, redirect
from siruco.db import Database

# Dennis Al Baihaqi Walangadi (c) 2021
# TODO: sql injection?

def ruangan_hotel(request):
    if request.method == 'POST':
        if request.session.get('role') == 'admin_sistem':
            create_ruangan_hotel(request.POST)
            return redirect('hotel/')
    elif request.method == 'GET':
        role = request.session.get('role')
        if role == 'admin_sistem':
            pass
    pass

def reservasi_hotel(request):
    pass

def transaksi_hotel(request):
    pass

def transaksi_booking_hotel(request):
    pass

# Helper functions
def create_ruangan_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             INSERT INTO HOTEL_ROOM(KodeHotel,KodeRoom,JenisBed,Tipe,Harga) VALUES (
                 '{data.get('kode_hotel')}',
                 '{data.get('kode_room')}',
                 '{data.get('jenis_bed')}',
                 '{data.get('tipe_room')}',
                 '{data.get('harga')}'
             );
             ''')
    db.close()
    return

def read_ruangan_hotel(data):
    db = Database(schema='siruco')
    db.query('''
             SELECT * FROM HOTEL_ROOM;
             ''')
    db.close()
    return

def update_ruangan_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             UPDATE HOTEL_ROOM
             SET JenisBed = '{data.get('jenis_bed')}',
                 Tipe = '{data.get('tipe_room')}',
                 Harga = '{data.get('harga')}'
             WHERE 
                KodeHotel = '{data.get('kode_hotel')}' AND
                KodeRoom = '{data.get('kode_room')}';
             ''')
    db.close()
    return

def delete_ruangan_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             DELETE FROM HOTEL_ROOM
             WHERE 
                KodeHotel = '{data.get('kode_hotel')}' AND
                KodeRoom = '{data.get('kode_room')}';
             ''')
    db.close()
    return

def create_reservasi_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             INSERT INTO RESERVASI_HOTEL(KodePasien,TglMasuk,TglKeluar,KodeHotel,KodeRoom) VALUES (
                 '{data.get('kode_pasien')}',
                 '{data.get('tgl_masuk')}',
                 '{data.get('tgl_keluar')}',
                 '{data.get('kode_hotel')}',
                 '{data.get('kode_room')}'
             );
             ''')
    db.close()
    return

def read_reservasi_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             SELECT * FROM RESERVASI_HOTEL;
             ''')
    db.close()
    return

def update_reservasi_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             UPDATE RESERVASI_HOTEL
             SET
                 TglKeluar = '{data.get('tgl_keluar')}',
                 KodeHotel = '{data.get('kode_hotel')}',
                 KodeRoom = '{data.get('kode_room')}'
             WHERE
                 KodePasien = '{data.get('kode_pasien')}' AND
                 TglMasuk = '{data.get('tgl_masuk')}';
             ''')
    db.close()
    return

def delete_reservasi_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             DELETE FROM RESERVASI_HOTEL
             WHERE
                 KodePasien = '{data.get('kode_pasien')}' AND
                 TglMasuk = '{data.get('tgl_masuk')}';
             ''')
    db.close()
    return

def create_transaksi_hotel(data):
    '''
    TODO: Calculate biaya_total (see trigger 4)
    '''
    db = Database(schema='siruco')
    db.query(f'''
             INSERT INTO TRANSAKSI_HOTEL(KodePasien,TanggalPembayaran,WaktuPembayaran,TotalBayar,StatusBayar) VALUES (
                 '{data.get('kode_pasien')}',
                 NULL,
                 NULL,
                 '{data.get('biaya_total')}',
                 'Belum Lunas'
             );
             ''')
    db.close()
    return

def read_transaksi_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             SELECT * FROM TRANSAKSI_HOTEL;
             ''')
    db.close()
    return

def update_transaksi_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             UPDATE TRANSAKSI_HOTEL
             SET 
                 KodePasien = '{data.get('kode_pasien')}'
                 TanggalPembayaran = '{data.get('tanggal_pembayaran')}'
                 WaktuPembayaran = '{data.get('waktu_pembayaran')}'
                 TotalBayar = '{data.get('total_bayar')}'
                 StatusBayar = '{data.get('status_bayar')}'
             WHERE
                 IdTransaksi = '{data.get('id_transaksi')}';
             ''')
    db.close()
    return

def delete_transaksi_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             DELETE FROM TRANSAKSI_HOTEL
             WHERE
                 IdTransaksi = '{data.get('id_transaksi')}';
             ''')
    db.close()
    return

def create_transaksi_booking_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             INSERT INTO TRANSAKSI_BOOKING(TotalBayar,KodePasien,TglMasuk) VALUES (
                 '{data.get('total_bayar')}',
                 '{data.get('kode_pasien')}',
                 '{data.get('tgl_masuk')}'
             );
             ''')
    db.close()
    return

def read_transaksi_booking_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             SELECT * FROM TRANSAKSI_BOOKING;
             ''')
    db.close()
    return

def delete_transaksi_booking_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             DELETE FROM TRANSAKSI_BOOKING
             WHERE
                IdTransaksiBooking = '{data.get('id_transaksi_booking')}'
             ''')
    db.close()
    return

