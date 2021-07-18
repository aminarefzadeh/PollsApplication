from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Choice


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.template'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        queryset = Question.objects.filter(pub_date__lte=timezone.now())
        if 'query' in self.request.GET and self.request.GET['query']:
            queryset = queryset.filter(question_text__icontains=self.request.GET['query'])
        """Return the last five published questions."""
        return queryset.order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'detail.template'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'results.template'


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question_id in request.session.get('voted_ids', []):
        return HttpResponse('You voted before', status=400)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return HttpResponse('Invalid choice', status=400)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        voted_ids = request.session.get('voted_ids') or []
        voted_ids.append(question_id)
        request.session['voted_ids'] = voted_ids
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
