#Django signals:

#1 Step: 

#create default config app file name in __init__.py file
default_app_config = 'yourapplicationname.apps.yourappconfigfilename'

#2 Step: 

#write a function in apps.py and import your config file in that function
def ready(self):
    import yourapplicationname.signals

#3 Step:
#write you signal.py file in your application
from django.db.models.signals import post_save

def yourfunctioname(**kwargs):
    
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        do your logic
        instance.save()

post_save.connect(yourfunctionname, sender = modelname)