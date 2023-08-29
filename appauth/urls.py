from django.urls import path
from appauth import views

urlpatterns = [
    path('', views.signup, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('createbio/', views.createbio, name='createbio')
]