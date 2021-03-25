import mysql.connector
import random


def queries():
    con = mysql.connector.connect(host="localhost", user="root", passwd="_Shail.esh2403", database="main")
    if con.is_connected():
        mycursor = con.cursor()
        sql = "select*from weat;"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        country_dict = {result[i][0]: result[i][2] for i in range(len(result))}
        sql1 = "select*from get_city;"
        mycursor.execute(sql1)
        result2 = mycursor.fetchall()
        city_dict = {i[0]: {i[1]: i[2]} for i in result2} # {city: {attraction: attraction type}}
        for i in result2:
            city_dict[i[0]].update({i[1]: i[2]})
        return country_dict, city_dict



def get_country(weather, d):
    country_list = list(d.keys())
    col_list = [i for i in country_list if d[i] == 'col']  # list of cold countries
    hot_list = [i for i in country_list if d[i] == 'hot']  # list of hot countries
    mod_list = [i for i in country_list if d[i] == 'mod']  # list of moderate countries
    if weather == 'col':
        return col_list
    elif weather == 'hot':
        return hot_list
    elif weather == 'mod':
        return mod_list
    else:
        return

def city_validate(city, attr_list, city_dict):
    adict = city_dict[city]  # attraction info per city in the form: {'attr': 'type'}
    alist = list(adict.values())  # fetching their types
    tr, fa = 0, 0
    for i in alist:
        if i in attr_list:  # preferred attraction types
            tr += 1
        else:
            fa += 1
    if tr >= fa:  # if there are more valid than invalid attractions, city is valid
        return True
    else:
        return False


def country_validate(cities_in_country, attr_list, city_dict):
    '''inputs: cities in the chosen country, list of attraction types chosen by user,
    city info with attractions and its types'''
    bool_list = []
    for i in cities_in_country:  # validating cities within the country
        bool_list.append(city_validate(i, attr_list, city_dict))
    if bool_list.count(True) > bool_list.count(False):  # if there are more valid than invalid cities, country is valid
        return True
    else:
        return False


def get_image(attr):
    lst = attr.split()
    new_lst = []
    for i in lst:
        new_lst.append(i.lower())
    img = ''
    for j in new_lst:
        img += j + '_'
    img = img[:-1] + '.jpg'
    return img


def tran_func(string):
    f = []
    for i in string:
        if i == '1':
            f.append('bus')
        elif i == '2':
            f.append('taxi')
        else:
            f.append('train')
    return f


def get_acctype(s):
    if s == 1:
        return 'Hotel'
    elif s == 2:
        return 'Motel'
    elif s == 3:
        return 'Resort'
    elif s == 4:
        return 'Hostel'
    else:
        return 'Bed & Breakfast'


def get_dict(citylist):
    return {i[1]: i[0] for i in citylist}


def shorten_timeline(ds):
    fff = {}
    if len(ds) > 10:
        cities = list(ds.keys())
        cities = cities[:11]
        for i in cities:
            fff[i] = ds[i]
    else:
        fff = ds
    return fff


def get_types(typestring):
    attr_list = []  # valid attraction types
    for i in typestring:
        if i == '1':
            attr_list.append('nat')
        elif i == '2':
            attr_list.append('mon')
        elif i == '3':
            attr_list.append('amu')
        elif i == '4':
            attr_list.append('her')
        elif i == '5':
            attr_list.append('bea')
        elif i == '6':
            attr_list.append('mus')
        elif i == '7':
            attr_list.append('adv')
        elif i == '8':
            attr_list.append('pil')
        elif i == '9':
            attr_list.append('wil')
        else:
            pass
    return attr_list
