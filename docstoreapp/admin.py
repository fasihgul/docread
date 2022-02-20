from django.contrib import admin


from .models import *

admin.site.register(Topics)
admin.site.register(Folder)
admin.site.register(Documents)