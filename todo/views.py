from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, FormView, DetailView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse

from .forms import CreateTodoForm
from .models import Todo, Comment, ShareTodo
from .utils import get_user_by_email_or_username, get_secs_until_10_minutes_before
from .tasks import send_todo_reminder


class TodoListView(LoginRequiredMixin, ListView):
    template_name = 'todo/index.html'
    context_object_name = 'todos'

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user) | \
            Todo.objects.filter(sharetodo__with_user=self.request.user)


class TodoCreateView(LoginRequiredMixin, FormView):
    form_class = CreateTodoForm
    template_name = 'todo/todo_create.html'
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        todo = Todo(name=data['name'],
                    description=data['description'],
                    deadline=data['deadline'])
        todo.author = self.request.user
        todo.save()
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(get_secs_until_10_minutes_before(todo.deadline))
        send_todo_reminder.apply_async(
            args=(self.request.user.email, todo.name),
            countdown=get_secs_until_10_minutes_before(todo.deadline)
        )
        return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = 'todo'
    template_name = 'todo/todo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TodoDetailView, self).get_context_data(**kwargs)
        instance = self.object
        if self.request.user != instance.author:
            share_obj = ShareTodo.objects.filter(todo=instance, with_user=self.request.user)
            share_obj = share_obj.last() if share_obj.exists() else None
            if share_obj and not share_obj.comment_allowed:
                context['comment_allowed'] = False
            else:
                context['comment_allowed'] = True
        else:
            context['comment_allowed'] = True
        context['comment_list'] = instance.comment_set.all().order_by('-created_at')
        context['todo_id'] = instance.pk
        return context


class CommentCreateView(LoginRequiredMixin, FormView):
    template_name = 'todo/comments.html'

    def post(self, request, *args, **kwargs):
        text = request.POST.get('text', False)
        related_todo_id = request.POST.get('todo_id', False)
        todo_queryset = Todo.objects.filter(pk=related_todo_id)
        if not todo_queryset.exists():
            return JsonResponse({
                'error': 'true',
                'msg': 'Invalid task object'
            })
        else:
            todo_obj = todo_queryset.last()
        if todo_obj.author != request.user:
            share_obj = ShareTodo.objects.filter(todo=todo_obj, with_user=self.request.user)
            share_obj = share_obj.last() if share_obj.exists() else None
            if share_obj and not share_obj.comment_allowed:
                return JsonResponse({
                    'error': 'true',
                    'msg': 'Unauthorized'
                })
            return JsonResponse({
                'error': 'true',
                'msg': 'Unauthorized'
            })

        if text and not text.isspace():
            Comment.objects.create(todo=todo_obj, author=request.user, text=text)
            comment_list = todo_obj.comment_set.all().order_by('-created_at')
            return render(request, self.template_name, {
                'comment_list': comment_list,
                'todo_id': todo_obj.pk,
                'comment_allowed': True
            })


class TodoDeleteView(UserPassesTestMixin, DeleteView):
    model = Todo
    success_url = '/'

    def test_func(self):
        todo = Todo.objects.get(pk=self.kwargs['pk'])
        return self.request.user == todo.author


class ShareTodoView(LoginRequiredMixin, FormView):
    def post(self, request, *args, **kwargs):
        todo_id = request.POST.get('todo_id', False)
        with_user = request.POST.get('user', False)
        allow_comment = request.POST.get('allow_comment', False)
        user_obj = get_user_by_email_or_username(with_user)
        if not user_obj:
            return JsonResponse({
                'msg': 'Invalid user'
            })
        allow_comment = True if allow_comment == 'checked' else False
        todo = Todo.objects.get(pk=todo_id)
        if todo.author != self.request.user:
            return JsonResponse({
                'msg': 'Unauthorized'
            })
        share_obj, created = ShareTodo.objects.get_or_create(todo=todo,
                                                             with_user=user_obj)
        if not created:
            return JsonResponse({
                'msg': 'This task already shared with {}'.format(user_obj.username)
            })
        else:
            share_obj.comment_allowed = allow_comment
            share_obj.save()
        return JsonResponse({
            'success': 'true'
        })
