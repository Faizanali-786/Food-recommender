
import email
from .forms import *
from django.shortcuts import render, redirect
import smtplib
import random 
import pickle
import pandas as pd
from . import src

from .models import *

def signup_page(request):
    return render(request, 'signup.html')

def confirm_code(request):
    if request.POST:
        request.session['uname'] = request.POST['uname']
        request.session['pnumber'] = request.POST['pnumber']
        request.session['eml'] = request.POST['eml']
        request.session['Password'] = request.POST['Password']
        request.session['home'] = request.POST['home']
        request.session['city'] = request.POST['city']
        request.session['age'] = request.POST['age']
    my_email = "Smartfoodweb@gmail.com"
    password = "cvgnveovnzvveccg"
    choic = random.randrange(111111, 999999, 3)
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=my_email, password=password)
    msg = """
    ---------- MESSAGE FOLLOWS ----------
    
    ''
    'To:''"""+ request.session['eml'] +"""'
    'Subject: Food App Verification Code'
    ''
    'Your Food App Verification Code is """+ str(choic)  +  """'
    ------------ END MESSAGE ------------
    """
    connection.sendmail(from_addr=my_email,
                        to_addrs=request.session['eml'], msg=msg)
    connection.close()
    return render(request,"confirm.html")

def signup_page(request):
    return render(request, 'signup.html')
def register_user(request):
    obj = Signup(username=request.session['uname'], email_address=request.session['eml'],
                 phone_number=request.session['pnumber'],  home_address=request.session['home'], password=request.session['Password'], city=request.session['city'], age=request.session['age'])
    count = Signup.objects.filter(
        email_address=request.session['eml']).count()
    if count > 0 :
        return render(request, 'signup.html', {"username_error": "Username Already Exist"})
    else:
        obj.save()
    return redirect('/')


def login_page(request):
    if request.POST:
        request.session['eml'] = request.POST['eml']
        request.session['Password'] = request.POST['password']

        count_user = Signup.objects.filter(
            email_address=request.session['eml'], password=request.session['Password']).count()
        count_manager = ManagerSignUp.objects.filter(
            email_address=request.session['eml'], password=request.session['Password']).count()
        if count_user > 0:
            return redirect("/")
        elif count_manager > 0:
            return redirect("/manager")
        else:
            return render(request, 'login.html', {"Details Error": "Invalid Details"})

    return render(request, 'login.html')


def logout(request):
    try:
        del request.session['eml']
    except KeyError:
        pass
    return render(request, "login.html")



def home_page(request):
    if not request.session.get('eml'):
        return redirect("/login")
    else:
        user = Signup.objects.get(email_address=request.session['eml'])
        cat = Category.objects.all()
        data = Food.objects.all()
    context = {"your_email": request.session['eml'], "items": data,
               "category": cat, "your_username": user.username}
    return render(request, "home.html", context)


def cat_id(request, id):
   
    cat = Category.objects.get(id=id)
    user = Signup.objects.get(email_address=request.session['eml'])

    data = Food.objects.filter(category=cat.id)
    category = Category.objects.all()

    context = {
        "your_email": request.session['eml'], "food": data, "cato": category ,"your_username":user.username}
    return render(request, "fooditems.html", context)


def manager(request):
    try:
        manager = ManagerSignUp.objects.get(email_address=request.session['eml'])
        if not request.session.get('eml'):
            return redirect("/login")
        else:
            cat = Category.objects.all()
            data = Food.objects.all()
            context = {"your_email": request.session['eml'], "food": data, "cato": cat ,"your_username":manager.username}
            return render(request,"manager.html",context)
    except  Exception:
        return redirect("/login")

def manager_cat_id(request,id):
    try:
        cat = Category.objects.get(id=id)
        manager = ManagerSignUp.objects.get(email_address=request.session['eml'])

        data = Food.objects.filter(category=cat.id)
        category = Category.objects.all()

        # print(data)
        context = {
            "your_email": request.session['eml'], "food": data, "cato": category ,"your_username":manager.username}
        return render(request,"manager.html",context)
    except  Exception:
        return redirect("/login")


def order_page(request):
    try:
        order = OrderItem.objects.all()
        manager = ManagerSignUp.objects.get(email_address=request.session['eml'])
        cat = Category.objects.all()
        context = {"order":order,"cato":cat,"your_email": request.session['eml'],"your_username": manager.username}
        return render(request, "order.html",context)
    except  Exception:
        return redirect("/login")

def recommend(request):
    try:
        manager = ManagerSignUp.objects.get(email_address=request.session['eml'])
        orders = pd.read_csv('orders.csv')
        new_and_specials = pd.read_csv('new_and_specials.csv')
        users = pd.read_csv('users.csv')
        with open("food_dataset.pkl","rb") as file_handle:
            df1 = pickle.load(file_handle)

        # the minimum number of votes required to appear in recommendation list, i.e, 60th percentile among 'num_rating'
        m= df1['num_rating'].quantile(0.6)
        
        # items that qualify the criteria of minimum num of votes
        q_items = df1.copy().loc[df1['num_rating'] >= m]

        # weighted_rating = src.weighted_rating(x, m=m, C=C)
        top_rated_items  = src.rated_items(q_items)
        popitems = src.pop_items(df1)

        columns = ['title', 'canteen_id', 'price', 'comment']
        current_user = 2
        current_canteen = src.get_user_home_canteen(users, current_user)

        personalised_r = src.personalised_recomms(orders, df1, current_user, columns)
        get_top_rated = src.get_top_rated_items(top_rated_items, df1, columns)
        get_new_and_specials_r = src.get_new_and_specials_recomms(new_and_specials, users, df1, current_canteen, columns)
        get_popular = src.get_popular_items(popitems, df1, columns).head(3)

        past_title_list = []
        past_price_list = []
        for i , val in enumerate(personalised_r.title):
            past_title_list.append(val)
        for i , val in enumerate(personalised_r.price):
            past_price_list.append(val)
        top_rated_title_list = []
        top_rated_price_list = []
        for i , val in enumerate(get_top_rated.title):
            top_rated_title_list.append(val)
        for i , val in enumerate(get_top_rated.price):
            top_rated_price_list.append(val)
        new_title_list = []
        new_price_list = []
        for i , val in enumerate(get_new_and_specials_r.title):
            new_title_list.append(val)
        for i , val in enumerate(get_new_and_specials_r.price):
            new_price_list.append(val)
        popular_title_list = []
        popular_price_list = []
        for i , val in enumerate(get_popular.title):
            popular_title_list.append(val)
        for i , val in enumerate(get_popular.price):
            popular_price_list.append(val)


        print(get_new_and_specials_r)

        past_list = zip(past_title_list , past_price_list)
        top_rated = zip(top_rated_title_list , top_rated_price_list)
        new_list = zip(new_title_list , new_price_list)
        popular = zip(popular_title_list , popular_price_list)
        category = Category.objects.all()


        context = {"cato":category,"manager_username":manager.username,"your_email":request.session['eml'],"past_list":past_list,"top_rated":top_rated,"special":new_list,"popularr":popular}
        return render(request,"recommended.html",context)
    except Exception:
        return redirect("/login")

def recommend_user(request):
    try:
        user = Signup.objects.get(email_address=request.session['eml'])
        orders = pd.read_csv('orders.csv')
        new_and_specials = pd.read_csv('new_and_specials.csv')
        users = pd.read_csv('users.csv')
        with open("food_dataset.pkl","rb") as file_handle:
            df1 = pickle.load(file_handle)

        # the minimum number of votes required to appear in recommendation list, i.e, 60th percentile among 'num_rating'
        m= df1['num_rating'].quantile(0.6)
        
        # items that qualify the criteria of minimum num of votes
        q_items = df1.copy().loc[df1['num_rating'] >= m]

        # weighted_rating = src.weighted_rating(x, m=m, C=C)
        top_rated_items  = src.rated_items(q_items)
        popitems = src.pop_items(df1)

        columns = ['title', 'canteen_id', 'price', 'comment']
        current_user = 2
        current_canteen = src.get_user_home_canteen(users, current_user)

        personalised_r = src.personalised_recomms(orders, df1, current_user, columns)
        get_top_rated = src.get_top_rated_items(top_rated_items, df1, columns)
        get_new_and_specials_r = src.get_new_and_specials_recomms(new_and_specials, users, df1, current_canteen, columns)
        get_popular = src.get_popular_items(popitems, df1, columns).head(3)

        past_title_list = []
        past_price_list = []
        for i , val in enumerate(personalised_r.title):
            past_title_list.append(val)
        for i , val in enumerate(personalised_r.price):
            past_price_list.append(val)
        top_rated_title_list = []
        top_rated_price_list = []
        for i , val in enumerate(get_top_rated.title):
            top_rated_title_list.append(val)
        for i , val in enumerate(get_top_rated.price):
            top_rated_price_list.append(val)
        new_title_list = []
        new_price_list = []
        for i , val in enumerate(get_new_and_specials_r.title):
            new_title_list.append(val)
        for i , val in enumerate(get_new_and_specials_r.price):
            new_price_list.append(val)
        popular_title_list = []
        popular_price_list = []
        for i , val in enumerate(get_popular.title):
            popular_title_list.append(val)
        for i , val in enumerate(get_popular.price):
            popular_price_list.append(val)


        print(get_new_and_specials_r)

        past_list = zip(past_title_list , past_price_list)
        top_rated = zip(top_rated_title_list , top_rated_price_list)
        new_list = zip(new_title_list , new_price_list)
        popular = zip(popular_title_list , popular_price_list)
        category = Category.objects.all()
    # user = Signup.objects.get(email_address=request.session['eml'])


        context = {"cato":category,"user_username":user.username,"your_email":request.session['eml'],"past_list":past_list,"top_rated":top_rated,"special":new_list,"popularr":popular}
        return render(request,"recommended.html",context)
    except Exception:
        return redirect("/login")

def confirm_order(request):
   
    if request.GET.get("Confirm") == 'Confirm':
        my_email = "Smartfoodweb@gmail.com"
        password = "cvgnveovnzvveccg"
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=my_email, password=password)
        msg = """
        ---------- MESSAGE FOLLOWS ----------
        ''
        'To:' """+ request.session['eml'] +"""'
        'Subject: Food App Order You Got an Order'
        ''
        ' from = """ + request.session['eml'] +"""'
        ------------ END MESSAGE ------------
        """
        connection.sendmail(from_addr=my_email,to_addrs=request.session['eml'], msg=msg)
        connection.close()
        
        return redirect("/")
    else:
        return redirect('/login')