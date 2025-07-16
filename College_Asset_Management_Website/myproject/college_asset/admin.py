from django.contrib import admin

# Register your models here.
from .models import RegisteredAsset, Classroom, ClassroomAsset

admin.site.register(RegisteredAsset)
admin.site.register(Classroom)
admin.site.register(ClassroomAsset)