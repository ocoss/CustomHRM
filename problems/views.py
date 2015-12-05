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
        context['form'] = CodeForm({'problem_slug':name_slug,})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        code_form = CodeForm(request.POST)
        if code_form.is_valid():
            context['user_name'] = code_form.cleaned_data['user_name']
            context['code'] = code_form.cleaned_data['code']
            context['size'] = code_form.cleaned_data['size']
            context['speed'] = code_form.cleaned_data['speed']

            return render(request, 'problems/solution.html', context)
        else:
            context['form'] = code_form
            return render(request, self.template_name, context)
