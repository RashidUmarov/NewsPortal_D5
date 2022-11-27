from django_filters import FilterSet, DateTimeFilter, ModelMultipleChoiceFilter, CharFilter
from django.forms import DateTimeInput
from .models import Post, Category


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    post_title=CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит',
    )

    created_after = DateTimeFilter(
        field_name='created',
        lookup_expr='gt',
        label='Публикация не ранее',
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs = {'type': 'date'}, ),)

    categories = ModelMultipleChoiceFilter(
        field_name='postcategory__category', #нет такого параметра
        label='Категория',
        #lookup_expr='exact', нет такого параметра
        queryset=Category.objects.all(),
        conjoined=False,
        #empty_label='Любая' #  - это только для ModelChoiceFilter
    )
"""
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по заголовку
            'title': ['icontains'],
            # категория
            # 'postcategory__category':['exact'],
            'categories': ['exact',],
        }
"""
