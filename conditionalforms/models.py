from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.db.models import JSONField

# Create your models here.
class form(models.Model):
    formtitle=models.CharField(max_length=500,default="Form Title",blank=True,db_column="FormTitle")
    formdescription=models.TextField(default="A small description about this form.",blank=True,db_column="FormDescription")
    formslug=models.SlugField(max_length=200,default="form-title",null=True,db_column="FormSlug")
    datemodified=models.DateTimeField(auto_now=True,db_column="DateModified")
    showformdetails=models.BooleanField(default=True,db_column="ShowFormDetails")
    ispublished=models.BooleanField(default=True,db_column="IsPublished")
        
    def __str__(self):
        return self.formtitle
    
    def save(self, *args, **kwargs):
        self.formslug=slugify(self.formslug)
        super(form,self).save(*args, **kwargs)

class FormSecuritySettings(models.Model):
    formId = models.OneToOneField(form,on_delete=models.CASCADE,db_column='FormID')
    allow_logged_in_user = models.BooleanField(default=False,db_column='AllowLoggedInUser')
    allow_multiple_attempts = models.BooleanField(default=False,db_column='AlloWMultipleAttempts')
    display_response = models.BooleanField(default=False,db_column='DisplayResponse')

    def __str__(self):
        return str(self.formId)
    
class FormUserInfoSettings(models.Model):
    InfoPlacement = (
        ('at_start', 'Collect at the Start'),
        ('at_end', 'Collect at the End'),
    )
    formId = models.OneToOneField(form,on_delete=models.CASCADE,db_column='FormID')
    collect_name = models.BooleanField(default=False,db_column='CollectName')
    collect_email = models.BooleanField(default=False,db_column='CollectEmail')
    info_collection_placement = models.CharField(max_length=20, choices=InfoPlacement,blank=True,default="at_start",db_column="InfoCollectionPlacement")

    def __str__(self):
        return self.formId

class question(models.Model):
    QUESTION_TYPES = (
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
        ('long_answer', 'Long Answer'),
        ('yes_no', 'Yes/No'),
    )
    form=models.ForeignKey(form,on_delete=models.CASCADE,db_column="Form")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES,blank=True,db_column="QuestionType")
    title = models.TextField(default="Question Title",db_column="Title")
    placeholder = models.CharField(default="Placeholder text",max_length=100,blank=True, null=True,db_column="Placeholder")
    def __str__(self):
        return self.title

class answer(models.Model):
    content=models.TextField(default="Answer",blank=True,null=True,db_column="Content")
    is_correct=models.BooleanField(default=False,db_column="IsCorrect")
    questiontitle=models.ForeignKey(question,on_delete=models.CASCADE,blank=True,null=True,db_column="QuestionTitle")
    def __str__(self):
        return self.content


# Take Form

class FormSubmission(models.Model):
    form=models.ForeignKey(form,on_delete=models.CASCADE,related_name='submissions',db_column="Form")
    user=models.CharField(default='Anonymous',max_length=100,db_column="User")
    submission_date=models.DateTimeField(auto_now_add=True,db_column="SubmissionDate")
    attempted_data = models.TextField(default=True,null=True,db_column="AttemptedData")
    unattempted_data = models.TextField(default=True,null=True,db_column="UnattemptedData")
    user_ip = models.GenericIPAddressField(db_column="IpAddress")

    def __str__(self):
        return f'Submission for Form: {self.form.formtitle} by {self.user}'
    
class UserAnswer(models.Model):
    submission=models.ForeignKey(FormSubmission,on_delete=models.CASCADE,related_name='answers',db_column="Submission")
    question_text = models.TextField(db_column="QuestionText")
    selected_answer = models.TextField(blank=True,null=True,db_column="SelectedAnswer")

    def __str__(self):
        return f'User Answer for Question: {self.question_text}'