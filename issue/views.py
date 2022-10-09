from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from typing import Any
from issue.forms import TaskForm
from issue.models import Task


class TaskListView(TemplateView):
    template_name: str = 'task_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context

class TaskDetailView(TemplateView):
    template_name: str = 'task_detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return context


class TaskUpdateView(TemplateView):
    template_name: str = 'task_update.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form = TaskForm(instance=task)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        form: TaskForm = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
        context = {
            'form': form
        }
        return render(request, 'task_update.html', context)


class TaskAddView(TemplateView):
    template_name: str = 'task_add.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        form = TaskForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form: TaskForm = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('task_detail', pk=task.pk)
        context = {
            'form': form
        }
        return render(request, 'task_add.html', context)


class TaskDeleteView(TemplateView):
    template_name: str = 'task_delete.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        task.delete()       
        return redirect('task_list')
