from django import forms
from django.utils.translation import ugettext_lazy as _

from categories.models import Category

class CategoriesFormMixin(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(required = False, queryset = Category.objects.all(), widget = forms.CheckboxSelectMultiple(), help_text = _(u'Categories for this item'))

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance', None):
            initial = kwargs.get('initial', {})
            initial['categories'] = kwargs['instance'].categories.all().values_list('id', flat = True)
            kwargs['initial'] = initial
        queryset = kwargs.pop('queryset', None)
        super(CategoriesFormMixin, self).__init__(*args, **kwargs)
        if queryset:
            self.fields['categories'].queryset = queryset

    def save(self, force_insert = False, force_update = False, commit = True):
        instance = super(CategoriesFormMixin, self).save(commit = False)

        old_m2m = self.save_m2m
        def save_m2m():
            if old_m2m:
                old_m2m()
            instance.categories.clear()
            for category in self.cleaned_data['categories']:
                instance.categories.add(category)

        if commit:
            instance.save()
            save_m2m()
        else:
            self.save_m2m = save_m2m
        return instance

