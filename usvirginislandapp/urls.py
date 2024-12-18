"""
URL configuration for usvirginisland project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path("",index,name="index"),
    path("pdf/",pdf,name="pdf"),
    path("member/",member,name="member"),
    path('get_data/', sponsorpopup, name='sponsorpopup'),
    path('getcosp_data/',cosponsorpopup,name='cosponsorpopup'),
    path('bill_detail/<int:doc_entry>/',billdetail,name='bill_detail'),
    path('view-pdf/', serve_pdf, name='view_pdf'),    
]
