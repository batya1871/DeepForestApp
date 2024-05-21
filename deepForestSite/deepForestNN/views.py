from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .services import deepForest_service
from .forms import SetImageForm


@login_required
def main(request):
    deepForest_service.clean_image(request.user)
    if request.method == "POST":
        form = SetImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Создаем объект модели, но не сохраняем его в базу данных
            image_data = form.save(commit=False)
            # Выполняем ваш метод анализа
            deepForest_service.initialize_analyze(request.user, image_data)
            return redirect(reverse_lazy('deepForest:results'))
    else:
        form = SetImageForm()
    context = {
        'title': "Главное меню",
        'show_nav': True,
        'form': form
    }
    return render(request, "deepForestNN/main.html", context)


@login_required
def results(request):
    context = deepForest_service.get_result(request.user)
    context['title'] = "Результаты обработки"
    context['show_nav'] = True
    return render(request, 'deepForestNN/results.html', context)
