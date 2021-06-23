from django.shortcuts import render


def home(request):
	isLogin = True if session(request, 'peran') else False
	response = { 'isLogin': isLogin }
	return render(request, 'main/home.html', response)

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