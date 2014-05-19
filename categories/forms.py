from django import forms
from django.utils.translation import ugettext_lazy as _

from categories.models import Category


class CategoriesFormMixin(forms.ModelForm):
    _model_field_name = 'categories'

    #_categories = forms.ModelMultipleChoiceField(required = False, queryset = Category.objects.choices(), widget = forms.CheckboxSelectMultiple(), help_text = CATEGORIES_HELP)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        user = kwargs.pop('user', None)
        super(CategoriesFormMixin, self).__init__(*args, **kwargs)

        # Form template
        self.fields[self._model_field_name].widget = forms.CheckboxSelectMultiple()
        help_text = _("%(model_field)s for this item") % {'model_field': self.Meta.model._meta.get_field_by_name(self._model_field_name)[0].verbose_name}
        self.fields[self._model_field_name].help_text = help_text.capitalize()

        # Queryset
        if queryset:
            self.fields[self._model_field_name].queryset = queryset
        else:
            self.fields[self._model_field_name].queryset = Category.objects.choices(user)

        if kwargs.get('instance', None):
            instance_categories_qs = getattr(kwargs['instance'], self._model_field_name)
            self.fields[self._model_field_name].initial = instance_categories_qs.all().values_list('id', flat = True)

    """
    def save(self, force_insert = False, force_update = False, commit = True):
        instance = super(CategoriesFormMixin, self).save(commit = False)

        old_m2m = self.save_m2m
        def save_m2m():
            if old_m2m:
                old_m2m()
            fildset = getattr(instance, self._model_field_name)
            fildset.clear()
            for category in self.cleaned_data['_categories']:
                fildset.add(category)

        if commit:
            instance.save()
            save_m2m()
        else:
            self.save_m2m = save_m2m
        return instance
    """
