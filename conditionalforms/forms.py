from django import forms
from .models import *
from django.forms import modelformset_factory

class FormForm(forms.ModelForm):
    class Meta:
        model=form
        fields=('__all__')
    
    def __init__(self, *args, **kwargs):
        super(FormForm,self).__init__(*args, **kwargs)
        self.fields['formtitle'].widget.attrs['onchange']='slugifyFormTitle()'

class SingleChoiceForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type')
        labels = {
            'correct_answer': 'Correct Answer (Select one option)',
        }

class MultipleChoiceForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type')
        labels = {
            'correct_answer': 'Correct Answers (Select one or more options)',
        }

class YesNoForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type')
        labels = {
            'correct_answer': 'Correct Answer (Select True or False)',
        }

class ShortAnswerForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type')

class LongAnswerForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type')

class AnswerForm(forms.ModelForm):
    class Meta:
        model = answer
        fields = ('content', 'is_correct')


class SecuritySettingForm(forms.ModelForm):
    class Meta:
        model=FormSecuritySettings
        fields=('allow_logged_in_user','allow_multiple_attempts','display_response')

class UserInfoSettingForm(forms.ModelForm):
    class Meta:
        model=FormUserInfoSettings
        fields=('info_collection_placement','collect_name','collect_email')

# Answerformset = modelformset_factory(answer,fields=('content', 'is_correct'),extra=1)
