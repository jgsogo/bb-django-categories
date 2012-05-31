from django.db import models
from django.core import validators
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey


class CategoryManager(models.Manager):
    def orphan(self):
        """ Retrieves all categories with no parent """
        return self.get_query_set().filter(parent=None)


class Category(MPTTModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True, help_text=_(u'Optional'))

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ['slug']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append( self.title )
        return self.get_separator().join(p_list)

    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p.title)
            more = self._recurse_for_parents(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return ' :: '

    @property
    def breadcrumb(self):
        p_list = self._recurse_for_parents(self)
        return self.get_separator().join(p_list)

    def save(self, *args, **kwargs):
        if not self.id:
            if not len(self.slug.strip()):
                self.slug = slugify(self.title)

        p_list = self._recurse_for_parents(self)
        if self.title in p_list:
            raise validators.ValidationError(_(u'You must not save a category in itself!'))
        super(Category, self).save(*args, **kwargs)


"""
    To be done: base model and generic relation to categorize anything

    class BaseCategorizedItem(models.Model):
        categories = models.ManyToMany(Category)

        class Meta:
            abstract = True

    class CategorizedItemGeneric(BaseCategorizedItem):
        generic...


"""
