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
            user_name = code_form.cleaned_data['user_name']
            size = code_form.cleaned_data['size']
            speed = code_form.cleaned_data['speed']
            context['user_name'] = user_name
            context['code'] = code_form.cleaned_data['code']
            context['size'] = size
            context['speed'] = speed

            # check if it is a high score
            high_score = True
            for score in context['scores']:
                if score.size <= size and score.speed <= speed:
                    high_score = False
                    break

            if high_score:
                # remove any defunct scores
                for score in context['scores']:
                    if score.size >= size and score.speed >= speed:
                        score.delete()

                # create the new high score
                new_score = Score(problem=context['problem'],
                                  user=user_name,
                                  size=size,
                                  speed=speed)
                new_score.save()

                # reset the list of high scores
                context['scores'] = context['problem'].score_set.all()

            context['high_score'] = high_score

            return render(request, 'problems/solution.html', context)
        else:
            context['form'] = code_form
            return render(request, self.template_name, context)
