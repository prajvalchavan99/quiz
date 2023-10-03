from django.contrib import admin
from .models import *

# Register your models here.
class quizAdmin(admin.ModelAdmin):
    prepopulated_fields = {"quizslug": ("quiztitle",)}
admin.site.register(quiz,quizAdmin)
admin.site.register(question)
admin.site.register(answer)
admin.site.register(QuizSubmission)
admin.site.register(UserAnswer)