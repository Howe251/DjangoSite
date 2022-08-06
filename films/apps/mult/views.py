import os

import requests
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from .models import Mult, Series, Film, Subs, Audio
from django.core.paginator import Paginator
from itertools import chain
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .forms import ListForm
from time import strftime

h = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache"
            }


def get_time():
    time = int(strftime("%H"))
    if time > 20 or 0 <= time < 8:
        night = "night"
    else:
        night = "day"
    return night


def mainpage(request):
    night = get_time()
    return render(request, 'main.html', {"night": night})


def mult_error(id):
    error_text = ["Попросила Спайка найти, но ничего  не нашлось",
                  "К сожалению библиотека пуста",
                  "Неправильные параметры сортировки",
                  "В нашей библиотеке такого нет"]
    return {"mult_error": f"{error_text[id]}"}


def film_list(request):
    night = get_time()
    films_lt = Film.objects.filter(isShown=True).order_by('name')
    if not films_lt:
        raise Http404(mult_error(1))
    for film in films_lt:
        if film.img_url != "None" and film.isShown:
            if (film.img_url and film.img_url != "Нет данных") and not film.img:
                FileDelete("films", film.id)
                result = requests.get(film.img_url, headers=h)
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(result.content)
                img_temp.flush()
                film.img.save(str(film.id)+".jpg", File(img_temp))
                film.save()

    return render(request, 'film/film_list.html', {'films_lt': films_lt,
                                                   'night': night})


def film_detail(request, film_id):
    try:
        a = Film.objects.get(id=film_id)
        series_list = a.seriesfilms_set.order_by('name_serie')
        night = get_time()
    except:
        raise Http404(mult_error(3))
    return render(request, 'film/film_detail.html', {'film': a,
                                                     'series_list': series_list,
                                                     'night': night})


def search(request):
    search_querry = request.GET.get('q', '')
    mults_lt = Mult.objects.filter(name__icontains=search_querry)
    films_lt = Film.objects.filter(name__icontains=search_querry)
    mult_genre_lt = Mult.objects.filter(genre__name=search_querry)
    film_genre_lt = Film.objects.filter(genre__name=search_querry)
    querysets = list(chain(mults_lt, films_lt, mult_genre_lt, film_genre_lt))
    night = get_time()
    if not querysets:
        raise Http404(mult_error(0))
    return render(request, 'film/film_list.html', {'films_lt': querysets,
                                                   'night': night})


def mult_list(request):
    mults_lt = Mult.objects.filter(isShown=True)
    if not mults_lt:
        raise Http404(mult_error(1))
    forms = {'ordering': request.GET.get('ordering'), 'genre': request.GET.get('genre')}
    form = ListForm(request.POST)
    formP = form.as_p()
    if request.method == "POST":
        if form.is_valid():
            if form.cleaned_data["ordering"]:
                forms['ordering'] = form.cleaned_data["ordering"]
                mults_lt = mults_lt.order_by(form.cleaned_data["ordering"])
            if form.cleaned_data["genre"]:
                forms['genre'] = form.cleaned_data["genre"].id
                mults_lt = mults_lt.filter(genre=form.cleaned_data["genre"].id)
    elif forms['ordering'] is not None or forms['genre'] is not None:
        if forms['genre']:
            if forms['genre'] in [str(choice[0]) for choice in form.fields['genre'].choices]:
                mults_lt = mults_lt.filter(genre=forms['genre'])
                formP = formP[0:formP.rfind("selected")-1] + formP[formP.rfind("selected") +
                            len("selected"):formP.rfind(f'''value="{forms['genre']}"''') +
                            len(f'''value="{forms['genre']}"''')] + " selected" + \
                            formP[formP.rfind(f'''value="{forms['genre']}"''') + len(f'''value="{forms['genre']}"''')::]
            else:
                raise Http404(mult_error(1))
        if forms['ordering']:
            if forms['ordering'] in [str(choice.data['value']) for choice in form.visible_fields()[0]]:
                mults_lt = mults_lt.order_by(forms['ordering'])
                formP = formP[0:formP.find(forms['ordering']) + len(forms['ordering'])+1] + " selected" + \
                        formP[formP.find(forms['ordering']) + len(forms['ordering'])+1::]
            else:
                raise Http404(mult_error(1))

    for mult in mults_lt:
        if mult.img_url != "None" and mult.isShown:
            if mult.img_url and not mult.img:
                FileDelete("mults", mult.id)
                h = {
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "cross-site",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache"
                }
                result = requests.get(mult.img_url, headers=h)
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(result.content)
                img_temp.flush()
                mult.img.save(str(mult.id)+".jpg", File(img_temp))
                mult.save()
    paginator = Paginator(mults_lt, 16)

    page_number = request.GET.get('p', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = f"p={page.previous_page_number()}"
        prev_url += f"&ordering={forms['ordering']}" if forms['ordering'] else ""
        prev_url += f"&genre={forms['genre']}" if forms['genre'] else ""
    else:
        prev_url = ""

    if page.has_next():
        next_url = f"p={page.next_page_number()}"
        next_url += f"&ordering={forms['ordering']}" if forms['ordering'] else ""
        next_url += f"&genre={forms['genre']}" if forms['genre'] else ""
    else:
        next_url = ""
    night = get_time()
    context = {
        'mults_lt': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'formP': formP,
        'ordering': forms,
        'night': night
    }
    return render(request, 'mult/list.html', context=context)


def FileDelete(path, id):
    try:
        os.remove(os.path.join(os.path.abspath(os.curdir), "media/images", path, str(id)+".jpg"))
    except FileNotFoundError:
        print()


def DetailedView(request, mult_id):
    try:
        a = Mult.objects.get(id=mult_id)
        series_list = Series.objects.filter(name_id=a.id).order_by('full_name')
        subs = Subs.objects.filter(mult_id=a.id)
        sounds = Audio.objects.filter(mult_id=a.id)
        night = get_time()
    except:
        raise Http404(mult_error(3))
    return render(request, 'mult/detail.html', {'mult': a,
                                                'series_list': series_list,
                                                'subs': subs,
                                                'sounds': sounds,
                                                'night': night})


def page_not_found_view(request, exception):
    night = get_time()
    if "mult_error" in exception.args[0]:
        return render(request, '404/index.html', {'night': night, 'error': exception.args[0]['mult_error']})
    return render(request, '404/index.html', {'night': night, 'error': mult_error(3)['mult_error']})
