from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.db.models import JSONField

# Create your models here.
class quiz(models.Model):
    quiztitle=models.CharField(max_length=500,default="Quiz Title",blank=True)
    quizdescription=models.TextField(default="A small description about this quiz.",blank=True)
    quizslug=models.SlugField(max_length=200,null=True)
    datemodified=models.DateTimeField(auto_now=True)
    showquizdetails=models.BooleanField(default=True)
    quiztimelimit=models.IntegerField(default=10)
    ispublished=models.BooleanField(default=True)
    isscored=models.BooleanField(default=False)
    totalscore=models.PositiveIntegerField(default=100,validators=[MinValueValidator(10)],blank=True,null=True)
    passingscore=models.PositiveIntegerField(default=30,validators=[MinValueValidator(0)],blank=True,null=True)
    def clean(self):
        if self.passingscore > self.totalscore:
            raise ValidationError("Passing score must be less than total score.")
        
    def __str__(self):
        return self.quiztitle
    
    def save(self, *args, **kwargs):
        self.quizslug=slugify(self.quizslug)
        super(quiz,self).save(*args, **kwargs)
        
class question(models.Model):
    QUESTION_TYPES = (
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
        ('long_answer', 'Long Answer'),
        ('yes_no', 'Yes/No'),
    )
    quiz=models.ForeignKey(quiz,on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES,blank=True)
    title = models.TextField(default="Question Title")
    placeholder = models.CharField(default="Placeholder text",max_length=100,blank=True, null=True)
    correct_answer=models.TextField(blank=True,null=True)
    marks=models.IntegerField(blank=True,null=True)
    is_mandatory=models.BooleanField(default=False,blank=True)
    questionorder=models.IntegerField(default=0)
    def __str__(self):
        return self.title

class answer(models.Model):
    content=models.TextField(default="Answer",blank=True,null=True)
    is_correct=models.BooleanField(default=False)
    questiontitle=models.ForeignKey(question,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.content


# Take Quiz

class QuizSubmission(models.Model):
    quiz=models.ForeignKey(quiz,on_delete=models.CASCADE,related_name='submissions')
    user=models.CharField(default='Anonymus',max_length=100)
    submission_date=models.DateTimeField(auto_now_add=True)
    attempted_data = models.TextField(default=True,null=True)
    unattempted_data = models.TextField(default=True,null=True)

    def __str__(self):
        return f'Submission for Quiz: {self.quiz.quiztitle} by {self.user}'
    
class UserAnswer(models.Model):
    submission=models.ForeignKey(QuizSubmission,on_delete=models.CASCADE,related_name='answers')
    question_text = models.TextField()
    selected_answer = models.TextField(blank=True,null=True)

    def __str__(self):
        return f'User Answer for Question: {self.question_text}'