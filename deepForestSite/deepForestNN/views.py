from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .services import deepForest_service


@login_required
def main(request):
    if request.method == "POST":
        deepForest_service.initialize_analyze(request.user)
        return redirect(reverse_lazy('deepForest:results'))
    context = {
        'title': "Главное меню",
        'show_nav': True
    }
    return render(request, "deepForestNN/main.html", context)


@login_required
def results(request):
    context = deepForest_service.get_result(request.user)
    context['title'] = "Результаты обработки"
    context['show_nav'] = True
    return render(request, 'deepForestNN/results.html', context)
