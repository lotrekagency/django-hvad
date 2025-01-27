""" Miscellaneous tools used by translation-aware serializers.
    Mostly intended for internal use and third-party modules.
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from hvad.utils import get_cached_translation, set_cached_translation
from django.utils.translation import gettext_lazy as _, get_language, activate

__all__ = ('TranslationListSerializer', )

#=============================================================================

class TranslationListSerializer(serializers.ListSerializer):
    'A custom serializer to output translations in a nice dict'
    many = True
    default_error_messages = {
        'not_a_dict': _('Expected a dictionary of items, but got a {input_type}.'),
        'no_translation': _('At least one translation must be provided.'),
    }

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            message = self.error_messages['not_a_dict'].format(
                input_type=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            })
        if not data:
            message = self.error_messages['no_translation']
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            })

        ret, errors = {}, {}
        instance = self.child.instance
        existing_objects = (
            {
                obj.language_code: obj
                for obj in instance._meta.translations_model.objects.filter(
                    master=instance
                )
            }
            if instance
            else {}
        )
        old_language = get_language()
        for language, translation in data.items():
            activate(language)
            try:
                self.child.instance = existing_objects.get(language)
                validated = self.child.run_validation(translation)
            except ValidationError as exc:
                errors[language] = exc.detail
            else:
                ret[language] = validated
                errors[language] = {}
        activate(old_language)
        if any(errors.values()):
            raise ValidationError(errors)
        return ret

    def get_attribute(self, instance):
        ''' Override get_attribute so it returns the whole translatable model and not just translations '''
        return instance

    def to_representation(self, instance):
        ''' Combine each translation in turn so the serializer has a full object '''
        result = {}
        stashed = get_cached_translation(instance)
        old_language = get_language()
        for translation in getattr(instance, self.source).all():
            activate(translation.language_code)
            set_cached_translation(instance, translation)
            result[translation.language_code] = self.child.to_representation(instance)
        activate(old_language)
        set_cached_translation(instance, stashed)
        return result

    def save(self, *args, **kwargs): #pragma: no cover
        raise NotImplementedError('TranslationList must be nested')
    @property
    def data(self): #pragma: no cover
        raise NotImplementedError('TranslationList must be nested')
    @property
    def errors(self): #pragma: no cover
        raise NotImplementedError('TranslationList must be nested')
