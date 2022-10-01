from time import strftime
import os
from django.utils.http import is_safe_url, urlunquote
from django.template.context_processors import csrf
from .forms import UserLoginForm


def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = UserLoginForm
    return context


def get_next_url(request):
    nnext = request.GET.get('next')
    if nnext:
        nnext = urlunquote(nnext)  # HTTP_REFERER may be encoded.
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
        return "night"
    return "day"


def mult_error(id):
    error_text = ["Попросила Спайка найти, но ничего  не нашлось",
                  "К сожалению библиотека пуста",
                  "Неправильные параметры сортировки",
                  "В нашей библиотеке такого нет"]
    return {"mult_error": f"{error_text[id]}"}

