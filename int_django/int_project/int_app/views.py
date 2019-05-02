from django.shortcuts import render,render_to_response, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.generic.base import View, TemplateView
import logging
uday_info_logger = logging.getLogger('uday_info')
uday_except_logger = logging.getLogger('uday_except')
from .models import *
# Create your views here.

class Test(View):
    def get(self,request):
        try:
            uday_info_logger.info('test class is calling')
            context = {'name':'uday'}
            x=0
            y=0
            z=x/y
        except ZeroDivisionError:
            uday_except_logger.critical('calling exception error')
        return render(request,'test.html',context=context)


class Index(View):
    def get(self,request):
        data = UserDetails.objects.all()
        context = {'data':data}
        return render(request,'index.html',context)