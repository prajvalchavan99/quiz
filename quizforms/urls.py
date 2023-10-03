from django.urls import path
from . import views

# app_name='quiz'

urlpatterns=[
    path("",views.quizzes,name="quizlist"),
    path("create-quiz/",views.createquiz,name="createquiz"),
    path("delete-quiz/<int:id>",views.deletequiz,name="deletequiz"),
    path("edit-quiz/<int:id>/<int:questionid>",views.editquiz,name="editquestion"),
    path("edit-quiz/<int:id>/",views.editquiz,name="editquiz"),
    path("addquestion/<int:id>",views.addquestion,name="addquestion"),
    path("adddelete/<int:questionid>",views.deletequestion,name="deletequestion"),
    path("addanswer/<int:quizid>/<int:questionid>",views.addanswer,name="addanswer"),
    path("deleteanswer/<int:quizid>/<int:questionid>/<int:answerid>",views.deletanswer,name="deleteanswer"),
    path("reorder-questions",views.HandleQuestionSort,name="reorderquestions"),
    # Settings
    path("quiz-general-settings/<int:id>",views.quizgeneralsettings,name="quizgeneralsettings"),
    path("quiz-security-settings/<int:id>",views.quizsecuritysettings,name="quizsecuritysettings"),
    path("quiz-question-settings/<int:id>",views.quizquestionsettings,name="quizquestionsettings"),
    path("quiz-information-settings/<int:id>",views.quizinformationsettings,name="quizinformationsettings"),
    # reports
    path("quiz-reports/<int:quiz_id>",views.quizreports,name="quizreports"),
    path("quiz-reports-detailed/<int:submission_id>/<int:quiz_id>",views.detailedreport,name="quizdetailedreports"),
    # Take quiz
    path("quiz/<slug:slug>",views.takequiz,name="takequiz"),
    path("submit-quiz/<int:quiz_id>",views.submit_quiz,name="submit_quiz")
]