from django import forms
from .models import *
from django.forms import modelformset_factory

class QuizForm(forms.ModelForm):
    class Meta:
        model=quiz
        fields=('__all__')
    
    def __init__(self, *args, **kwargs):
        super(QuizForm,self).__init__(*args, **kwargs)
        self.fields['quiztitle'].widget.attrs['onchange']='slugifyQuizTitle(this.value)'

class SingleChoiceForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type', 'marks', 'is_mandatory')
        labels = {
            'correct_answer': 'Correct Answer (Select one option)',
        }

class MultipleChoiceForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type', 'marks', 'is_mandatory')
        labels = {
            'correct_answer': 'Correct Answers (Select one or more options)',
        }

class YesNoForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type', 'marks', 'is_mandatory')
        labels = {
            'correct_answer': 'Correct Answer (Select True or False)',
        }

class ShortAnswerForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type', 'marks', 'is_mandatory')

class LongAnswerForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ('title', 'question_type', 'marks', 'is_mandatory')

class AnswerForm(forms.ModelForm):
    class Meta:
        model = answer
        fields = ('content', 'is_correct')


# Answerformset = modelformset_factory(answer,fields=('content', 'is_correct'),extra=1)
