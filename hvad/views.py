""" Translatable-model-aware views for use as a replacement to django.views.generic
    Part of hvad public API.
"""
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView, BaseDeleteView
from django.utils.translation import get_language
from hvad.forms import translatable_modelform_factory

__all__ = ('TranslatableCreateView', 'TranslatableUpdateView', 'TranslatableDeleteView')

#=============================================================================

class TranslatableModelFormMixin(ModelFormMixin):
    ''' ModelFormMixin that works with an TranslatableModelForm in **enforce** mode '''
    query_language_key = 'language'

    def get_language(self):
        """ Return the language to enforce on the form.
            Use request URI's "language=" parameter, defaulting to current language.
        """
        return self.request.GET.get(self.query_language_key) or get_language()

    def get_form_class(self):
        """ Return the form class to use within the view """
        if self.model is not None:
            model = self.model
        elif getattr(self, 'object', None) is not None:
            model = self.object.__class__
        else:
            qs = self.get_queryset()
            model = getattr(qs, 'shared_model', qs.model)

        kwargs = {}
        if self.form_class is not None:
            kwargs['form'] = self.form_class
        return translatable_modelform_factory(self.get_language(), model, **kwargs)

#=============================================================================

class TranslatableBaseCreateView(TranslatableModelFormMixin, ProcessFormView):
    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

class TranslatableCreateView(SingleObjectTemplateResponseMixin, TranslatableBaseCreateView):
    template_name_suffix = '_form'

#=============================================================================

class TranslatableBaseUpdateView(TranslatableModelFormMixin, ProcessFormView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

class TranslatableUpdateView(SingleObjectTemplateResponseMixin, TranslatableBaseUpdateView):
    template_name_suffix = '_form'

#=============================================================================

class TranslatableBaseDeleteView(BaseDeleteView):
    pass

class TranslatableDeleteView(SingleObjectTemplateResponseMixin, TranslatableBaseDeleteView):
    template_name_suffix = '_confirm_delete'
