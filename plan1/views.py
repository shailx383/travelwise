from django.shortcuts import render
from plan1.models import s1  # tables which contain choices of users
from plan1.models import s2
from plan1.models import s3
from plan1.models import s4
from django import forms


# Create your views here.
def plan_1(request):
    if request.method == 'GET':
        return render(request, 'mainpage.html')  # directs user to first planning page
    elif request.method == 'POST':
        u = request.user  # instance of currently logged in user
        pp = request.POST['people']  # number of people
        t = request.POST['type']  # scheduling
        city = request.POST['city']  # city of residence
        country = request.POST['country']  # country of residence
        if request.GET['a'] == 's1':
            a = s1()
            a.user = u
            a.people = pp
            a.type = t
            a.city = city
            a.country = country
            a.save()
            return render(request, 'plan2.html')
        else:
            return render('login_error.html')


def plan_2(request):
    if request.method == 'GET':
        return render(request, 'plan2.html')  # directs user to second planning page
    elif request.method == 'POST':
        u = request.user  # instance of currently logged in user
        w = request.POST.get('weather')  # preferred weather
        s_d = request.POST.get('start_date')  # start date of trip
        bud = request.POST.get('budget')  # budget range
        if request.GET['b'] == 's2':
            b = s2()
            b.user = u
            b.weather = w
            b.start_date = s_d
            b.budget = bud
            b.save()
            val = s1.objects.get(user_id=request.user.id)
            return render(request, 'plan3.html', {'val': val})
        else:
            return render(request, 'login_error.html')


def plan_3(request):
    if request.method == 'GET':
        return render(request, 'plan3.html')  # directs user to third planning page
    elif request.method == 'POST':
        u = request.user  # instance of currently logged in user
        t = request.POST.getlist('type')  # list of attraction types preferred by user
        type = ''
        for i in t:
            type += i  # converting list to string to store in database
        x = s1.objects.get(user_id=request.user.id)
        val = x.people
        if val == 'fami':  # asks for number of people if 'family' option is selected 
            rooms = request.POST.get('rooms')  # number of rooms
            ppl = request.POST.get('ppl')  # number of people
        elif val == 'coup':
            rooms = 1
            ppl = 2
        else:
            rooms = 1
            ppl = 1
        if request.GET['b'] == 's3':
            b = s3()
            b.user = u
            b.rooms = rooms
            b.ppl = ppl
            b.type = type
            b.save()
            return render(request, 'plan4.html')
        else:
            return render(request, 'login_error.html')


def plan_4(request):
    if request.method == 'GET':
        return render(request, 'plan4.html')  # directs user to fourth planning page
    elif request.method == 'POST':
        u = request.user  # instance of currently logged in user
        t2 = request.POST.getlist('tran')  # list of transportation types (between cities)
        tran = ''
        for j in t2:
            tran += j
        if request.GET['b'] == 's4':
            b = s4()
            b.user = u
            b.tran = tran
            b.save()
            return render(request, 'int.html')
        else:
            return render(request, 'login_error.html')


# Classes for datepickers
class Date_Input(forms.DateInput):
    input_type = "date"


class form1(forms.Form):
    start_date = forms.DateField(widget=Date_Input)
    end_date = forms.DateField(widget=Date_Input)
