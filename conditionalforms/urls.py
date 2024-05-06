from django.urls import path
from . import views

# app_name='form'

urlpatterns=[
    path("",views.forms,name="formlist"),
    path("create-form/",views.createform,name="createform"),
    path("delete-form/<int:id>",views.deleteform,name="deleteform"),
    path("edit-form/<int:id>/<int:questionid>",views.editform,name="editquestion"),
    path("edit-form/<int:id>/",views.editform,name="editform"),
    path("addquestion/<int:id>",views.addquestion,name="addquestion"),
    path("adddelete/<int:questionid>",views.deletequestion,name="deletequestion"),
    path("addanswer/<int:formid>/<int:questionid>",views.addanswer,name="addanswer"),
    path("deleteanswer/<int:formid>/<int:questionid>/<int:answerid>",views.deletanswer,name="deleteanswer"),
    # Settings
    path("form-general-settings/<int:id>",views.formgeneralsettings,name="formgeneralsettings"),
    path("form-security-settings/<int:id>",views.formsecuritysettings,name="formsecuritysettings"),
    path("form-information-settings/<int:id>",views.forminformationsettings,name="forminformationsettings"),
    # reports
    path("form-reports/<int:form_id>",views.formreports,name="formreports"),
    path("form-reports-detailed/<int:submission_id>/<int:form_id>",views.detailedreport,name="formdetailedreports"),
    # Take form
    path("form/<slug:slug>",views.formfill,name="formfill"),
    path("submit-form/<int:form_id>",views.submit_form,name="submit_form")
]