from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import *
from django.forms import formset_factory
import json
from django.db import transaction
from conditionalforms import models
from conditionalforms.utils import getUserIp

# Create your views here.
def forms(request):
    context={}
    formlist=form.objects.all()
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    context['formlist']=formlist
    return render(request,"forms.html",context)

def createform(request):
    forminstance=models.form.objects.create()
    models.FormSecuritySettings.objects.create(formId=forminstance)
    models.FormUserInfoSettings.objects.create(formId=forminstance)
    messages.success(request,'Form created successfully! You can now start adding questions and customizing the form settings.')
    return redirect('editform',forminstance.id)

def deleteform(request,id):
    if request.method=="POST":
        forminstance=get_object_or_404(models.form,id=id)
        forminstance.delete()
        messages.success(request,'The form has been successfully deleted.')
    return redirect('formlist')


def editform(request, id,questionid=None):
    context = {}
    projectName = settings.ROOT_URLCONF.split('.')[0]
    formdata = get_object_or_404(models.form, id=id)
    allform = models.form.objects.all().exclude(id=id)
    questions = question.objects.get(form_id=id,id=questionid) if questionid else ''
    allQuestions = question.objects.filter(form_id=id)
    Answerformset = modelformset_factory(answer,fields=('content', 'is_correct'),extra=0)
    if request.method == "POST":
        answer_formset=Answerformset(request.POST,queryset=answer.objects.filter(questiontitle_id=questions.id))
        form = None
        prefix = f'question_{questions.id}'
        if questions.question_type == 'single_choice':
            form = SingleChoiceForm(request.POST, instance=questions, prefix=prefix)
        elif questions.question_type == 'multiple_choice':
            form = MultipleChoiceForm(request.POST, instance=questions, prefix=prefix)
        elif questions.question_type == 'yes_no':
            form = YesNoForm(request.POST, instance=questions, prefix=prefix)
        elif questions.question_type == 'short_answer':
            form = ShortAnswerForm(request.POST, instance=questions, prefix=prefix)
        elif questions.question_type == 'long_answer':
            form = LongAnswerForm(request.POST, instance=questions, prefix=prefix)
        if answer_formset.is_valid():
            answer_formset.save()
        if form is not None and form.is_valid():
            inst=form.save(commit=False)
            if questions.question_type == 'long_answer' or questions.question_type == 'short_answer':
                inst.placeholder=request.POST.get('answer')
            elif questions.question_type == 'multiple_choice':
                inst.correct_answer=request.POST.getlist('answer')
            else:
                inst.correct_answer=request.POST.get('answer')
            inst.save()
            messages.success(request, "Questions updated successfully. Your changes have been saved.")
        else:
            error = form.errors if form else None
            messages.error(request, "Failed to update the form. An error occurred while saving your changes.")
            context['errors'] = error
    else:
        answer_formset=Answerformset(queryset=answer.objects.filter(questiontitle_id=questions.id)) if questions != '' else None

    question_forms = [SingleChoiceForm(instance=questions, prefix=f'question_{questions.id}') if questions.question_type == 'single_choice'
        else MultipleChoiceForm(instance=questions, prefix=f'question_{questions.id}') if questions.question_type == 'multiple_choice'
        else YesNoForm(instance=questions, prefix=f'question_{questions.id}') if questions.question_type == 'yes_no'
        else ShortAnswerForm(instance=questions, prefix=f'question_{questions.id}') if question.question_type == 'short_answer'
        else LongAnswerForm(instance=questions, prefix=f'question_{questions.id}')] if questionid else None
    
    context['allForms'] = allform
    context['questions'] = questions
    context['allQuestions'] = allQuestions
    context['question_forms'] = question_forms
    context['projectName'] = projectName
    context['id'] = id
    context['form'] = formdata
    context['answerforms']=answer_formset
    return render(request, "editform.html", context)


def addquestion(request,id):
    if request.method=="POST":
        formdata=form.objects.get(id=id)
        question_type=request.POST.get('addquestion')
        order=0
        newquestioninstance=question.objects.create(form=formdata,question_type=question_type)
        if question_type=='single_choice':
            answer.objects.create(content="Answer",questiontitle_id=newquestioninstance.id,is_correct=False)
            answer.objects.create(content="Answer",questiontitle_id=newquestioninstance.id,is_correct=False)
        if question_type=='multiple_choice':
            answer.objects.create(content="Answer",questiontitle_id=newquestioninstance.id,is_correct=False)
            answer.objects.create(content="Answer",questiontitle_id=newquestioninstance.id,is_correct=False)
    return redirect('editquestion',id,newquestioninstance.id)

def addanswer(request,formid,questionid):
    answer.objects.create(
        content="Answer",
        questiontitle_id=questionid,
        is_correct=False
    )
    return redirect('editquestion',formid,questionid)

def deletanswer(request,formid,questionid,answerid):
    answer.objects.get(id=answerid).delete()
    return redirect('editquestion',formid,questionid)

def deletequestion(request,questionid):
    if request.method=="POST":
        questioninstance=question.objects.get(id=questionid)
        questioninstanceid=questioninstance.form.id
        questioninstance.delete()
    return redirect('editform',questioninstanceid)

# settings
def formgeneralsettings(request,id):
    context={}
    forminstance=get_object_or_404(models.form,id=id)
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    context['formform']=FormForm(instance=forminstance)
    context['form']=forminstance
    if request.method=="POST":
        form=FormForm(request.POST,instance=forminstance)
        if form.is_valid():
            form.save()
            messages.success(request,"Form updated successfully. Your changes have been saved.")
            return redirect('formgeneralsettings',id)
        else:
            error=form.errors
            messages.error(request,"Failed to update the form. An error occured while saving your changes.")
            context['errors']=error
    return render(request,'settings/formgeneralsettings.html',context)

def formsecuritysettings(request,id):
    context={}
    forminstance=get_object_or_404(models.form,id=id)
    security_setting = models.FormSecuritySettings.objects.get(formId=forminstance)
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    context['formform']=FormForm(instance=forminstance)
    context['form']=forminstance
    context['securitySetting']=SecuritySettingForm(instance=security_setting)
    if request.method=="POST":
        form=SecuritySettingForm(request.POST,instance=security_setting) 
        if form.is_valid():
            form.save()
            messages.success(request,"Form updated successfully. Your changes have been saved.")
            return redirect('formsecuritysettings',id)
        else:
            error=form.errors
            messages.error(request,"Failed to update the form. An error occured while saving your changes.")
            context['errors']=error
    return render(request,'settings/formsecuritysettings.html',context)

def forminformationsettings(request,id):
    context={}
    forminstance=get_object_or_404(models.form,id=id)
    user_info_settings = models.FormUserInfoSettings.objects.get(formId=forminstance)
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    context['formform']=FormForm(instance=forminstance)
    context['form']=forminstance
    context['securitySetting']=UserInfoSettingForm(instance=user_info_settings)
    if request.method=="POST":
        form=UserInfoSettingForm(request.POST,instance=user_info_settings) 
        if form.is_valid():
            form.save()
            messages.success(request,"Form updated successfully. Your changes have been saved.")
            return redirect('forminformationsettings',id)
        else:
            error=form.errors
            messages.error(request,"Failed to update the form. An error occured while saving your changes.")
            context['errors']=error
    return render(request,'settings/forminformationsettings.html',context)

# reports
def formreports(request,form_id):
    context={}
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    form_instance=form.objects.get(id=form_id)
    submissions=models.FormSubmission.objects.filter(form=form_instance)
    context['form']=form_instance
    context['submissions']=submissions
    return render(request,'reports/formreports.html',context)

def detailedreport(request,submission_id,form_id):
    projectName=settings.ROOT_URLCONF.split('.')[0]
    forminstance=get_object_or_404(form,id=form_id)
    submission = get_object_or_404(models.FormSubmission,id=submission_id,form_id=form_id)
    user_answers = submission.answers.all()
    context = {
        'form':forminstance,
        'projectName':projectName,
        'submission':submission,
        'user_answers':user_answers,
    }
    return render(request,'reports/detailed-report.html',context)

# Take form

def formfill(request,slug):
    context={}
    form_instance=models.form.objects.get(formslug=slug)
    security_setting = models.FormSecuritySettings.objects.get(formId=form_instance)
    if not security_setting.allow_multiple_attempts and (models.FormSubmission.objects.filter(user_ip=getUserIp(request)).exists() or models.FormSubmission.objects.filter(user=request.user).exists()):
        context['multiple_attempt_error'] = "You have already submitted the form."
    context['form']=form_instance
    context['security_settings'] = models.FormSecuritySettings.objects.get(formId=form_instance)
    context['user_info_settings'] = models.FormUserInfoSettings.objects.get(formId=form_instance)
    context['allQuestions']=question.objects.filter(form=form_instance)
    return render(request,'form/formfill.html',context)

def submit_form(request, form_id):
    if request.method == 'POST':
        user_info_settings = models.FormUserInfoSettings.objects.get(formId=form_id)
        form_instance = form.objects.get(id=form_id)

        attempted_questions = []
        unattempted_questions = []

        questions = question.objects.filter(form=form_instance)
        submission = models.FormSubmission.objects.create(form=form_instance,user_ip=getUserIp(request),user=request.user)
        for question_item in questions:
            question_id = question_item.id
            selected_answer = request.POST.getlist(f'question_{question_id}', '')

            if selected_answer:
                attempted_questions.append({'question_id': question_id, 'selected_answer': json.dumps(selected_answer)})
            else:
                unattempted_questions.append({'question_id': question_id})
            useranswers = UserAnswer.objects.create(
                        submission=submission,
                        question_text=question_item.title,
                        selected_answer=json.dumps(selected_answer)
                    )

        attempted_data = json.dumps(attempted_questions)
        unattempted_data = json.dumps(unattempted_questions)

        with transaction.atomic():
            # Create a FormSubmission instance
            models.FormSubmission.objects.filter(form=form_instance).update(attempted_data=attempted_data,unattempted_data=unattempted_data)
            context = {
                'attempted_questions': attempted_questions,
                'unattempted_questions' : unattempted_questions,
                'user_answers': UserAnswer.objects.filter(submission=submission),
                'user_info_settings':user_info_settings
            }
            print(UserAnswer.objects.filter(submission=submission))
            messages.success(request, "Form submitted successfully")
            return render(request,'reports/detailed-report.html',context)