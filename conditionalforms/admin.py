from django.contrib import admin
from .models import *

# Register your models here.
class formAdmin(admin.ModelAdmin):
    prepopulated_fields = {"formslug": ("formtitle",)}
admin.site.register(form,formAdmin)
admin.site.register(question)
admin.site.register(answer)
admin.site.register(FormSubmission)
admin.site.register(UserAnswer)
admin.site.register(FormSecuritySettings)
admin.site.register(FormUserInfoSettings)