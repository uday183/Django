from django.contrib import admin
from .models import Book, Author, Publisher, Books, Store 
# Register your models here.

admin.site.register(Book)

# admin.site.register(Author)
# admin.site.register(Publisher)
# admin.site.register(Books)
# admin.site.register(Store)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ('name',)
    list_per_page = 50

admin.site.register(Author,AuthorAdmin)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = ('name',)
    list_per_page = 50

admin.site.register(Publisher,PublisherAdmin)

class BooksAdmin(admin.ModelAdmin):
    list_display = ('id','name','pages','price','rating','author','publisher','pubdate')
    search_fields = ('name','rating')
    list_editable = ('rating','price')
    list_per_page = 30

    def author(self, obj):
        return "\n".join([a.name for a in obj.authors.all()])

admin.site.register(Books,BooksAdmin)

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id','name','get_books')
    search_fields = ('name','get_books')
    list_per_page = 50

    def get_books(self, obj):
        return "\n".join([b.name for b in obj.books.all()])


admin.site.register(Store,StoreAdmin)