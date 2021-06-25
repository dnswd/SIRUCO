from django.forms import Form, TextInput, NumberInput, ChoiceField, CharField


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
    Create HOTEL_ROOM Form
    """
    kode_hotel = CharField(disabled=True)
    kode_ruangan = CharField(widget=TextInput, disabled=True, required=False)
    jenis_bed = CharField(widget=TextInput, max_length=10)
    tipe = CharField(widget=TextInput, max_length=10)
    harga_per_hari = CharField(widget=NumberInput)
