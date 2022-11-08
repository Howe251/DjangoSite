from time import strftime
import os
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
import urllib
from django.template.context_processors import csrf
from .forms import UserLoginForm
from django.core.files.temp import NamedTemporaryFile


def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = UserLoginForm
    return context


def get_next_url(request):
    nnext = request.GET.get('next')
    if nnext:
        nnext = urllib.parse.unquote(nnext)  # HTTP_REFERER may be encoded.
    if not is_safe_url(url=nnext, allowed_hosts=request.get_host()):
        nnext = '/'
    return nnext


def FileDelete(path, id):
    try:
        os.remove(os.path.join(os.path.abspath(os.curdir), "media/images", path, str(id)+".jpg"))
    except FileNotFoundError:
        print()


def get_time():
    time = int(strftime("%H"))
    if time > 20 or 0 <= time < 8:
        return True
    return False


def mult_error(id):
    error_text = ["Попросила Спайка найти, но ничего  не нашлось",
                  "К сожалению библиотека пуста",
                  "Неправильные параметры сортировки",
                  "В нашей библиотеке такого нет"]
    return {"mult_error": f"{error_text[id]}"}


def handle_upload_file(f):
        img_temp = NamedTemporaryFile()
        for chunk in f.chunks():
                img_temp.write(chunk)
        img_temp.flush()
        return img_temp
