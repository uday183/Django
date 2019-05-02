from int_app.models import Address,UserDetails
from django import template
register = template.Library()




@register.simple_tag
def getAddress(usr_pk):
    #import ipdb; ipdb.set_trace()
    data = UserDetails.objects.get(pk=usr_pk).address.all()
    return data