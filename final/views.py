from django.shortcuts import render
from plan1.models import s1
from plan1.models import s2
from plan1.models import s3
from plan1.models import s4
from plan1.models import attractions
from plan1.models import city
from final.models import acc
from final.models import transport
from final.models import flights
from utils import tip_funcs as tf
import os
import random
import datetime
import math
import pickle
import copy

# Create your views here.
countries_visited = []  # countries already visited by the user
country_false = []  # invalid countries: countries not preferred by the user
handler = open("itinerary_files.dat", "wb")  # creating the file used to store final itineraries
handler.close()


def show(request):
    if request.method == 'GET':
        logged_in = request.user
        val1 = s1.objects.get(user_id=request.user.id)  # retrieving inputs given by current user
        val2 = s2.objects.get(user_id=request.user.id)
        val3 = s3.objects.get(user_id=request.user.id)
        val4 = s4.objects.get(user_id=request.user.id)
        city_val = list(city.objects.values_list('city_name', 'country'))  # fetching all cities from database
        if (val1.city, val1.country) in city_val:
            country, flight_info, flightcost, flag = f1(val2, val3)  # feeding data to f1()
            city_info, cost1, last, new_Desc, ax = f2(val1, val2, val3, val4, country, flag)  # feeding data to f2()
            cit = list(city_info.keys())
            first = cit[0]  # first city visited
            COST = flightcost + cost1  # total cost of entire trip
            user_dict = {'id': request.user.id,  # creating dictionary to store in 'itinerary_files.dat'
                         'country': country,
                         'countryedit': country + '_edit',
                         'dict': city_info,
                         'new': new_Desc,
                         'ax': ax,
                         'cost': COST,
                         'f_info': flight_info,
                         'last': last
                         }
            handle = open("itinerary_files.dat", "ab")
            pickle.dump(user_dict, handle)  # dumping dict into file
            handle.close()
            return render(request, 'final.html', {'logged_in': logged_in,  # redirects to final itinerary page
                                                  'data1': val1,
                                                  'data2': val2,
                                                  'data3': val3,
                                                  'data4': val4,
                                                  'country': country,
                                                  'f_info': flight_info,
                                                  'info': city_info,
                                                  'first': first,
                                                  'last': last,
                                                  'cost': COST
                                                  }
                          )
        else:
            return render(request, 'city_error.html')


def f1(val2, val3):
    '''decides the country based on the weather
     and decides the flight details based on budget range and country
     outputs: country, number of inter-city transports, flight details, total flight cost'''
    attr_list = tf.get_types(val3.type)  # attraction types preferred by user
    country_info, city_info = tf.queries()  # fetching data from database
    country_list = tf.get_country(val2.weather, country_info)
    country_list.sort()
    city_val = list(city.objects.values_list('city_name', 'country'))
    while True:
        country_false.sort()  # list of invalid countries
        country_list.sort()  # list of countries which have the chosen weather
        if country_false != country_list:
            country = country_list[random.randint(0, len(country_list) - 1)]  # choosing a random country
            if country not in countries_visited:  # if country is not yet chosen as valid
                cities_in_country = [i[0] for i in city_val if i[1] == country]  # list of cities in chosen country
                if tf.country_validate(cities_in_country, attr_list, city_info):
                    country_final = country  # validating, finalising the country
                    if country not in countries_visited:
                        countries_visited.append(country_final)
                        country_false.append(country)  # adds it to list of invalid countries
                        flag = False
                        break
                else:
                    if country not in country_false:
                        country_false.append(country)  # adds it to list of invalid countries
                    else:
                        pass
            else:
                pass
        else:  # executes if no country of given weather is valid
            country = country_list[random.randint(0, len(country_list) - 1)]  # selecting the country by brute force
            country_final = country
            flag = True
            if country not in countries_visited:
                countries_visited.append(country_final)
                break
    flightlist = list(flights.objects.values_list('name', 'cost_per_head', 'clas', 'country'))  # fetching data from database
    if val2.budget == 'low':
        flight_obj = [i for i in flightlist if i[2] == 'Economy Class' and i[3] == country_final]  # deciding flight details based on budget
    elif val2.budget == 'med':
        flight_obj = [i for i in flightlist if
                      (i[2] == 'Business Class' or i[2] == 'Economy Class') and i[3] == country_final]
    else:
        flight_obj = [i for i in flightlist if
                      i[2] == ('Business Class' or i[2] == 'First Class') and i[3] == country_final]
    flight = flight_obj[random.randint(0, len(flight_obj) - 1)]
    flight_dict = {'Name': flight[0], 'Class': flight[2], 'Cost_per_head': flight[1]}
    flightcost = val3.ppl * flight[1]  # flight costs, multiply by number of seats
    return country_final, flight_dict, flightcost, flag


def f2(val1, val2, val3, val4, country, flag):
    '''calculates attraction + accommodation costs, decides attractions
    based on type input, decides accomodation based on budget.
    also adds the timeline info.
    outputs: final info, (acc + attr) cost, last city, last 2 are for edits'''
    city_val = list(city.objects.values_list('city_code', 'city_name', 'country'))  # fetching data from database
    cities_in_country = [[i[0], i[1]] for i in city_val if
                         i[2] == country]  # list of cities in the country:[city code, city name]
    print(country)
    info_city = tf.get_dict(cities_in_country)  # {city name: city code}
    codelist = [i[0] for i in cities_in_country]  # list of city codes
    attr_list = tf.get_types(val3.type)  # list of attraction types preferred by users
    if flag:
        attr_list = random.sample(['nat', 'her', 'mon', 'bea', 'mus', 'wil', 'pil', 'adv', 'amu'],
                                  4)  # attraction types if country is chosen by brute force
    f_dict = {}
    acc_val = list(acc.objects.values_list('city_id', 'name', 'type', 'cost_per_night'))  # fetching data from database
    acclist = [{'name': a[1], 'type': tf.get_acctype(a[2]), 'price': a[3], 'id': a[0]} for a in acc_val if
               a[0] in codelist]  # reorganizing fetched data into dict
    acc_cost = 0  # total cost of accommodation
    for i in acclist:
        acc_cost += math.ceil((i['price']) * val3.rooms / 2)
    country_info, city_info = tf.queries()  # fetching data from database
    for i in cities_in_country:
        c_dict = {}  # attraction info (only valid ones)
        valid_acc = [q for q in acclist if q['id'] == info_city[i[1]]]  # accommodations in city per city in country
        accc = valid_acc[random.randint(0, len(valid_acc) - 1)]  # choosing accommodation for a particular city
        adict = city_info[i[1]]
        for k, v in adict.items():
            if v in attr_list:
                c_dict[k] = v
            else:
                pass
        f_dict[i[1]] = {'attrs': c_dict, 'accs': accc}  # combining attraction and accommodation details
    temp = {}
    for k, v in f_dict.items():
        if len(v['attrs']) != 0:  # eliminating empty dicts if there are no attractions in any city
            temp[k] = v
        else:
            pass
    f_dict = temp
    cities = list(f_dict.keys())
    ff = {}
    for i in cities:
        ff[i] = f_dict[i]
    f_dict = ff
    f_dict = tf.shorten_timeline(f_dict)  # restricting length of trip
    k = list(f_dict.keys())
    print('k', k)
    v = list(f_dict.values())
    ax = [i['accs'] for i in v]
    desc_val = list(attractions.objects.values_list('name', 'desc', 'cost'))  # fetching data from database
    desc_dict = {i[0]: i[1] for i in desc_val}  # description of attractions
    new_desc = []
    for cit in v:
        tempd = {}
        for att in (cit['attrs']).keys():
            tempd[att] = {'desc': desc_dict[att], 'img': tf.get_image(att)}  # complete attraction details
        new_desc.append(tempd)  # list of attrs per city for all cities in the country
    subdict = [{'attrs': new_desc[i], 'accs': ax[i]} for i in range(len(new_desc))]
    final_dict = dict(zip(k, subdict))  # creating final itinerary dict
    print('new', new_desc)
    edit_desc = copy.deepcopy(new_desc)  # list of dicts of dicts, each elem is a city, sub-elem is an attraction
    print('edit', edit_desc)
    attcost = 0
    for cc in new_desc:
        for atr in cc:
            tempv = attractions.objects.get(name=atr)
            attcost += tempv.cost * val3.ppl
    total = attcost + acc_cost  # adding accommodation and attraction costs
    t_info, last = timeline_info(new_desc, val1, val2, val4)  # adding timeline info
    print('t_ingo', t_info)
    print('final1', final_dict)
    for j in new_desc:
        for ii, jj in j.items():
            jj['day'] = t_info[ii]['day']
            jj['date'] = t_info[ii]['date']
            jj['time'] = t_info[ii]['time']
            jj['mode'] = t_info[ii]['mode']
    print('newww', new_desc)
    print('final2', final_dict)
    print('ax', ax)
    return final_dict, total, last, edit_desc, ax


def timeline_info(dictt, val1, val2, val4):
    attrlist = []  # list of all attractions chosen (whole country)
    start_date = val2.start_date  # fetching start date
    rh = val1.type  # type of scheduling (relaxed/hectic)
    tranlist = tf.tran_func(val4.tran)  # transport between cities
    tran_val = list(transport.objects.values_list('name', 'type', 'clas'))
    tranlist1 = [i for i in tran_val if i[1] in tranlist]
    for i in dictt:
        attrlist.extend(list(i.keys()))
    if rh == 'rel':  # scheduling of attractions for relaxed trip
        info = {}
        for i in range(1, len(attrlist) + 1):
            att = attractions.objects.get(name=attrlist[i - 1])
            tran = tranlist1[random.randint(0, len(tranlist1) - 1)]
            if tran[2] is None:
                tran = list(tran)
                tran[2] = 'General'
                tran = tuple(tran)
            if att.time == 'mor':
                time = 'Morning'
            else:
                time = 'Evening'
            info[att.name] = {'day': i,
                              'date': start_date + datetime.timedelta(days=i, seconds=0, microseconds=0, milliseconds=0,
                                                                      minutes=0, hours=0, weeks=0),
                              'time': time,
                              'mode': {'tran_name': tran[0], 'type': tran[1], 'clas': tran[2]}
                              }
        last = start_date + datetime.timedelta(days=i + 1, seconds=0, microseconds=0, milliseconds=0, minutes=0,
                                               hours=0, weeks=0)  # end date
    else:  # scheduling of attractions for hectic trip
        info = {}
        for i in range(1, len(attrlist) + 1):
            att = attractions.objects.get(name=attrlist[i - 1])
            tran = tranlist1[random.randint(0, len(tranlist1) - 1)]
            if tran[2] is None:
                tran = list(tran)
                tran[2] = 'General'
                tran = tuple(tran)
            if att.time == 'mor':
                time = 'Morning'
            else:
                time = 'Evening'
            info[att.name] = {'day': math.ceil(i / 2),
                              'date': start_date + datetime.timedelta(days=math.ceil(i / 2), seconds=0, microseconds=0,
                                                                      milliseconds=0, minutes=0, hours=0, weeks=0),
                              'time': time,
                              'mode': {'tran_name': tran[0], 'type': tran[1], 'clas': tran[2]}
                              }
        last = start_date + datetime.timedelta(days=math.ceil(i / 2) + 1, seconds=0, microseconds=0, milliseconds=0,
                                               minutes=0, hours=0, weeks=0)  # end date
    return info, last


def show2(request):
    if request.method == 'GET':
        logged_in = request.user
        val1 = s1.objects.get(user_id=request.user.id)
        val2 = s2.objects.get(user_id=request.user.id)
        val3 = s3.objects.get(user_id=request.user.id)
        val4 = s4.objects.get(user_id=request.user.id)
        city_val = list(city.objects.values_list('city_name', 'country'))
        if (val1.city, val1.country) in city_val:
            country, flight_info, flightcost, flag = f1(val2, val3)
            city_info, cost1, last, new_Desc, ax = f2(val1, val2, val3, val4, country, flag)
            cit = list(city_info.keys())
            first = cit[0]
            COST = flightcost + cost1
            print('COST', COST)
            user_dict = {'id': request.user.id, 'country': country, 'countryedit': country + '_edit', 'dict': city_info,
                         'new': new_Desc, 'ax': ax, 'cost': COST, 'f_info': flight_info, 'last': last}
            handle = open("itinerary_files.dat", "ab")
            pickle.dump(user_dict, handle)
            handle.close()
            return render(request, 'final2.html', {'logged_in': logged_in,
                                                   'data1': val1,
                                                   'data2': val2,
                                                   'data3': val3,
                                                   'data4': val4,
                                                   'country': country,
                                                   'f_info': flight_info,
                                                   'info': city_info,
                                                   'first': first,
                                                   'last': last,
                                                   'cost': COST
                                                   }
                          )
        else:
            return render(request, 'city_error.html')


def show3(request):
    if request.method == 'GET':
        logged_in = request.user
        val1 = s1.objects.get(user_id=request.user.id)
        val2 = s2.objects.get(user_id=request.user.id)
        val3 = s3.objects.get(user_id=request.user.id)
        val4 = s4.objects.get(user_id=request.user.id)
        city_val = list(city.objects.values_list('city_name', 'country'))
        if (val1.city, val1.country) in city_val:
            country, flight_info, flightcost, flag = f1(val2, val3)
            city_info, cost1, last, new_Desc, ax = f2(val1, val2, val3, val4, country, flag)
            cit = list(city_info.keys())
            first = cit[0]
            COST = flightcost + cost1
            print('COST', COST)
            user_dict = {'id': request.user.id, 'country': country, 'countryedit': country + '_edit', 'dict': city_info,
                         'new': new_Desc, 'ax': ax, 'cost': COST, 'f_info': flight_info, 'last': last}
            handle = open("itinerary_files.dat", "ab")
            pickle.dump(user_dict, handle)
            handle.close()
            return render(request, 'final3.html', {'logged_in': logged_in,
                                                   'data1': val1,
                                                   'data2': val2,
                                                   'data3': val3,
                                                   'data4': val4,
                                                   'country': country,
                                                   'f_info': flight_info,
                                                   'info': city_info,
                                                   'first': first,
                                                   'last': last,
                                                   'cost': COST
                                                   }
                          )
        else:
            return render(request, 'city_error.html')


def itin_list(request):
    if request.method == 'GET':
        itinerary_list = []
        logged_in = request.user.first_name
        with open("itinerary_files.dat", "rb") as handle:
            while True:
                try:
                    itinerary = pickle.load(handle)
                    if itinerary['id'] == request.user.id:
                        itinerary_list.append(itinerary)
                    else:
                        pass
                except EOFError:
                    break
        return render(request, 'itinlist.html',
                      {'lst': itinerary_list, 'len': len(itinerary_list), 'logged_in': logged_in})
    else:
        return render(request, 'city_error.html')


def USA(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'USA':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Canada(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Canada':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def India(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'India':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def England(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'England':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Spain(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Spain':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Italy(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Italy':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def France(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'France':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Russia(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Russia':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Sweden(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Sweden':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Germany(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Germany':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Norway(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Norway':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Switzerland(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Switzerland':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Netherlands(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Netherlands':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Belgium(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Belgium':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Denmark(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Denmark':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Japan(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Japan':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def China(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'China':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Singapore(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Singapore':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def UAE(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'UAE':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Egypt(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Egypt':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Morocco(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Morocco':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Mexico(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Mexico':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def Australia(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Australia':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def NZ(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'New Zealand':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        cit = list(fin_dict['dict'].keys())
        first = cit[0]
        return render(request, 'sideview.html', {'i': fin_dict,
                                                 'logged_in': request.user,
                                                 'data1': s1.objects.get(user_id=request.user.id),
                                                 'first': first,
                                                 'data2': s2.objects.get(user_id=request.user.id)
                                                 })


def delete(request):
    if request.method == 'GET':
        it_list = []
        with open("itinerary_files.dat", "rb") as handle:
            while True:
                try:
                    itinerary = pickle.load(handle)
                    it_list.append(itinerary)
                except EOFError:
                    break
        return render(request, 'delete.html', {'ilist': it_list})  # redirects to deletion page
    elif request.method == 'POST':
        trip = request.POST['deleted_itinerary']  # fetching user input (deleted itinerary)
        if request.GET['d'] == 'delete':
            cty = trip.split()[2]
            fh1 = open("itinerary_files.dat", "rb") # removing itinerary from itinerary_files.dat by temporary file method
            temp = open("temp.dat", "wb")
            while True:
                try:
                    itinerary = pickle.load(fh1)
                    if itinerary['id'] == request.user.id and itinerary['country'] != cty:
                        pickle.dump(itinerary, temp)
                    else:
                        pass
                except EOFError:
                    break
            fh1.close()
            temp.close()
            os.remove('itinerary_files.dat')
            os.rename('temp.dat', 'itinerary_files.dat')
            itinerary_list = []
            logged_in = request.user.first_name
            with open("itinerary_files.dat", "rb") as handle:  # fetching itineraries already finalized by user
                while True:
                    try:
                        itinerary = pickle.load(handle)
                        if itinerary['id'] == request.user.id:
                            itinerary_list.append(itinerary)
                        else:
                            pass
                    except EOFError:
                        break
            return render(request, 'itinlist.html',
                          {'lst': itinerary_list, 'len': len(itinerary_list), 'logged_in': logged_in})  # returning to itinerary list
        else:
            return render(request, 'city_error.html')


def edit(request):
    if request.method == 'POST':
        if request.GET['e'] == 'edit':
            dit_attrs = request.POST.getlist('edit')  # fetching list of deleted attractions
            s = dit_attrs[0]
            edit_attrs = []  # list of attraction without (Country)
            for i in dit_attrs:
                ls = i.split()
                word = ''
                for j in range(0, len(ls) - 1):
                    word += (ls[j] + ' ')
                edit_attrs.append(word[:-1])
            cost_red = 0
            val3 = s3.objects.get(user_id=request.user.id)
            for atr in edit_attrs:
                tempv = attractions.objects.get(name=atr)
                cost_red += tempv.cost * val3.ppl  # cost to be reduced
            country = s.split()[-1][1:len(s.split()[-1]) - 1]  # fetching country name
            with open("itinerary_files.dat", "rb") as handle:  # retrieving itinerary for editing
                while True:
                    try:
                        itinerary = pickle.load(handle)
                        if itinerary['id'] == request.user.id and itinerary['country'] == country:
                            fin_dict = itinerary
                        else:
                            pass
                    except EOFError:
                        break
            val1 = s1.objects.get(user_id=request.user.id)  # user inputs
            val2 = s2.objects.get(user_id=request.user.id)
            val4 = s4.objects.get(user_id=request.user.id)
            newdesc = fin_dict['new']
            axx = fin_dict['ax']
            city_val = list(city.objects.values_list('city_code', 'city_name', 'country'))  # fetching data from database
            k = [i[1] for i in city_val if
                 i[2] == country]  # list of cities in the country:[city code, city name]
            intdesc = []
            for cur_city in newdesc:
                for attr in edit_attrs:
                    try:
                        del cur_city[attr]  # deleting selected attractions
                    except KeyError:
                        pass
                intdesc.append(cur_city)
            finaldesc = []
            for thing in intdesc:
                if len(thing) != 0:
                    finaldesc.append(thing)
                else:
                    axx.pop(intdesc.index(thing))
                    k.pop(intdesc.index(thing))
            subdict = [{'attrs': finaldesc[i], 'accs': axx[i]} for i in range(len(finaldesc))]
            final_dict = dict(zip(k, subdict))
            t_info, last = timeline_info(finaldesc, val1, val2, val4)  # reorganising timeline info
            for j in finaldesc:
                for ii, jj in j.items():
                    jj['day'] = t_info[ii]['day']
                    jj['date'] = t_info[ii]['date']
                    jj['time'] = t_info[ii]['time']
                    jj['mode'] = t_info[ii]['mode']
            fh1 = open("itinerary_files.dat", "rb")
            temp = open("temp.dat", "wb")
            while True:
                try:
                    itinerary = pickle.load(fh1)
                    if itinerary['id'] == request.user.id and itinerary['country'] == country:
                        itinerary['dict'] = final_dict
                        itinerary['last'] = last
                        itinerary['cost'] = itinerary['cost'] - cost_red  # reducing the cost
                        pickle.dump(itinerary, temp)
                    else:
                        pickle.dump(itinerary, temp)
                except EOFError:
                    break
            fh1.close()
            temp.close()
            os.remove('itinerary_files.dat')
            os.rename('temp.dat', 'itinerary_files.dat')
            itinerary_list = []
            logged_in = request.user.first_name
            with open("itinerary_files.dat", "rb") as handle:
                while True:
                    try:
                        itinerary = pickle.load(handle)
                        if itinerary['id'] == request.user.id:
                            itinerary_list.append(itinerary)
                        else:
                            pass
                    except EOFError:
                        break
            return render(request, 'itinlist.html', {'lst': itinerary_list,  # returning to itinerary list
                                                     'len': len(itinerary_list),
                                                     'logged_in': logged_in
                                                     })
        else:
            return render(request, 'itinlist.html')
    else:
        return render(request, 'itinlist.html')


def USA_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'USA':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Canada_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Canada':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def India_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'India':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def England_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'England':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Spain_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Spain':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Italy_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Italy':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def France_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'France':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Russia_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Russia':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Sweden_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Sweden':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Germany_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Germany':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Norway_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Norway':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Switzerland_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Switzerland':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Netherlands_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Netherlands':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Belgium_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Belgium':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Denmark_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Denmark':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Japan_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Japan':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def China_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'China':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Singapore_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Singapore':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def UAE_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'UAE':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Egypt_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Egypt':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Morocco_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Morocco':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Mexico_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Mexico':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def Australia_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'Australia':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})


def NZ_edit(request):
    with open("itinerary_files.dat", "rb") as handle:
        while True:
            try:
                itinerary = pickle.load(handle)
                if itinerary['id'] == request.user.id and itinerary['country'] == 'New Zealand':
                    fin_dict = itinerary
                else:
                    pass
            except EOFError:
                break
    if request.method == 'GET':
        return render(request, 'edit.html', {'i': fin_dict})
