from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from problems.models import Problem, Test, Score
from problems.forms import CodeForm


class HomeView(generic.TemplateView):
    template_name = 'problems/home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['problems'] = Problem.objects.all()
        return context


class ProblemView(generic.TemplateView):
    template_name = 'problems/problem.html'

    def get_context_data(self, **kwargs):
        context = super(ProblemView, self).get_context_data(**kwargs)
        name_slug = self.kwargs['name_slug']
        problem = get_object_or_404(Problem, name_slug=name_slug)
        context['problem'] = problem
        context['scores'] = problem.score_set.all()
        context['form'] = CodeForm()
        return context

    def post(self, request, *args, **kwargs):
        code_form = CodeForm(request.POST)
        context = self.get_context_data(**kwargs)
        if code_form.is_valid():
            user_name = code_form.cleaned_data['user_name']
            #TODO: create score and add it if it is a high score

            return HttpResponseRedirect(reverse('solution', \
                    args=(self.kwargs['name_slug'],)))
        else:
            context['form'] = code_form
            return render(request, self.template_name, context)


class SolutionView(generic.TemplateView):
    template_name = 'problems/solution.html'

    def get_context_data(self, **kwargs):
        context = super(SolutionView, self).get_context_data(**kwargs)
        name_slug = self.kwargs['name_slug']
        problem = get_object_or_404(Problem, name_slug=name_slug)
        context['problem'] = problem
        context['scores'] = problem.score_set.all()
        return context
