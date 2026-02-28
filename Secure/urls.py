from django.urls import path
from .views_auth import user_login, user_logout
from . import views
from .view_records import *
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("records/", view_records),
    path("records/delete/<int:record_id>/", delete_record),
]
