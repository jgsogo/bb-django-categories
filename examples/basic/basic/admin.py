
from django.contrib import admin
from basic.models import BasicModel
from categories.forms import CategoriesFormMixin

class CategorizedBasicModelForm(CategoriesFormMixin):
    pass

class CategorizedPhotoSetAdmin(admin.ModelAdmin):
    form = CategorizedBasicModelForm

admin.site.register(BasicModel, CategorizedPhotoSetAdmin)
