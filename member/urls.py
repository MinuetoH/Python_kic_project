# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 10:19:40 2022

@author: KITCOOP
member/urls.py
"""

from django.urls import path
from . import views
# http://127.0.0.1:8000/member/
urlpatterns=[
    #http://127.0.0.1:8000/member/login/ 요청시 view.py
    #  의 login 함수 실행
    path("login/",views.login, name="login"),
    #http://127.0.0.1:8000/member/join/
    path('join/', views.join,name='join'),
    path('main/', views.main, name='main'),
    path('logout/', views.logout, name='logout'),
    path('info/<str:id>/', views.info,name='info'),
    path('update/<str:id>/', views.update,name='update'),
    path('delete/<str:id>/', views.delete,name='delete'),
    path('list/', views.list,name='list'),
    path('password/', views.password,name='password'),
]