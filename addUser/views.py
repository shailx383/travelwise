from django.shortcuts import render
from django.contrib.auth.models import User as User_New
from django.contrib.auth import authenticate
from django.contrib.auth import login as log
import pickle


# Create your views here.
def index(request):  # directs to landing page
    return render(request, 'homepage.html')


def add_User(request):  # takes user info from the form and loads it into the database
    if request.method == 'GET':
        return render(request, 'add_user1.html')
    elif request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['passwd']
        email = request.POST['email']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        if request.GET['a'] == 'db':
            user = User_New.objects.create_user(username, email, passwd)  # creating the user
            user.first_name = f_name
            user.last_name = l_name
            user.save()
            return render(request, 'homepage.html')
        else:
            return render(request, 'homepage.html')


def login(request):  # authenticates the user, checks validity of credentials
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user = request.POST['username']
        pwd = request.POST['passwd']
        if request.GET['b'] == 'ck':
            user = authenticate(request, username=user, password=pwd)
            if user is not None:
                log(request, user)
                with open("itinerary_files.dat", "rb") as handle:
                    itinerary_list = []
                    while True:
                        try:
                            itinerary = pickle.load(handle)
                            if itinerary['id'] == request.user.id:
                                itinerary_list.append(itinerary)  # extracting user's previously planned itineraries
                            else:
                                pass
                        except EOFError:
                            break
                return render(request, 'itinlist.html',  # leads to home page or itinerary list
                              {'lst': itinerary_list, 'len': len(itinerary_list), 'logged_in': request.user.first_name})
            else:
                return render(request, 'login_error.html')  # error page
