from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import *
from django.forms import formset_factory
import json
from django.db import transaction

# Create your views here.
def quizzes(request):
    context={}
    quizlist=quiz.objects.all()
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    context['quizlist']=quizlist
    return render(request,"quizzes.html",context)

def createquiz(request):
    quizinstance=quiz.objects.create()
    messages.success(request,'Quiz created successfully! You can now start adding questions and customizing the quiz settings.')
    return redirect('editquiz',quizinstance.id)

def deletequiz(request,id):
    if request.method=="POST":
        quizinstance=get_object_or_404(quiz,id=id)
        quizinstance.delete()
        messages.success(request,'The quiz has been successfully deleted.')
    return redirect('quizlist')


def editquiz(request, id,questionid=None):
    context = {}
    projectName = settings.ROOT_URLCONF.split('.')[0]
    quizdata = get_object_or_404(quiz, id=id)
    questions = question.objects.get(quiz_id=id,id=questionid) if questionid else ''
    allQuestions = question.objects.filter(quiz_id=id).order_by("questionorder")
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
            messages.error(request, "Failed to update the quiz. An error occurred while saving your changes.")
            context['errors'] = error
    else:
        answer_formset=Answerformset(queryset=answer.objects.filter(questiontitle_id=questions.id)) if questions != '' else None

    question_forms = [SingleChoiceForm(instance=questions, prefix=f'question_{questions.id}') if questions.question_type == 'single_choice'
        else MultipleChoiceForm(instance=questions, prefix=f'question_{questions.id}') if questions.question_type == 'multiple_choice'
        else YesNoForm(instance=questions, prefix=f'question_{questions.id}') if questions.question_type == 'yes_no'
        else ShortAnswerForm(instance=questions, prefix=f'question_{questions.id}') if question.question_type == 'short_answer'
        else LongAnswerForm(instance=questions, prefix=f'question_{questions.id}')] if questionid else None
    
    context['questions'] = questions
    context['allQuestions'] = allQuestions
    context['question_forms'] = question_forms
    context['projectName'] = projectName
    context['id'] = id
    context['quiz'] = quizdata
    context['answerforms']=answer_formset
    return render(request, "editquiz.html", context)


def addquestion(request,id):
    if request.method=="POST":
        quizdata=quiz.objects.get(id=id)
        question_type=request.POST.get('addquestion')
        order=0
        if question.objects.filter(quiz=quizdata).exists():
            order=question.objects.filter(quiz=quizdata).last().questionorder + 1
        newquestioninstance=question.objects.create(quiz=quizdata,question_type=question_type,questionorder=order)
        if question_type=='single_choice':
            answer.objects.create(content="Answer",questiontitle_id=newquestioninstance.id,is_correct=False)
            answer.objects.create(content="Answer",questiontitle_id=newquestioninstance.id,is_correct=False)
        if question_type=='multiple_choice':
            answer.objects.create(content="Answer",questiontitle_id=newquestioninstance.id,is_correct=False)
            answer.objects.create(content="Answer",questiontitle_id=newquestioninstance.id,is_correct=False)
    return redirect('editquestion',id,newquestioninstance.id)

def addanswer(request,quizid,questionid):
    answer.objects.create(
        content="Answer",
        questiontitle_id=questionid,
        is_correct=False
    )
    return redirect('editquestion',quizid,questionid)

def deletanswer(request,quizid,questionid,answerid):
    answer.objects.get(id=answerid).delete()
    return redirect('editquestion',quizid,questionid)

def deletequestion(request,questionid):
    if request.method=="POST":
        questioninstance=question.objects.get(id=questionid)
        questioninstanceid=questioninstance.quiz.id
        questioninstance.delete()
    return redirect('editquiz',questioninstanceid)

def HandleQuestionSort(request):
    if request.method == 'POST':
        reorderedData=json.loads(request.body)
        for entries in reorderedData['order']:
            question.objects.filter(id=entries['element']).update(questionorder=entries['index'])
    return HttpResponse("Reorder completed")

# settings
def quizgeneralsettings(request,id):
    context={}
    quizinstance=get_object_or_404(quiz,id=id)
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    context['quizform']=QuizForm(instance=quizinstance)
    context['quiz']=quizinstance
    if request.method=="POST":
        form=QuizForm(request.POST,instance=quizinstance)
        if form.is_valid():
            form.save()
            messages.success(request,"Quiz updated successfully. Your changes have been saved.")
            return redirect('quizgeneralsettings',id)
        else:
            error=form.errors
            messages.error(request,"Failed to update the quiz. An error occured while saving your changes.")
            context['errors']=error
    return render(request,'settings/quizgeneralsettings.html',context)

def quizsecuritysettings(request,id):
    context={}
    quizinstance=get_object_or_404(quiz,id=id)
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    context['id']=id
    context['quiz']=quizinstance
    return render(request,'settings/quizsecuritysettings.html',context)

def quizquestionsettings(request,id):
    context={}
    projectName=settings.ROOT_URLCONF.split('.')[0]
    quizinstance=get_object_or_404(quiz,id=id)
    context['projectName']=projectName
    context['id']=id
    context['quiz']=quizinstance
    return render(request,'settings/quizquestionsettings.html',context)

def quizinformationsettings(request,id):
    context={}
    projectName=settings.ROOT_URLCONF.split('.')[0]
    quizinstance=get_object_or_404(quiz,id=id)
    context['projectName']=projectName
    context['id']=id
    context['quiz']=quizinstance
    return render(request,'settings/quizinformationsettings.html',context)

# reports
def quizreports(request,quiz_id):
    context={}
    projectName=settings.ROOT_URLCONF.split('.')[0]
    context['projectName']=projectName
    quiz_instance=quiz.objects.get(id=quiz_id)
    submissions=QuizSubmission.objects.filter(quiz=quiz_instance)
    context['quiz']=quiz_instance
    context['submissions']=submissions
    return render(request,'reports/quizreports.html',context)

def detailedreport(request,submission_id,quiz_id):
    projectName=settings.ROOT_URLCONF.split('.')[0]
    quizinstance=get_object_or_404(quiz,id=quiz_id)
    submission = get_object_or_404(QuizSubmission,id=submission_id,quiz_id=quiz_id)
    user_answers = submission.answers.all()
    context = {
        'quiz':quizinstance,
        'projectName':projectName,
        'submission':submission,
        'user_answers':user_answers,
    }
    return render(request,'reports/detailed-report.html',context)

# Take quiz

def takequiz(request,slug):
    context={}
    quiz_instance=quiz.objects.get(quizslug=slug)
    context['quiz']=quiz_instance
    context['allQuestions']=question.objects.filter(quiz=quiz_instance).order_by('questionorder')
    return render(request,'quiz/takequiz.html',context)

def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz_instance = quiz.objects.get(id=quiz_id)
        attempted_questions = []
        unattempted_questions = []

        questions = question.objects.filter(quiz=quiz_instance)

        for question_item in questions:
            question_id = question_item.id
            selected_answer = request.POST.get(f'question_{question_id}', '')
            print(f'question_{question_id}')

            if selected_answer:
                attempted_questions.append({'question_id': question_id, 'selected_answer': selected_answer})
            else:
                unattempted_questions.append({'question_id': question_id})

        attempted_data = json.dumps(attempted_questions)
        unattempted_data = json.dumps(unattempted_questions)

        with transaction.atomic():
            # Create a QuizSubmission instance
            submission = QuizSubmission.objects.create(quiz=quiz_instance,attempted_data=attempted_data,unattempted_data=unattempted_data)

            # Process and store user answers
            for question_id, answer_text in request.POST.items():
                if question_id.startswith('question_'):
                    question_id = question_id.lstrip('question_')
                    question_item = question.objects.get(id=question_id)
                    UserAnswer.objects.create(
                        submission=submission,
                        question_text=question_item.title,
                        selected_answer=answer_text
                    )

            messages.success(request, "Quiz submitted successfully")
            return redirect('quizreports', quiz_id)