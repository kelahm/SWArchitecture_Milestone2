from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(UserBalance)
admin.site.register(OwnedStock)
admin.site.register(History)