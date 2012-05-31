django-categories
=================

Easy to use and implement app to categorize elements.

**Source**: https://bitbucket.org/jgsogo/django-categories


Installation
------------

Download sources and add them to path

::

    pip install hg+https://bitbucket.org/jgsogo/django-categories


Modify ``settings.py`` to include app

::

    INSTALLED_APPS = (
        ...
        'mptt',
        'categories',
        ...
        )

Usage
-----

On your models add a ``categories`` many-to-many field

::

    from categories.models import Category

    class YourModel(models.Model):
        ...
        categories = models.ManyToManyField(Category)

Use ``CategoriesFormMixin`` on any form to get a checkboxlist to select
categories for your model. For example, you can edit your ``admin.py``
file to something like this

::

    from django.contrib import admin
    from basic.models import BasicModel
    from categories.forms import CategoriesFormMixin

    class CategorizedBasicModelForm(CategoriesFormMixin):
        pass

    class CategorizedPhotoSetAdmin(admin.ModelAdmin):
        form = CategorizedBasicModelForm

    admin.site.register(BasicModel, CategorizedPhotoSetAdmin)


Dependencies
------------

 * `django-mptt`_ - 0.5 (surely works with many others)


License
-------

Are you joking? XD

.. _`django-mptt`: https://github.com/django-mptt/django-mptt
