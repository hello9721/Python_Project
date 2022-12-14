from django.shortcuts import render
from .models import *
from API_TO_DB import *
from LOC_TO_XY import *

def test(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context = {'list' : ip}

    return render(request, 'test/index.html', context)

def home(request):

    val = ['=== 시 ===', '=== 구 ===', '=== 동 ===']

    c1 = Location.objects.values('one')

    Rc1 = []
    Rc2 = []
    Rc3 = []

    get_thr = ''

    cst = ['vFcst', 'sFcst', 'sNcst']

    for i in c1:

        if i not in Rc1: Rc1.append(i)

    if request.GET != {}:

        if request.GET.get('one') != '=== 시 ===':

            get_one = request.GET.get('one')
            val[0] = get_one

            c2 = Location.objects.filter(one__contains=get_one).values('two')

            for i in c2:
                if i not in Rc2: Rc2.append(i)

        if request.GET.get('two') != '=== 구 ===':

            get_two = request.GET.get('two')
            val[1] = get_two

            c3 = Location.objects.filter(two__contains=get_two).values('thr')

            for i in c3:
                if i not in Rc3: Rc3.append(i)

        if request.GET.get('thr') != '=== 동 ===':

            get_thr = request.GET.get('thr')
            val[2] = get_thr

    for i in cst:
    
        temp = get_data(i, get_thr)
        data_to_DB(temp, i)

    return render(request, "home/index.html", {"Rc1": Rc1, "Rc2": Rc2, "Rc3": Rc3, 'val' : val})