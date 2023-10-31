from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import requests
import random

from .models import User, Completion, Todo


## Simple view to render the front page
def index(request):
    return render(request, "compendium/browse.html")


## Render the search page. Searches are handled in compendium.js
def search(request):
    return render(request, "compendium/search.html")


## Log a user in
@csrf_exempt
def compendium_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        ## Authenticate that the user exists
        current_user = authenticate(request, username=username, password=password)

        if current_user is not None:
            ## If so, log them in and redirect
            login(request, current_user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "compendium/login.html", {"error": "Log in failed"})

    return render(request, "compendium/login.html")


## Log current user out
def compendium_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    ## When the user submits the form
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation_password = request.POST["confirm-password"]

        ## Check the passwords match
        if password != confirmation_password:
            return render(
                request, "compendium/register.html", {"error": "Passwords don't match"}
            )

        ## Check the password is at least 8 digits long
        if len(password) < 8:
            return render(
                request,
                "compendium/register.html",
                {"error": "Password needs to be at least 8 digits"},
            )

        ## User error handling when trying to create the user in case they already exist
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "compendium/register.html",
                {"error": "Username/password exists"},
            )

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "compendium/register.html")


## Render MyTracker page. Further functionality is handled in compendium.js
def mytracker(request):
    return render(request, "compendium/mytracker.html")


## Render a page for a single compendium entry
def entry(request, id):
    response = requests.get(
        f"https://botw-compendium.herokuapp.com/api/v3/compendium/entry/{id}"
    )

    data = response.json()["data"]

    context = {"data": data}

    ## If we have a logged in user, get the "completion" and "todo" statuses and add to context
    try:
        if request.user:
            completed = Completion.objects.filter(
                itemid=id, compendium_user=request.user
            ).first()
            todo = Todo.objects.filter(itemid=id, list_writer=request.user).first()
            context["completed"] = completed
            context["todo"] = todo
    except TypeError:
        pass

    return render(request, "compendium/entry.html", context)


## Render a random entry by generating a random number and passing to entry()
## This could definitely be sped up by hard-coding the total possible number of entries
## instead of pulling the whole compendium.
def random_entry(request):
    response = requests.get(
        f"https://botw-compendium.herokuapp.com/api/v3/compendium/all"
    )
    random_id = random.randint(1, len(response.json()["data"]))
    return HttpResponseRedirect(reverse("entry", args=[random_id]))


## API view that uses a PUT request to toggle whether
## or not the user has "collected" the item.
@csrf_exempt
def toggle_collection(request, itemid):
    if request.method == "PUT":
        compendium_user = User.objects.get(username=request.user)
        try:
            completion = Completion(itemid=itemid, compendium_user=compendium_user)
            completion.save()
        except IntegrityError:
            completion = Completion.objects.filter(
                itemid=itemid, compendium_user=compendium_user
            )
            completion.delete()
    return HttpResponse(status=204)


## API view that uses a PUT request to toggle whether
## or not the user wants the item on their "to-do" list
@csrf_exempt
def toggle_todo(request, itemid):
    if request.method == "PUT":
        compendium_user = User.objects.get(username=request.user)
        try:
            todo = Todo(itemid=itemid, list_writer=compendium_user)
            todo.save()
        except IntegrityError:
            todo = Todo.objects.filter(itemid=itemid, list_writer=compendium_user)
            todo.delete()
    return HttpResponse(status=204)


## API view that returns a flat list of itemids representing a todo list.
@csrf_exempt
def todo(request):
    todolist = Todo.objects.filter(list_writer=request.user).values_list(
        "itemid", flat=True
    )

    return JsonResponse(list(todolist), safe=False)


## API view that returns a flat list of itemids that represent all completed items.
def completed(request):
    completions = Completion.objects.filter(compendium_user=request.user).values_list(
        "itemid", flat=True
    )

    return JsonResponse(list(completions), safe=False)
