from django.urls import path
from users import views

urlpatterns=[
    path('register',views.RegisterAPIView.as_view(),name='register'),
    path('login',views.LoginAPIView.as_view(),name='login'),
    path('user',views.CurrentUserAPIView.as_view(),name='user'),
]