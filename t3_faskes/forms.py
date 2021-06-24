# from django import forms
# from siruco.db import Database


# def get_nik_pasien():
# 	db = Database(schema='siruco')
# 	kode = db.query(f'''
# 	SELECT nik FROM PASIEN;
# 	''')
# 	db.close()
# 	result = []
# 	for item in kode:
# 	    result.append(item[0])
# 	# print(result)
# 	return result

# pasienlist = get_nik_pasien()

# # form_class: str = 'form-control mr-sm-2'
# # class LoginForm(forms.Form):
# #     username = forms.CharField(widget=forms.TextInput(attrs={
# #     'class': form_class,
# #     "placeholder" : "Username"
# #     }))
# #     password = forms.CharField(widget=forms.PasswordInput(attrs={
# #     'class': form_class,
# #     "placeholder" : "Password",
# #     "type" : "password"
# #     }))

# class ReservasiRSForm(forms.Form):
#     nik = forms.ChoiceField(label="nik", choices=pasienlist, 
#     	widget = forms.Select(attrs={'class':'form-control'} ))

#     tgl_masuk = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     tgl_keluar = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
#     kode_rs = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     kode_ruangan = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
#     kode_bed = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))