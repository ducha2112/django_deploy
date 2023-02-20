from django.shortcuts import render, get_object_or_404,redirect
from .models import News,Message
from datetime import date
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.forms import MessageFromUser
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# def home(request):
#     # news = [
#     #     {
#     #         'title': 'Наша новая статья',
#     #         'text': 'Полный текст статьи',
#     #         'date':'1 января 2030 года',
#     #         'author': 'Джон'
#     #     },
#     #       {
#     #         'title': 'Наша вторая статья',
#     #         'text': 'Полный текст статьи',
#     #         'date':'10 января 2030 года',
#     #
#     #     }
#     # ]
#     number = 50
#     data = {
#         'news':News.objects.all(),
#         'title':'Главная страница'
#     }
#     return render(request,'blog/home.html',data)

class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 4

    def get_context_data(self, **kwards):
        ctx = super(ShowNewsView, self).get_context_data(**kwards)

        ctx['title'] = 'Главная страница сайта'
        return ctx

class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author=user).order_by('-date')


    def get_context_data(self, **kwards):
        ctx = super(UserAllNewsView, self).get_context_data(**kwards)

        ctx['title'] = f"Статьи от пользователя {self.kwargs.get('username')}"
        return ctx

class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)

        ctx['title'] = News.objects.get(pk=self.kwargs['pk'])
        return ctx


    # template_name = 'blog/news_detail.html' можно не передавать, т.к. по умолчанию берется News и detail jотимени класса
    # context_object_name = 'post'

class UpdateNewsView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'blog/create_news.html'

    fields = ['title','text']

    def get_context_data(self, **kwards):
        ctx = super(UpdateNewsView, self).get_context_data(**kwards)

        ctx['title'] = 'Обновление статьи'
        ctx['btn_text'] = 'Обновить статью'
        return ctx

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return  True
        return False

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class DeleteNewsView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = News
    success_url = '/'
    template_name = 'blog/delete_news.html'
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return  True
        return False



class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'blog/create_news.html'

    fields = ['title','text']

    def get_context_data(self, **kwards):
        ctx = super(CreateNewsView, self).get_context_data(**kwards)

        ctx['title'] = 'Добавление статьи'
        ctx['btn_text'] = 'Добавить статью'
        return ctx

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def kontakty(request,**kwargs):
    dateToday = date.today().strftime('%d/%m/%Y')
    if request.method == 'POST':
        form = MessageFromUser(request.POST)
        if form.is_valid():
            form.save()
            subject = form.cleaned_data.get('theme')
            plain_message = form.cleaned_data.get('text')
            from_email = f" от {form.cleaned_data.get('email')}"
            to = 'ducha2112@gmail.com'
            send_mail(subject,plain_message, from_email,[to])
            messages.success(request, f'Сообщение успешно отправлено')
            return redirect('home')
    else:
        form=MessageFromUser()


    return render(request,'blog/kontakty.html',{
            'date': dateToday,
            'title': 'Страница контакты',
            'form': form
        })

# def about(request):
#     return HttpResponse('<h3>Страница про нас</h3>')

