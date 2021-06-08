from django.apps import AppConfig
from siruco.db import Database
from dotenv import load_dotenv
from os import getenv

class MainConfig(AppConfig):
    name = 'main'
    
    def ready(self):
        load_dotenv()
        if getenv("DATABASE_URL") == None:
          print("Still configuring...")
        else:
            db = Database(schema="siruco")
            # Screate schema
            db.query("""
                    CREATE TABLE IF NOT EXISTS AKUN_PENGGUNA (
                        Username VARCHAR(50),
                        Password VARCHAR(20) NOT NULL,
                        Peran VARCHAR(20) NOT NULL,
                        PRIMARY KEY (Username)
                    );
                    
                    CREATE TABLE IF NOT EXISTS ADMIN (
                        Username VARCHAR(50),
                        PRIMARY KEY (Username),
                        FOREIGN KEY (Username) REFERENCES AKUN_PENGGUNA(Username) ON UPDATE CASCADE ON DELETE CASCADE 
                    );
                    
                    CREATE TABLE IF NOT EXISTS PENGGUNA_PUBLIK (
                        Username VARCHAR(50),
                        NIK VARCHAR(20) NOT NULL,
                        Nama VARCHAR(50) NOT NULL,
                        Status VARCHAR(10) NOT NULL,
                        Peran VARCHAR(20) NOT NULL,
                        NoHP VARCHAR(12) NOT NULL,
                        PRIMARY KEY (Username),
                        FOREIGN KEY (Username) REFERENCES AKUN_PENGGUNA(Username) ON UPDATE CASCADE ON DELETE CASCADE 
                    );
                    
                    CREATE TABLE IF NOT EXISTS PASIEN (
                        NIK VARCHAR(20),
                        IdPendaftar VARCHAR(50),
                        Nama VARCHAR(50) NOT NULL,
                        KTP_jalan VARCHAR(30) NOT NULL,
                        KTP_Kelurahan VARCHAR(30) NOT NULL,
                        KTP_Kecamatan VARCHAR(30) NOT NULL,
                        KTP_KabKot VARCHAR(30) NOT NULL,
                        KTP_Prov VARCHAR(30) NOT NULL,
                        Dom_jalan VARCHAR(30) NOT NULL,
                        Dom_Kelurahan VARCHAR(30) NOT NULL,
                        Dom_Kecamatan VARCHAR(30) NOT NULL,
                        Dom_KabKot VARCHAR(30) NOT NULL,
                        Dom_Prov VARCHAR(30) NOT NULL,
                        NoTelp VARCHAR(20) NOT NULL,
                        NoHP VARCHAR(12) NOT NULL,
                        PRIMARY KEY (NIK),
                        FOREIGN KEY (IdPendaftar) REFERENCES PENGGUNA_PUBLIK(Username) ON UPDATE CASCADE ON DELETE CASCADE 
                    );
                    
                    CREATE TABLE IF NOT EXISTS TES (
                        NIK_pasien VARCHAR(20),
                        TanggalTes DATE,
                        Jenis VARCHAR(10) NOT NULL,
                        Status VARCHAR(15) NOT NULL,
                        NilaiCT VARCHAR(5),
                        PRIMARY KEY (NIK_pasien, TanggalTes),
                        FOREIGN KEY (NIK_pasien) REFERENCES PASIEN(NIK) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS DOKTER (
                        Username VARCHAR(50),
                        NoSTR VARCHAR(20),
                        Nama VARCHAR(50) NOT NULL,
                        NoHp VARCHAR(12) NOT NULL, 
                        GelarDepan VARCHAR(10) NOT NULL,
                        GelarBelakang VARCHAR(10) NOT NULL,
                        PRIMARY KEY (Username, NoSTR),
                        FOREIGN KEY (Username) REFERENCES ADMIN(Username) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS FASKES (
                        Kode VARCHAR(3),
                        Tipe VARCHAR(30) NOT NULL,
                        Nama VARCHAR(50) NOT NULL,
                        StatusMilik VARCHAR(30) NOT NULL,
                        Jalan VARCHAR(30) NOT NULL,
                        Kelurahan VARCHAR(30) NOT NULL,
                        Kecamatan VARCHAR(30) NOT NULL,
                        KabKot VARCHAR(30) NOT NULL,
                        Prov VARCHAR(30) NOT NULL,
                        PRIMARY KEY (Kode)
                    );
                    
                    CREATE TABLE IF NOT EXISTS ADMIN_SATGAS (
                        Username VARCHAR(50),
                        IdFaskes VARCHAR(3),
                        PRIMARY KEY (Username),
                        FOREIGN KEY (Username) REFERENCES ADMIN(Username) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (IdFaskes) REFERENCES FASKES(Kode) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS JADWAL (
                        Kode_Faskes VARCHAR(3),
                        Shift VARCHAR(15),
                        Tanggal DATE,
                        PRIMARY KEY (Kode_Faskes, Shift, Tanggal),
                        FOREIGN KEY (Kode_Faskes) REFERENCES FASKES(Kode) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS JADWAL_DOKTER (
                        NoSTR VARCHAR(20),
                        Username VARCHAR(50),
                        Kode_Faskes VARCHAR(3),
                        Shift VARCHAR(15),
                        Tanggal DATE,
                        JmlPasien INT,
                        PRIMARY KEY (NoSTR, Username, Kode_Faskes, Shift, Tanggal),
                        FOREIGN KEY (NoSTR, Username) REFERENCES DOKTER(NoSTR, Username) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (Kode_Faskes, Shift, Tanggal) REFERENCES JADWAL(Kode_Faskes, Shift, Tanggal) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS MEMERIKSA (
                        NIK_Pasien VARCHAR(20),
                        NoSTR VARCHAR(20),
                        Username_Dokter VARCHAR(50),
                        Kode_Faskes VARCHAR(3),
                        Praktek_Shift VARCHAR(15),
                        Praktek_Tgl DATE,
                        Rekomendasi VARCHAR(500),
                        PRIMARY KEY (NIK_Pasien, NoSTR, Username_Dokter, Kode_Faskes, Praktek_Shift, Praktek_Tgl),
                        FOREIGN KEY (NoSTR, Username_Dokter, Kode_Faskes, Praktek_Shift, Praktek_Tgl) REFERENCES JADWAL_DOKTER(NoSTR, Username, Kode_Faskes, Shift, Tanggal) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (NIK_Pasien) REFERENCES PASIEN(NIK) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS RUMAH_SAKIT (
                        Kode_Faskes VARCHAR(3) NOT NULL,
                        IsRujukan CHAR(1) NOT NULL,
                        PRIMARY KEY (Kode_Faskes),
                        FOREIGN KEY (Kode_Faskes) REFERENCES FASKES(Kode) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS RUANGAN_RS (
                        KodeRS VARCHAR(3) NOT NULL,
                        KodeRuangan VARCHAR(5) NOT NULL,
                        Tipe VARCHAR(10) NOT NULL,
                        JmlBed INT NOT NULL,
                        Harga INT NOT NULL,
                        PRIMARY KEY (KodeRS, KodeRuangan),
                        FOREIGN KEY (KodeRS) REFERENCES RUMAH_SAKIT(Kode_Faskes) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS BED_RS (
                        KodeRuangan VARCHAR(5) NOT NULL,
                        KodeRS VARCHAR(3) NOT NULL,
                        KodeBed VARCHAR(5) NOT NULL,
                        PRIMARY KEY (KodeRuangan, KodeRS, KodeBed),
                        FOREIGN KEY (KodeRS, KodeRuangan) REFERENCES RUANGAN_RS(KodeRS, KodeRuangan) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS RESERVASI_RS (
                        KodePasien VARCHAR(20) NOT NULL,
                        TglMasuk DATE NOT NULL,
                        TglKeluar DATE NOT NULL,
                        KodeRS VARCHAR(3),
                        KodeRuangan VARCHAR(5),
                        KodeBed VARCHAR(5),
                        PRIMARY KEY (KodePasien, TglMasuk),
                        FOREIGN KEY (KodePasien) REFERENCES PASIEN(NIK) ON UPDATE CASCADE ON DELETE CASCADE,    
                        FOREIGN KEY (KodeRuangan, KodeRS, KodeBed) REFERENCES BED_RS(KodeRuangan, KodeRS, KodeBed) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    
                    CREATE TABLE IF NOT EXISTS TRANSAKSI_RS (
                        IdTransaksi VARCHAR(10) NOT NULL,
                        KodePasien VARCHAR(20),
                        TanggalPembayaran DATE,
                        WaktuPembayaran TIMESTAMP,
                        TglMasuk DATE,
                        TotalBiaya INT,
                        StatusBayar VARCHAR(15) NOT NULL,
                        PRIMARY KEY (IdTransaksi),
                        FOREIGN KEY (KodePasien, TglMasuk) REFERENCES RESERVASI_RS(KodePasien, TglMasuk) ON UPDATE CASCADE ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS HOTEL (
                        Kode VARCHAR(5) NOT NULL,
                        Nama VARCHAR(30) NOT NULL,
                        IsRujukan CHAR(1) NOT NULL, -- 1 denotes rujukan, 0 denotes non-rujukan
                        Jalan VARCHAR(30) NOT NULL,
                        Kelurahan VARCHAR(30) NOT NULL,
                        Kecamatan VARCHAR(30) NOT NULL,
                        KabKot VARCHAR(30) NOT NULL,
                        Prov VARCHAR(30) NOT NULL,
                        PRIMARY KEY (Kode)
                    );

                    CREATE TABLE IF NOT EXISTS HOTEL_ROOM (
                        KodeHotel VARCHAR(5) NOT NULL,
                        KodeRoom VARCHAR(5) NOT NULL,
                        JenisBed VARCHAR(10) NOT NULL,
                        Tipe VARCHAR(10) NOT NULL,
                        Harga INT NOT NULL,
                        PRIMARY KEY (KodeHotel, KodeRoom),
                        FOREIGN KEY (KodeHotel) REFERENCES HOTEL(Kode) ON UPDATE CASCADE ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS PAKET_MAKAN (
                        KodeHotel VARCHAR(5) NOT NULL,
                        KodePaket VARCHAR(5) NOT NULL,
                        Nama VARCHAR(20) NOT NULL,
                        Harga INT NOT NULL,
                        PRIMARY KEY (KodeHotel, KodePaket),
                        FOREIGN KEY (KodeHotel) REFERENCES HOTEL(Kode) ON UPDATE CASCADE ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS RESERVASI_HOTEL (
                        KodePasien VARCHAR(20) NOT NULL,
                        TglMasuk DATE NOT NULL,
                        TglKeluar DATE NOT NULL,
                        KodeHotel VARCHAR(5),
                        KodeRoom VARCHAR(5),
                        PRIMARY KEY (KodePasien, TglMasuk),
                        FOREIGN KEY (KodePasien) REFERENCES PASIEN(NIK) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (KodeHotel, KodeRoom) REFERENCES HOTEL_ROOM(KodeHotel, KodeRoom) ON UPDATE CASCADE ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS TRANSAKSI_HOTEL (
                        IdTransaksi VARCHAR(10) NOT NULL,
                        KodePasien VARCHAR(20),
                        TanggalPembayaran DATE,
                        WaktuPembayaran TIMESTAMP,
                        TotalBayar INT,
                        StatusBayar VARCHAR(15) NOT NULL,
                        PRIMARY KEY (IdTransaksi),
                        FOREIGN KEY (KodePasien) REFERENCES PASIEN(NIK) ON UPDATE CASCADE ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS TRANSAKSI_BOOKING (
                        IdTransaksiBooking VARCHAR(10) NOT NULL,
                        TotalBayar INT,
                        KodePasien VARCHAR(20),
                        TglMasuk DATE,
                        PRIMARY KEY (IdTransaksiBooking),
                        FOREIGN KEY (IdTransaksiBooking) REFERENCES TRANSAKSI_HOTEL(IdTransaksi) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (KodePasien, TglMasuk) REFERENCES RESERVASI_HOTEL(KodePasien,TglMasuk) ON UPDATE CASCADE ON DELETE CASCADE
                    );

                    CREATE TABLE IF NOT EXISTS TRANSAKSI_MAKAN (
                        IdTransaksi VARCHAR(10) NOT NULL,
                        IdTransaksiMakan VARCHAR(10) NOT NULL,
                        TotalBayar INT,
                        PRIMARY KEY (IdTransaksi, IdTransaksiMakan),
                        FOREIGN KEY (IdTransaksi) REFERENCES TRANSAKSI_HOTEL(IdTransaksi) ON UPDATE CASCADE ON DELETE CASCADE
                    );

                    -- ini paling bawah ---------------------------

                    -- auto increment pake sequence
                    CREATE SEQUENCE IF NOT EXISTS id_daftar_pesan;
                    CREATE TABLE IF NOT EXISTS DAFTAR_PESAN (
                        id_transaksi VARCHAR(10) NOT NULL,
                        IdTransaksiMakan VARCHAR(10) NOT NULL,
                        KodeHotel VARCHAR(5),
                        KodePaket VARCHAR(5),
                        id_pesanan INT NOT NULL DEFAULT nextval('id_daftar_pesan'),
                        PRIMARY KEY (id_transaksi, IdTransaksiMakan, id_pesanan),
                        FOREIGN KEY (id_transaksi, IdTransaksiMakan) REFERENCES TRANSAKSI_MAKAN(IdTransaksi, IdTransaksiMakan) 
                        ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (KodeHotel, KodePaket) REFERENCES PAKET_MAKAN(KodeHotel, KodePaket) ON UPDATE CASCADE ON DELETE CASCADE
                    );
                    """)
            db.close()
