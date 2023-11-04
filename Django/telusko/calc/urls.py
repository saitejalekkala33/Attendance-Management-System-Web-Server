from django.urls import path

from . import views

urlpatterns = [
    # URL pattern for the home page
    path('', views.home, name='home'),

    # URL pattern for the "signin" page
    path('signin/', views.signin, name='signin'),

     # URL pattern for the "signup" page
    path('signup/', views.signup, name='signup'),

    # URL pattern for the "delete" page
    path('delete/', views.delete, name='delete'),

    # URL pattern for recognizing a user from a captured image
    path('recognize_user/', views.recognize_user, name='recognize_user'),

    # URL pattern for registering a user from a captured image
    path('register_user/', views.register_user, name='register_user'),

    # URL pattern for deleting user data based on a captured image
    path('delete_user_data/', views.delete_user_data, name='delete_user_data')
]