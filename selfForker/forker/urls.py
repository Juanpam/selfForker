from django.urls import path, include
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', authViews.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('social-auth/', include('social_django.urls', namespace='social'))
]
