"""GenomicPrediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from app import api_views
from rest_framework.authtoken import views as authviews

#api urls
from django.conf.urls import url, include
from rest_framework import routers
from app import api_views

router = routers.DefaultRouter()
#router.register(r'patient', api_views.PatientViewSet)# replaced with manual views 
router.register(r'embryo', api_views.EmbryoViewSet)
router.register(r'user', api_views.UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    #patient uses manual views
    path('patient/', api_views.patient_list),
    path('patient/<int:pk>/', api_views.patient_detail),

    #path('login/', views.login, name='login'),
    path('api-token-auth/', authviews.obtain_auth_token),
    path('mailreport/<int:pk>/', api_views.mail_report),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('django-rq/', include('django_rq.urls'))
]
