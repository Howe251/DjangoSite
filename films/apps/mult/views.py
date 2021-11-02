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
from .forms import SortForm


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


def mainpage(request):
    return render(request, 'main.html')


def film_list(request):
    films_lt = Film.objects.order_by('name')
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

    return render(request, 'film/film_list.html', {'films_lt': films_lt})


def film_detail(request, film_id):
    try:
        a = Film.objects.get(id=film_id)
        series_list = a.seriesfilms_set.order_by('name_serie')
    except:
        raise Http404("Фильм не найден")
    return render(request, 'film/film_detail.html', {'film': a,
                                                'series_list': series_list})


def search(request):
    search_querry = request.GET.get('q', '')
    mults_lt = Mult.objects.filter(name__icontains=search_querry)
    films_lt = Film.objects.filter(name__icontains=search_querry)
    querysets = list(chain(mults_lt, films_lt))
    return render(request, 'film/film_list.html', {'films_lt': querysets})


def mult_list(request):
    mults_lt = Mult.objects.all()
    ordering = request.GET.get('ordering')
    form = SortForm(request.POST, initial={"ordering": ["-name", "По убыванию"]})
    if form.is_valid() or ordering:
        if form.cleaned_data["ordering"]:
            ordering = form.cleaned_data["ordering"]
            mults_lt = mults_lt.order_by(form.cleaned_data["ordering"])
        elif ordering:
            if ordering in [choice[0] for choice in form.base_fields['ordering'].choices]:
                mults_lt = mults_lt.order_by(ordering)
            else:
                raise Http404("Неправильные параметры сортировки")
    formP = form.as_p()
    if ordering:
        if "selected" not in formP:
            formP = formP[0:formP.find(ordering) + len(ordering) + 1] + " selected" + formP[formP.find(ordering) +
            len(ordering) + 1::]
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
        prev_url = f"p={page.previous_page_number()}&ordering={ordering}" if ordering else f"p={page.previous_page_number()}"
    else:
        prev_url = ""

    if page.has_next():
        next_url = f"p={page.next_page_number()}&ordering={ordering}" if ordering else f"p={page.next_page_number()}"
    else:
        next_url = ""

    context = {
        'mults_lt': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'form': formP,
        'ordering': ordering
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
        #series_list = a.series_set.order_by('name_serie')
        series_list = Series.objects.filter(name_id=a.id)
        subs = Subs.objects.filter(mult_id=a.id)
        sounds = Audio.objects.filter(mult_id=a.id)
    except:
        raise Http404("Фильм не найден")
    return render(request, 'mult/detail.html', {'mult': a,
                                                'series_list': series_list,
                                                'subs': subs,
                                                'sounds': sounds})


def page_not_found_view(request, exception):
    return render(request, '404/index.html')

"""class DetailedView(View):
    def get(self, request, mult_id):
        try:
            a = Mult.objects.get(id=mult_id)
        except:
            raise Http404("Фильм не найден")

        return render(request, 'mult/film_detail.html', {'mult': a})"""



