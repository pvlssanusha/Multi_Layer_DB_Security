from django.urls import path
from .views_auth import *
from . import views
from .view_records import *
urlpatterns = [
    path("", user_login, name="index"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("records/", records_page, name="records"),
    path("signup/", user_signup, name="signup"),
    path("records/delete/<int:record_id>/", delete_record, name="delete_record"),
]
