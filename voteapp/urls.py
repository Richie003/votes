from django.urls import path
from voteapp import views

urlpatterns = [
    path('', views.index, name="home"),
    path('elect/', views.electoraltable, name="elect"),
    path('elect-api/', views.electoraltable_api),
    path('get_votecheck/', views.get_votecheck),
    path('dashboard/', views.adminDashboard, name='dashboard'),
    # createuser API endpoint url
    path('createuser/', views.createUser, name="createuser"),
    path('createrole/', views.addrole, name="createrole"),
]