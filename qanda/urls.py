from django.urls import path
from qanda import views

app_name = 'qanda'
urlpatterns = [
    path('ask', views.AskQuestionView.as_view(), name='ask'),
]