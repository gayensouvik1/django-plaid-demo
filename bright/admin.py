from django.contrib import admin

# Register your models here.

from .models import Itemtoken, Availablebanks, Usertoken

admin.site.register(Itemtoken)
admin.site.register(Availablebanks)
admin.site.register(Usertoken)