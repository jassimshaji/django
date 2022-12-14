from pyexpat import model
from re import template
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Choices, Questions

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Questions.objects.order_by('-pub_date')[:5]    

class DetailView(generic.DetailView):
    model = Questions
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Questions
    template_name = "polls/result.html"

def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choices_set.get(pk=request.POST['choice'])
    except (KeyError, Choices.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))
