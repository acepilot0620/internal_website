from django.contrib import admin
from .models import Youtube_result,Search,Instagram_result,Contract,Record,ID_btn

# Register your models here.
admin.site.register(Youtube_result)
admin.site.register(Instagram_result)
admin.site.register(Search)
admin.site.register(Record)
admin.site.register(Contract)
admin.site.register(ID_btn)
