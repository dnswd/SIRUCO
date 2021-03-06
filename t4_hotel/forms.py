from django.forms import Form, TextInput, NumberInput, ChoiceField, CharField, DateField, DateTimeField
from datetime import datetime, timedelta


class HotelRoomForm(Form):
    """
    Create HOTEL_ROOM Form
    """
    kode_hotel = ChoiceField(required=True)
    kode_ruangan = CharField(widget=TextInput, disabled=True, required=False)
    jenis_bed = CharField(widget=TextInput, max_length=10)
    tipe = CharField(widget=TextInput, max_length=10)
    harga_per_hari = CharField(widget=NumberInput)


class EditHotelRoomForm(Form):
    """
    Edit HOTEL_ROOM Form
    """
    kode_hotel = CharField(disabled=True)
    kode_ruangan = CharField(widget=TextInput, disabled=True, required=False)
    jenis_bed = CharField(widget=TextInput, max_length=10)
    tipe = CharField(widget=TextInput, max_length=10)
    harga_per_hari = CharField(widget=NumberInput)


class ReservationForm(Form):
    """
    Create HOTEL_RESERVATION Form
    """
    nik = ChoiceField()
    tgl_masuk = DateField(initial=datetime.today, required=True)
    tgl_keluar = DateField(
        initial=(datetime.today() + timedelta(days=12)), required=True)
    kode_hotel = ChoiceField()
    kode_ruangan = ChoiceField()


class EditReservationForm(Form):
    """
    Edit HOTEL_RESERVATION Form
    """
    nik = CharField(disabled=True)
    tgl_masuk = DateField(disabled=True)
    tgl_keluar = DateField(required=True)
    kode_hotel = CharField(disabled=True)
    kode_ruangan = CharField(disabled=True)


class EditTransactionForm(Form):
    """
    Edit HOTEL_TRANSACTION Form
    """
    nik = CharField(disabled=True)
    idtransaksi = CharField(disabled=True)
    tglbayar = DateField(disabled=True)
    wktbayar = DateTimeField(disabled=True)
    totalbiaya = DateField(disabled=True)
    statusbayar = CharField(required=True)
