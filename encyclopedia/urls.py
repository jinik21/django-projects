from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.Random_Page, name="random"),
    path("wiki/create",views.Create_page,name="create"),
    path("wiki/edit/<str:name>",views.edit,name="edit"),    
    path("wiki/<str:name>",views.name,name="name"),
]
