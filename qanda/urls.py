from django.urls import path
from qanda import views

app_name = 'qanda'
urlpatterns = [
    path('ask', views.AskQuestionView.as_view(), name='ask'),
    path('q/<int:pk>', views.QuestionDeatilView.as_view(), name='question_detail'),
    path('q/<int:pk>/answer', views.CreateAnswerView.as_view(), name='answer_question'),
    path('a/<int:pk>/accept', views.UpdateAnswerAcceptance.as_view(), name='update_answer_acceptance'),
]