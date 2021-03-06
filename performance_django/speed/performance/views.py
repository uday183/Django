from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
kencloud_logger = logging.getLogger('uday_info')
kencloud_except_logger = logging.getLogger('uday_except')
from .models import Book,Books,Author,Publisher,Store
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
        for i in range(0,10000000,100):
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
        kencloud_logger.info('GetBulkNormal(%s) ' %(obj))
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
        kencloud_logger.info('GetBulkNormal(%s) ' %(count))
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
        kencloud_logger.info('GetBulkQueryIterator(%s) ' %(users))
        return Response([{'name':i.name,'place':i.place,'country':i.country} for i in users])
        #return Response([{'name':i.name,'place':i.place,'country':i.country} for i in res])
#result
# started time: 2020-07-23 12:33:00.370047
# end time time: 2020-07-23 12:33:00.370151
# diff : 0:00:00.015797

#################################################################################
#celery
from .task import create_random_user_accounts

class CeleryUserCreation(APIView):
    def get(self,request):
        #import ipdb;ipdb.set_trace()
        tot = request.GET.get('tot')
        result=create_random_user_accounts.delay(int(tot))
        return Response("user created...")


class Indexing(APIView):
    def get(self,request):
        #import ipdb;ipdb.set_trace()
        res =Book.objects.filter(pk=request.GET.get('srno'))
        
        return Response(res[0].serial_number)

#################################################################################
#Aggregations
#Aggregate generate result (summary) values over an entire QuerySet
#Annotate generate an independent summary for each object in a QuerySet
from django.db.models import Avg, Max, Min, FloatField, Count
from django.db.models import Q

class BooksQuery(APIView):
    def get(self,request):
        lst=[]
        
        # Total number of books.
        #result['tot_books'] = Books.objects.count()

        # Total number of books with publisher=Kiran
        #result['rk_publisher_tot_books'] = Books.objects.filter(publisher__name='RK Publishers').count()

        # Average price across all books.
        #result['avg_price_all_books'] = Books.objects.all().aggregate(Avg('price')).get('price__avg')

        # Max price across all books.
        #result['max_price_book'] = Books.objects.all().aggregate(Max('price')).get('price__max')

        # Difference between the highest priced book and the average price of all books.
        #not working
        #result['diff_high_avg_book'] = Books.objects.aggregate(price_diff=Max('price', output_field=FloatField()) - Avg('price'))



        # Each publisher, each with a count of books as a "num_books" attribute.
        #import ipdb; ipdb.set_trace()
        # pubs = Publisher.objects.annotate(num_book=Count('books'))
        # for each in pubs:
        #     result={}
        #     result['num_of_book'] = each.num_book
        #     result['each_publisher_num_book'] = each.name
        #     lst.append(result)


        # Each publisher, with a separate count of books with a rating above and below 5
        # above5 = Count('books', filter=Q(books__rating__gt=5))
        # below5 = Count('books', filter=Q(books__rating__lt=5))

        # pubs = Publisher.objects.annotate(above5=above5).annotate(below5=below5)
        # for each in pubs:
        #     d={}
        #     #import ipdb; ipdb.set_trace()
        #     d['above_5_rating'] = each.above5
        #     d['below_5_rating'] = each.below5
        #     d['name'] = each.name
        #     lst.append(d)

        # The top 5 publishers, in order by number of books.
        # pubs = Publisher.objects.annotate(num_book=Count('books')).order_by('-num_book')[:5]
        # for each in pubs:
        #     d={}
        #     #import ipdb; ipdb.set_trace()
        #     d['num_of_book'] = each.num_book
        #     d['pulisher'] = each.name
        #     lst.append(d)
        result={}
        result['cal'] =Books.objects.aggregate(Avg('price'), Max('price'), Min('price'))


        return Response(result)

#################################################################################