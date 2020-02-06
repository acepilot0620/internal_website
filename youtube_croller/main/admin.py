from django.contrib import admin
from .models import Youtube_result,Search,Instagram_result,Contract,Record

# Register your models here.
admin.site.register(Youtube_result)
admin.site.register(Instagram_result)
admin.site.register(Search)
admin.site.register(Record)
admin.site.register(Contract)
