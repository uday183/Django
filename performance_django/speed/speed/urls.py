"""speed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from performance.views import NormalSave, AutomicSave, BulkCreate, GetBulkNormal, GetBulk,\
                              GetBulkQueryIterator, CeleryUserCreation
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^normal_save/', NormalSave.as_view(),name='save_record_normal'),
    url(r'^automic_save/', AutomicSave.as_view(),name='save_record_automic'),
    url(r'^bulk_save/', BulkCreate.as_view(),name='bulk_save'),
    url(r'^get_bulk/', GetBulkNormal.as_view(),name='get_bulk'),
    url(r'^get_bulk_fast/', GetBulk.as_view(),name='get_bulk_fast'),
    url(r'^get_query_iter/', GetBulkQueryIterator.as_view(),name='get_bulk_iter'),
    url(r'^celery_user_create/', CeleryUserCreation.as_view(),name='celery_user_create'),
]
