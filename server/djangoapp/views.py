from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview, CarMake, CarModel
from .restapis import get_dealers_from_cf, get_request, get_dealer_reviews_from_cf, post_request, get_dealer_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger 
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/2bda4203-74dd-4183-b1cb-62a99d3efd8e/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context["dealerships"] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):

def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/2bda4203-74dd-4183-b1cb-62a99d3efd8e/dealership-package/get-review.json"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)

        url = "https://us-east.functions.appdomain.cloud/api/v1/web/2bda4203-74dd-4183-b1cb-62a99d3efd8e/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealer = get_dealer_by_id(url, dealer_id)

        context["reviews"] = reviews
        context["dealer"] = dealer[0]
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    context["dealer_id"] = dealer_id
    if request.method == "POST":
        if request.user.is_authenticated:
            review = dict()
            json_payload = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["id"] = "1404"
            review["review"] = request.post["review"]
            review["purchase"] = "False"
            review["name"] = "John"
            review["car_make"] = "Audi"
            review["car_model"]  = "Car"
            review["car_year"] = "2021"
            review["purchase_date"] =  "02/16/2021"
            review["another"] = "field"

            json_payload["review"] = review
            
            url = 'https://us-east.functions.appdomain.cloud/api/v1/web/2bda4203-74dd-4183-b1cb-62a99d3efd8e/dealership-package/post-review.json'

            response = post_request(url, json_payload, dealerId=dealer_id)

        redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        
    else:
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/2bda4203-74dd-4183-b1cb-62a99d3efd8e/dealership-package/get-dealership.json"
        dealer = get_dealer_by_id(url, dealer_id)
        context["dealer"] = dealer[0]
        context["cars"] = CarModel.objects.all()

        return render(request, 'djangoapp/add_review.html', context)
    


