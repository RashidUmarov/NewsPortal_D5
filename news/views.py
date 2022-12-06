from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
# модуль для отправки почты
from django.core.mail import send_mail
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from NewsPaper.settings import DAILY_POST_LIMIT


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    # model = Post
    # возьмем только статьи, потому что постов мало
    queryset = Post.objects.filter(message_type=Post.news)  # Post.news)
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-created'

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # момент на сутки назад
        prev_day = datetime.utcnow() - timedelta(days=7)
        # количество постов с этого момента
        user = self.request.user
        posts_day_count = posts_day_count = Post.objects.filter(created__gte=prev_day, author__author=user).count()
        context['allow_post'] = (posts_day_count < DAILY_POST_LIMIT)
        return context

    paginate_by = 10  # вот так мы можем указать количество записей на странице


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранная новость
    context_object_name = 'post'


class PostSearch(ListView):
    # возьмем только статьи, потому что постов мало
    model = Post
    # queryset = Post.objects.filter(message_type=Post.news)  # Post.news)
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-created'

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search'

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        return context

    paginate_by = 10  # вот так мы можем указать количество записей на странице


# Добавляем новое представление для создания поста.
class PostCreate(LoginRequiredMixin, CreateView):
    # raise_exception = True
    permission_required = ('news.add_post',)
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # момент на сутки назад
        prev_day = datetime.utcnow() - timedelta(days=7)
        # количество постов с этого момента
        user = self.request.user
        posts_day_count = posts_day_count = Post.objects.filter(created__gte=prev_day, author__author=user).count()
        context['allow_post'] = (posts_day_count < DAILY_POST_LIMIT)
        return context


    # def post(self, request, *args, **kwargs):
    #     print(f'request = {request}')
    #     print(f'categories={request.POST["categories"]}')
    #     post = Post(
    #         message_type=request.POST['message_type'],
    #         author=Author.objects.get(pk=request.POST['author']),
    #         title=request.POST['title'],
    #         content=request.POST['content'],
    #         # created=request.POST['created'],
    #         postcategory=request.POST["categories"],
    #         # вместо поля categories используем имя промежуточной таблицы PostCategory
    #     )
    #
    #     send_mail(
    #         subject=post.title,  # имя клиента и дата записи будут в теме для удобства
    #         message=post.content,  # сообщение с кратким описанием проблемы
    #         from_email='ivanpomata@yandex.ru',
    #         # здесь указываете почту, с которой будете отправлять (об этом попозже)
    #         recipient_list=['vypusk2015class11a@yandex.ru']
    #         # здесь список получателей. Например, секретарь, сам врач и т. д.
    #     )
    #
    #     return super().post(request, *args, **kwargs)


# Добавляем представление для изменения публикации.
class PostUpdate(LoginRequiredMixin, UpdateView):
    # raise_exception = True
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление удаляющее публикацию
class PostDelete(LoginRequiredMixin, DeleteView):
    # raise_exception = True
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


# списко публикаций по указанной категории
class PostsByCategory(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # queryset = Post.objects.filter(category =Post.news)
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-created'

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'categories_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'category_posts_list'

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        # Получаем обычный запрос
        queryset = Post.objects.filter(categories=self.category).order_by('-created')
        # Возвращаем из функции отфильтрованный список постов
        return queryset

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

    paginate_by = 10  # вот так мы можем указать количество записей на странице


class ArticlesList(ListView):
    queryset = Post.objects.filter(message_type=Post.article)  # Post.news)
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-created'
    template_name = 'articles.html'
    context_object_name = 'articles'

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        return context

    paginate_by = 10  # количество записей на странице


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку о новых публикациях в категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
