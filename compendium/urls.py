from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("login/", views.compendium_login, name="login"),
    path("logout/", views.compendium_logout, name="logout"),
    path("register/", views.register, name="register"),
    path("mytracker/", views.mytracker, name="mytracker"),
    path("entry/<int:id>/", views.entry, name="entry"),
    path("randomentry", views.random_entry, name="random_entry"),

    ## API views
    path("togglecollection/<int:itemid>", views.toggle_collection, name="toggle_collection"),
    path("toggletodo/<int:itemid>", views.toggle_todo, name="toggle_todo"),
    path("todo/", views.todo, name="todo"),
    path("completed/", views.completed, name="completed")

]