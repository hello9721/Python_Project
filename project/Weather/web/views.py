from django.shortcuts import render
from .models import *
from .API_TO_DB import *
from .LOC_TO_XY import *

def test(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context = {'list' : ip}

    return render(request, 'test/index.html', context)

def home(request):

    c1 = Location.objects.values('one')

    Rc1 = []
    Rc2 = []
    Rc3 = []

    cst = ['vFcst', 'sFcst', 'sNcst']

    for i in c1:

        if i not in Rc1: Rc1.append(i)

    if request.GET == {}:

        address = ''

        for i in cst:
        
            temp, address = get_data(i, '')
            data_to_DB(temp, i)

        val = [address[0], address[1], address[2]]

    elif request.GET != {}:
        
        val = [request.GET.get('prev_one'), request.GET.get('prev_two'), request.GET.get('prev_thr')]

        if request.GET.get('one') != val[0]:

            get_one = request.GET.get('one')
            val[0] = get_one

            c2 = Location.objects.filter(one__contains=get_one).values('two')
            isRight = Location.objects.filter(one__contains=get_one).values(f'two = "{val[1]}"')

            print(isRight)

            if c2 == {}:
                
                val[1] = '=== 구 ==='
                val[2] = '=== 동 ==='

            else:

                for i in c2:
                    if i not in Rc2: Rc2.append(i)


        if request.GET.get('two') != val[1]:

            get_two = request.GET.get('two')
            val[1] = get_two

            c3 = Location.objects.filter(two__contains=get_two).values('thr')

            for i in c3:
                if i not in Rc3: Rc3.append(i)

        if request.GET.get('thr') != val[2]:

            get_thr = request.GET.get('thr')
            val[2] = get_thr

            for i in cst:
        
                temp, useless = get_data(i, get_thr)
                data_to_DB(temp, i)



    return render(request, "home/index.html", {"Rc1": Rc1, "Rc2": Rc2, "Rc3": Rc3, 'val' : val})