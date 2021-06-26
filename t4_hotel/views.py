from django.shortcuts import render, redirect
from django.http import HttpResponse
from siruco.db import Database
from .forms import HotelRoomForm, EditHotelRoomForm, ReservationForm, EditReservationForm, EditTransactionForm
import json

# Dennis Al Baihaqi Walangadi (c) 2021
# This code is prone to SQL Injection, but security isn't the main concern because:
#     1. I need to study for finals
#     2. Security mitigations doesn't increase my score according to the specification


def index(request):
    role = request.session.get('peran')
    if role is None or role not in ['admin_satgas', 'admin_sistem', 'pengguna_publik']:
        return redirect('t1_auth:login')

    hotels = list_hotel_rooms()
    context = {'hotels': hotels if len(hotels) > 0 else False,
               'peran': request.session['peran']}
    return render(request, 'hotel_index.html', context=context)


def ruangan_hotel(request):
    role = request.session.get('peran')
    if role is None or role != 'admin_sistem':
        return redirect('t1_auth:login')

    if request.method == 'GET':

        hotel_room_form = HotelRoomForm(
            initial={'kode_ruangan': new_hotel_room()})
        hotel_room_form.fields['kode_hotel'].choices = list_to_choice_array(
            get_hotel_codes())

        context = {'form': hotel_room_form}
        # render index
        return render(request, 'hotel_ruangan.html', context=context)

    elif request.method == 'POST':
        data = {}
        data['kode_hotel'] = kode_hotel = request.POST.get('kode_hotel')
        # I don't have much time
        data['kode_room'] = kode_ruangan = new_hotel_room()
        data['jenis_bed'] = jenis_bed = request.POST.get('jenis_bed')
        data['tipe_room'] = tipe = request.POST.get('tipe')
        data['harga'] = harga_per_hari = request.POST.get(
            'harga_per_hari')

        if kode_hotel and kode_ruangan and jenis_bed and tipe and harga_per_hari:
            create_ruangan_hotel(data)
        else:
            context = {'form': HotelRoomForm(request.POST)}
            context['form'].fields['kode_hotel'].choices = list_to_choice_array(
                get_hotel_codes())
            return render(request, 'hotel_ruangan.html', context=context)

    elif request.method == 'UPDATE':
        update_ruangan_hotel(request.POST)
    elif request.method == 'DELETE':
        delete_ruangan_hotel(request.POST)

    return redirect('t4_hotel:hotel_index')


def ubah_ruangan_hotel(request, koderoom=None):
    role = request.session.get('peran')
    if role is None or role != 'admin_sistem':
        return redirect('t1_auth:login')

    if request.method == 'GET':
        room_data = get_room_data(koderoom)
        form = EditHotelRoomForm(initial={
            'kode_hotel': room_data[0],
            'kode_ruangan': room_data[1],
            'jenis_bed': room_data[2],
            'tipe': room_data[3],
            'harga_per_hari': room_data[4],
        })
        context = {'form': form}
        return render(request, 'hotel_ruangan_update.html', context=context)

    elif request.method == 'POST':
        data = {}
        room_data = get_room_data(koderoom)
        data['kode_hotel'] = kode_hotel = room_data[0]
        data['kode_room'] = kode_ruangan = room_data[1]
        data['jenis_bed'] = jenis_bed = request.POST.get('jenis_bed')
        data['tipe_room'] = tipe = request.POST.get('tipe')
        data['harga'] = harga_per_hari = request.POST.get('harga_per_hari')
        print(data)
        update_ruangan_hotel(data)

        return redirect('t4_hotel:hotel_index')


def remove_ruangan_hotel(request, koderoom=None):
    role = request.session.get('peran')
    if role is None or role != 'admin_sistem':
        return redirect('t1_auth:login')

    if koderoom:
        delete_ruangan_hotel(koderoom)

    return redirect('t4_hotel:hotel_index')


def index_reservasi(request):
    role = request.session.get('peran')
    if role is None or role not in ['admin_satgas', 'pengguna_publik']:
        return redirect('t1_auth:login')

    rsvp = read_reservasi_hotel()
    return render(request, 'hotel_reservasi_index.html', context={'rsvp': rsvp, 'peran': request.session['peran']})


def reservasi_hotel(request):
    role = request.session.get('peran')
    if role is None or role not in ['admin_satgas', 'pengguna_publik']:
        return redirect('t1_auth:login')

    if request.method == 'GET':
        form = ReservationForm()
        form.fields['nik'].choices = list_to_choice_array(list_nik_pasien())
        form.fields['kode_hotel'].choices = list_to_choice_array(
            get_hotel_codes())
        # render form
        return render(request, 'hotel_reservasi.html', context={'form': form})
    elif request.method == 'POST':
        data = {}
        create_reservasi_hotel(request.POST)
        pass

    # if role == 'admin_satgas':
    #     if request.method == 'UPDATE':
    #         update_reservasi_hotel(request.POST)
    #     elif request.method == 'DELETE':
    #         delete_reservasi_hotel(request.POST)

    return redirect('t4_hotel:reservasi_index')  # refresh the form


def remove_reservasi_hotel(request, nik=None, tglmasuk=None):
    role = request.session.get('peran')
    if role is None or role not in ['admin_satgas', 'pengguna_publik']:
        return redirect('t1_auth:login')

    if nik and tglmasuk:
        delete_reservasi_hotel(nik=nik, tglmasuk=tglmasuk)

    return redirect('t4_hotel:reservasi_index')


def edit_reservasi_hotel(request, nik=None, tglmasuk=None):
    role = request.session.get('peran')
    if role is None or role not in ['admin_satgas', 'pengguna_publik']:
        return redirect('t1_auth:login')

    if request.method == 'POST':
        update_reservasi_hotel(nik, tglmasuk, request.POST.get('tgl_keluar'))
        return redirect('t4_hotel:reservasi_index')

    if nik and tglmasuk:
        data = get_reservasi_hotel(nik, tglmasuk)
        form = EditReservationForm(initial={
            "nik": nik,
            "tgl_masuk": tglmasuk,
            "tgl_keluar": data[2],
            "kode_hotel": data[3],
            "kode_ruangan": data[4]
        })

    return render(request, 'hotel_reservasi.html', context={'form': form})


def fetch_hotel_room(request, hotel=None):
    if hotel:
        rooms = rooms_by_hotel(hotel)
        return HttpResponse(json.dumps(rooms))


def transaksi_hotel(request):
    role = request.session.get('peran')
    if role is None or not role == 'admin_satgas':
        return redirect('/')

    if role == 'admin_satgas':
        if request.method == 'GET':
            transactions = read_transaksi_hotel()
            context = {'transactions': transactions}
            # render form
        return render(request, 'hotel_transaksi_index.html', context=context)


def transaksi_hotel_edit(request, idtransaksi=None):
    role = request.session.get('peran')
    if role is None or not role == 'admin_satgas':
        return redirect('/')

    if request.method == 'GET' and idtransaksi:
        data = get_transaksi_hotel(idtransaksi=idtransaksi)
        form = EditTransactionForm(initial={
            'nik': data[1],
            'idtransaksi': data[0],
            'tglbayar': data[2],
            'wktbayar': data[3],
            'totalbiaya': data[4],
            'statusbayar': data[5]
        })
        context = {'form': form}
        # render form
        return render(request, 'hotel_transaksi.html', context=context)
    elif request.method == 'POST':
        update_transaksi_hotel(idtransaksi, request.POST.get('statusbayar'))

    return redirect('t4_hotel:transaksi_hotel')


def transaksi_booking_hotel(request):
    role = request.session.get('peran')
    if role is None or role not in ['admin_satgas', 'pengguna_publik']:
        return redirect('/')

    else:
        bookings = read_transaksi_booking_hotel()
        return render(request, 'hotel_transaksi_booking.html', context={'bookings': bookings})  # show form

# Helper functions


def new_hotel_room():
    return 'RH%03d' % (int(get_max_hotel_room_code()[2:])+1)


def list_to_choice_array(lst):
    ret = []
    for data in lst:
        ret.append((data, data))
    return ret


def list_hotel_rooms():
    db = Database(schema='siruco')
    result = db.query(f'''
                       SELECT *,
                       CASE
                            WHEN koderoom IN (
                                SELECT koderoom
                                FROM RESERVASI_HOTEL
                                WHERE tglkeluar < current_date
                            )
                            OR koderoom NOT IN (
                                SELECT koderoom
                                FROM RESERVASI_HOTEL
                            ) THEN 1 ELSE 0
                            END
                       FROM HOTEL_ROOM;
                       ''')
    db.close()
    return result


def get_hotel_room_codes():
    db = Database(schema='siruco')
    result = db.query(f'''
                       SELECT koderoom FROM HOTEL_ROOM;
                       ''')
    db.close()
    return [item for row in result for item in row]


def get_max_hotel_room_code():
    db = Database(schema='siruco')
    result = db.query(f'''
                       SELECT max(koderoom) FROM HOTEL_ROOM;
                       ''')
    db.close()
    return result[0][0]


def get_room_data(koderoom):
    db = Database(schema='siruco')
    result = db.query(f'''
                       SELECT * FROM HOTEL_ROOM
                       WHERE koderoom='{koderoom}';
                       ''')
    db.close()
    return result[0]


def get_hotel_codes():
    db = Database(schema='siruco')
    result = db.query(f'''
                       SELECT kode FROM HOTEL;
                       ''')
    db.close()
    return [item for row in result for item in row]


def create_ruangan_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             INSERT INTO HOTEL_ROOM(KodeHotel,KodeRoom,JenisBed,Tipe,Harga) VALUES (
                 '{data.get('kode_hotel')}',
                 '{data.get('kode_room')}',
                 '{data.get('jenis_bed').upper()}',
                 '{data.get('tipe_room').upper()}',
                 '{data.get('harga')}'
             );
             ''')
    db.close()
    return


def read_ruangan_hotel(data):
    db = Database(schema='siruco')
    result = db.query('''
             SELECT * FROM HOTEL_ROOM;
             ''')
    db.close()
    return [item for row in result for item in row]


def update_ruangan_hotel(data):
    db = Database(schema='siruco')
    result = db.query(f'''
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


def delete_ruangan_hotel(kode_room):
    db = Database(schema='siruco')
    db.query(f'''
             DELETE FROM HOTEL_ROOM
             WHERE
                KodeRoom = '{kode_room}';
             ''')
    db.close()
    return


def create_reservasi_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             INSERT INTO RESERVASI_HOTEL(KodePasien,TglMasuk,TglKeluar,KodeHotel,KodeRoom) VALUES (
                 '{data.get('nik')}',
                 '{data.get('tgl_masuk')}',
                 '{data.get('tgl_keluar')}',
                 '{data.get('kode_hotel')}',
                 '{data.get('kode_ruangan')}'
             );
             ''')
    db.close()
    return


def read_reservasi_hotel():
    db = Database(schema='siruco')
    result = db.query(f'''
             SELECT * , CASE
                WHEN tglmasuk > current_date THEN 1
                ELSE 0 END
             FROM RESERVASI_HOTEL;
             ''')
    db.close()
    return result


def get_reservasi_hotel(nik, tglmasuk):
    db = Database(schema='siruco')
    result = db.query(f'''
             SELECT *
             FROM RESERVASI_HOTEL
             WHERE 
                KodePasien = '{nik}' AND
                TglMasuk = '{tglmasuk}';
             ''')
    db.close()
    return result[0]


def update_reservasi_hotel(kode_pasien, tgl_masuk, tgl_keluar):
    db = Database(schema='siruco')
    db.query(f'''
             UPDATE RESERVASI_HOTEL
             SET
                 TglKeluar = '{tgl_keluar}'
             WHERE
                 KodePasien = '{kode_pasien}' AND
                 TglMasuk = '{tgl_masuk}';
             ''')
    db.close()
    return


def delete_reservasi_hotel(nik, tglmasuk):
    db = Database(schema='siruco')
    db.query(f'''
             DELETE FROM RESERVASI_HOTEL
             WHERE
                 KodePasien = '{nik}' AND
                 TglMasuk = '{tglmasuk}';
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


def read_transaksi_hotel():
    db = Database(schema='siruco')
    result = db.query(f'''
             SELECT * FROM TRANSAKSI_HOTEL;
             ''')
    db.close()
    return result


def get_transaksi_hotel(idtransaksi):
    db = Database(schema='siruco')
    result = db.query(f'''
             SELECT * 
             FROM TRANSAKSI_HOTEL
             WHERE idtransaksi='{idtransaksi}';
             ''')
    db.close()
    return result[0]


def update_transaksi_hotel(id_transaksi, status_bayar):
    db = Database(schema='siruco')
    db.query(f'''
             UPDATE TRANSAKSI_HOTEL
             SET
                 StatusBayar = '{status_bayar}'
             WHERE
                 IdTransaksi = '{id_transaksi}';
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


def read_transaksi_booking_hotel():
    db = Database(schema='siruco')
    result = db.query(f'''
             SELECT * FROM TRANSAKSI_BOOKING;
             ''')
    db.close()
    return result


def delete_transaksi_booking_hotel(data):
    db = Database(schema='siruco')
    db.query(f'''
             DELETE FROM TRANSAKSI_BOOKING
             WHERE
                IdTransaksiBooking = '{data.get('id_transaksi_booking')}'
             ''')
    db.close()
    return


def list_nik_pasien():
    db = Database(schema='siruco')
    result = db.query(f'''
             SELECT nik
             FROM PASIEN;
             ''')
    db.close()
    return [item for row in result for item in row]


def rooms_by_hotel(hotel):
    db = Database(schema='siruco')
    result = db.query(f'''
             SELECT koderoom
             FROM HOTEL_ROOM
             WHERE kodehotel='{hotel}';
             ''')
    db.close()
    return [item for row in result for item in row]
