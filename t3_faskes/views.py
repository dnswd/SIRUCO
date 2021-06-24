from django.shortcuts import render, redirect
from siruco.db import Database
from django.http import HttpResponse
from datetime import date, datetime
from django.contrib import messages
import json

def reservasi(request):
	response = {}
	peran = session(request, 'peran')
	if peran == "admin_satgas": # read all reservasi
		isAdminSatgas = True
		reservasilist = get_reservasi()
	elif peran == "pengguna_publik": # read only its reservasi
		isAdminSatgas = False
		username = session(request, 'username')
		reservasilist = get_reservasi_by_user(username)
	else:
		return redirect('/')

	response['reservasilist'] = reservasilist
	response['isAdminSatgas'] = isAdminSatgas
	return render(request, 'reservasi.html', response)

def reservasi_create(request): #handle tanggal masuk keluar
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')

	if (request.method == 'GET'):
		response = {}
		response['pasienlist'] = get_nik_pasien()
		response['rslist'] = get_kode_rs()
		return render(request, 'reservasi_create.html', response)
	else :
		rep = request.POST
		if (rep.get('tgl_masuk') >= rep.get('tgl_keluar')):
			messages.error(request, "Tanggal Keluar harus lebih lama dari Tanggal Masuk ❗")
			response = {}
			response['pasienlist'] = get_nik_pasien()
			response['rslist'] = get_kode_rs()
			return render(request, 'reservasi_create.html', response)

		# print(rep.get('tgl_masuk'))
		# print(rep.get('tgl_keluar'))
		db = Database(schema='siruco')
		db.query(f'''
				INSERT INTO RESERVASI_RS VALUES
				('{rep.get('nik')}', 
				'{rep.get('tgl_masuk')}', 
				'{rep.get('tgl_keluar')}', 
				'{rep.get('kode_rs')}', 
				'{rep.get('kode_ruangan')}', 
				'{rep.get('kode_bed')}');
				''')
		db.close()
		return redirect('/faskes/reservasi/')

def reservasi_update(request, pk): #handle tanggal masuk keluar
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')
	
	nik = pk[:-8]
	tglmasuk = pk[-4:] + '-' + pk[-6:-4] + '-' + pk[-8:-6]
	if (request.method == 'GET'):
		response = {}
		response['reservasi'] = get_reservasi_by_nik_and_tgl(nik, tglmasuk)
		return  render(request, 'reservasi_update.html', response)
	
	else :
		rep = request.POST

		if (datetime.strptime(tglmasuk, "%Y-%m-%d") >= datetime.strptime(rep.get('tgl_keluar'), "%Y-%m-%d")):
			messages.error(request, "Tanggal Keluar harus lebih lama dari Tanggal Masuk ❗")
			response = {}
			response['reservasi'] = get_reservasi_by_nik_and_tgl(nik, tglmasuk)
			return  render(request, 'reservasi_update.html', response)

		# print(rep.get('tgl_keluar'))
		db = Database(schema='siruco')
		db.query(f'''
				UPDATE RESERVASI_RS
				SET tglkeluar='{rep.get('tgl_keluar')}'
				WHERE kodepasien='{nik}'
				and tglmasuk='{tglmasuk}';
				''')
		db.close()
		return redirect('/faskes/reservasi/')

def reservasi_delete(request, pk): #handle belum tanggal masuk
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')
	nik = pk[:-8]
	tglmasuk = pk[-4:] + pk[-6:-4] + pk[-8:-6]
	if datetime.today() < datetime.strptime(tglmasuk, "%Y%m%d"):
		db = Database(schema='siruco')
		db.query(f'''
				DELETE FROM RESERVASI_RS
				WHERE kodepasien='{nik}'
				and tglmasuk='{tglmasuk}';
				''')
		db.close()

	return redirect('/faskes/reservasi/')

def faskes(request):
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')
	response = {}
	response['faskeslist'] = get_faskes()
	return render(request, 'faskes.html', response)

def faskes_detail(request, pk):
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')

	response = {}
	response['faskes'] = get_faskes_by_kode(pk)
	return render(request, 'faskes_detail.html', response)

def faskes_create(request):
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')

	if (request.method == 'GET'):
		response = {}
		#generate new kode faskes
		faskeslist =  get_faskes()
		newid = 0
		for faskes in faskeslist :
			oldid = int(faskes['kode'][2:])
			if (oldid > newid):
				newid = oldid
		newkode = 'FK' + str(newid + 1)
		response['newkode'] = newkode
		return  render(request, 'faskes_create.html', response)
	else :
		rep = request.POST
		db = Database(schema='siruco')
		db.query(f'''
				INSERT INTO FASKES VALUES
				('{rep.get('kode')}', 
				'{rep.get('tipe')}', 
				'{rep.get('nama')}', 
				'{rep.get('statusmilik')}', 
				'{rep.get('jalan')}', 
				'{rep.get('kelurahan')}',
				'{rep.get('kecamatan')}',
				'{rep.get('kabkot')}',
				'{rep.get('prov')}');
				''')
		db.close()
		return redirect('/faskes/')

def faskes_update(request, pk):
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')

	if (request.method == 'GET'):
		response = {}
		response['faskes'] = get_faskes_by_kode(pk)
		return  render(request, 'faskes_update.html', response)
	
	else :
		rep = request.POST
		db = Database(schema='siruco')
		db.query(f'''
				UPDATE FASKES
				SET tipe='{rep.get('tipe')}',
				nama='{rep.get('nama')}',
				statusmilik='{rep.get('statusmilik')}',
				jalan='{rep.get('jalan')}',
				kelurahan='{rep.get('kelurahan')}',
				kecamatan='{rep.get('kecamatan')}',
				kabkot='{rep.get('kabkot')}',
				prov='{rep.get('prov')}'
				WHERE kode='{pk}';
				''')
		db.close()
		return redirect('/faskes/')

def faskes_delete(request, pk):
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')

	db = Database(schema='siruco')
	db.query(f'''
			DELETE FROM FASKES
			WHERE kode='{pk}';
			''')
	db.close()
	return redirect('/faskes/')

# api views
def reservasi_ruangan_api(request, koders):
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')
	ruanganlist = get_koderuangan_by_koders(koders)
	data_list = json.dumps(ruanganlist)
	return HttpResponse(data_list, content_type="text/json-comment-filtered")

def reservasi_bed_api(request, koders, koderuangan):
	peran = session(request, 'peran')
	if peran != "admin_satgas":
		return redirect('/')
	bedlist = get_kodebed_by_koders_koderuangan(koders, koderuangan)
	data_list = json.dumps(bedlist)
	return HttpResponse(data_list, content_type="text/json-comment-filtered")

# Helper Functions
def get_faskes():
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT * FROM FASKES;
		''')
	db.close()
	result = [{
		"kode": query[r][0],
		"tipe": query[r][1],
		"nama": query[r][2],
		"statusmilik": query[r][3],
		"jalan": query[r][4],
		"kelurahan": query[r][5],
		"kecamatan": query[r][6],
		"kabkot": query[r][7],
		"prov": query[r][8],
		} for r in range(len(query))
	]
	# print(result)
	return result

def get_faskes_by_kode(kode):
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT * FROM FASKES
		WHERE kode='{kode}';
		''')
	db.close()
	result = {
		"kode": query[0][0],
		"tipe": query[0][1],
		"nama": query[0][2],
		"statusmilik": query[0][3],
		"jalan": query[0][4],
		"kelurahan": query[0][5],
		"kecamatan": query[0][6],
		"kabkot": query[0][7],
		"prov": query[0][8],
		}
	# print(result)
	return result

def get_reservasi():
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT * FROM RESERVASI_RS;
		''')
	db.close()
	result = [{
		"nik": query[r][0],
		"tglmsk": query[r][1],
		"tglklr": query[r][2],
		"koders": query[r][3],
		"koderuang": query[r][4],
		"kodebed": query[r][5],
		"idreservasi": (query[r][0] + query[r][1].strftime("%d%m%Y")),
		"isDue": False if date.today() < query[r][1] else True
		} for r in range(len(query))
	]
	# print(result)
	return result

def get_reservasi_by_nik_and_tgl(nik, tgl_masuk):
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT * FROM RESERVASI_RS
		WHERE kodepasien='{nik}' and tglmasuk='{tgl_masuk}';
		''')
	db.close()
	result = {
		"nik": query[0][0],
		"tglmsk": query[0][1],
		"tglklr": query[0][2],
		"koders": query[0][3],
		"koderuang": query[0][4],
		"kodebed": query[0][5],
		"idreservasi": (query[0][0] + query[0][1].strftime("%d%m%Y")),
		}
	# print(result)
	return result

def get_reservasi_by_user(username):
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT kodepasien, tglmasuk, tglkeluar, koders, koderuangan, kodebed
		FROM RESERVASI_RS R
		JOIN PASIEN P ON P.nik=R.kodepasien
		JOIN PENGGUNA_PUBLIK PP ON P.idpendaftar=PP.username
		WHERE PP.username='{username}';
		''')
	db.close()
	result = [{
		"nik": query[r][0],
		"tglmsk": query[r][1],
		"tglklr": query[r][2],
		"koders": query[r][3],
		"koderuang": query[r][4],
		"kodebed": query[r][5],
		"idreservasi": (query[r][0] + query[r][1].strftime("%d%m%Y")),
		} for r in range(len(query))
	]
	# print(result)
	return result

def get_nik_pasien():
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT nik FROM PASIEN;
		''')
	db.close()
	result = []
	for item in query:
	    result.append(item[0])
	# print(result)
	return result

def get_kode_rs():
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT kode_faskes FROM RUMAH_SAKIT;
		''')
	db.close()
	result = []
	for item in query:
	    result.append(item[0])
	# print(result)
	return result

def get_koderuangan_by_koders(koders):
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT koderuangan FROM RUANGAN_RS
		WHERE koders='{koders}';
		''')
	db.close()
	result = []
	for item in query:
	    result.append(item[0])
	# print(result)
	return result

def get_kodebed_by_koders_koderuangan(koders, koderuangan):
	db = Database(schema='siruco')
	query = db.query(f'''
		SELECT kodebed FROM BED_RS
		WHERE koders='{koders}'
		and koderuangan='{koderuangan}';
		''')
	db.close()
	result = []
	for item in query:
	    result.append(item[0])
	# print(result)
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