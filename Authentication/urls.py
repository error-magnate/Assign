from django.urls import path, include
from. import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('reset/', views.reset, name="reset"),
    path('verify/<str:uid>/<str:pid>', views.verify, name="reset"),
    path('logout/', views.logout, name="logout"),
]
