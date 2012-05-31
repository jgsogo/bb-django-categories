
from django.db import models

from categories.models import Category

class BasicModel(models.Model):
    just_a_field = models.CharField(max_length = 20)

    categories = models.ManyToManyField(Category)
