from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView

from qanda.forms import QuestionForm, AnswerForm, AnswerAcceptedForm
from qanda.models import Question

from django.http import HttpResponseBadRequest


# Create your views here.

class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'qanda/ask.html'

    def get_initial(self):
        return {
            'user' : self.request.user.id
        }
    
    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            #save and redirect
            return super().form_valid(form)

        elif action == "PREVIEW":
            preview = Question(
                question=form.cleaned_data['question'],
                title=form.cleaned_data['title'])
            ctx = self.get_context_data(preview=preview)
            return self.render_to_response(context=ctx)

        return HttpResponseBadRequest()

class QuestionDeatilView(DetailView):
    model = Question

    ACCEPT_FORM = AnswerAcceptedForm(initial={'accepted':True})
    REJECT_FORM = AnswerAcceptedForm(initial={'acccepted':False})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'answer_form': AnswerForm(initial={
                'user':self.request.user.id,
                'question': self.object.id,
            })
        })
        if self.object.can_accept_answers(self.request.user):
            ctx.update({
                'accept_form': self.ACCEPT_FORM,
                'reject_form': self.REJECT_FORM,
            })
        return ctx

class CreateAnswerView(LoginRequiredMixin, CreateView):
    form_class = AnswerForm
    template_name = 'qanda/create_answer.html'

    def get_initial(self):
        return {
            'question':self.get_question().id,
            'user': self.request.user.id,
        }
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(question=self.get_question(), **kwargs)

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == "SAVE":
            return super().form_valid(form)

        elif action == "PREVIEW":
            ctx = self.get_context_data(preview=form.cleaned_data['answer'])
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()

    def get_question(self):
        return Question.objects.get(pk=self.kwargs['pk'])
