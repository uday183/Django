from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book
import datetime
import gc
# Create your views here.

class NormalSave(APIView):
    def post(self,request):
        st = datetime.datetime.now()
        print ("started time:",st)
        for i in range(0,10000):
            Book.objects.create(name=i,place=i,country=i)
        end = datetime.datetime.now()
        print ("end time time:",end)
        print("diff :", end-st)
        return Response("saved")

#results:
# started time: 2020-07-23 09:18:59.563808
# end time time: 2020-07-23 09:38:31.556767
# diff : 0:19:31.992959
#################################################################################

class AutomicSave(APIView):
    @transaction.atomic
    def post(self,request):
        st = datetime.datetime.now()
        print ("started time:",st)
        for i in range(0,10000000,1000):
            Book.objects.create(name=i,place=i,country=i)
        end = datetime.datetime.now()
        print ("end time time:",end)
        print("diff :", end-st)
        return Response("saved")

#result
# started time: 2020-07-23 09:40:58.701664
# end time time: 2020-07-23 09:41:00.424635
# diff : 0:00:01.722971

#################################################################################

class BulkCreate(APIView):
    def post(self,request):
        st = datetime.datetime.now()
        print ("started time:",st)
        instances = [Book(name=i,place=i,country=i) for i in range(0, 10000)]
        Book.objects.bulk_create(instances)
        end = datetime.datetime.now()
        print ("end time time:",end)
        print("diff :", end-st)
        return Response("saved")

#result
# started time: 2020-07-23 10:11:36.769534
# end time time: 2020-07-23 10:11:37.305944
# diff : 0:00:00.536410


#################################################################################

class GetBulkNormal(APIView):
    def get(self,request):
        st = datetime.datetime.now()
        print ("started time:",st)
        obj =[(i.name,i.place,i.country) for i in Book.objects.iterator()][:10]
        end = datetime.datetime.now()
        print ("end time time:",end)
        print("diff :", end-st)
        return Response(obj)

#result
# started time: 2020-07-23 10:11:36.769534
# end time time: 2020-07-23 10:11:37.305944
#diff : 0:00:08.038571
#Book.objects.all()[:10]-0:00:10.833879
#Book.objects.iterator()[:10] - 0:00:07.696596

#################################################################################

class GetBulk(APIView):
    def get(self,request):
        st = datetime.datetime.now()
        print ("started time:",st)
        count = Book.objects.all().count()
        chunk_size = 1210000
        # import ipdb;ipdb.set_trace()
        lst=[]
        for i in range(0, count, chunk_size):
            posts = Book.objects.all()[i:i+chunk_size]
            lst.append([{'name':i.name,'place':i.place,'country':i.country} for i in posts])
        end = datetime.datetime.now()
        print ("end time time:",end)
        print("diff :", end-st)
        return Response(lst[:1])

#result
# started time: 2020-07-23 11:06:39.502144
# end time time: 2020-07-23 11:06:49.703953
# diff : 0:00:10.201809


#################################################################################
def queryset_iterator(queryset, chunksize=1210000):
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()

class GetBulkQueryIterator(APIView):
    def get(self,request):
        page = request.GET.get('page')
        st = datetime.datetime.now()
        print ("started time:",st)
        posts = Book.objects.all()
        #res = queryset_iterator(posts)
        paginator = Paginator(posts, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        end = datetime.datetime.now()
        print ("end time time:",end)
        print("diff :", end-st)
        #import ipdb;ipdb.set_trace()

        return Response([{'name':i.name,'place':i.place,'country':i.country} for i in users])
        #return Response([{'name':i.name,'place':i.place,'country':i.country} for i in res])
#result
# started time: 2020-07-23 12:33:00.370047
# end time time: 2020-07-23 12:33:00.370151
# diff : 0:00:00.015797

#################################################################################