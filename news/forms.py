from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'message_type',
            'author',
            'categories',
        ]
        labels={'title':('Заголовок'),
                'content':('Текст'),
                'message_type':('Тип'),
                'author':('Автор'),
                'categories':('Категория')}
        help_texts={'title':('Укажите заголовок статьи или поста'),
                'content':('Введите текст'),
                'message_type':('Выберите тип публикации'),
                'author':('Укажите автора'),
                'categories':('Можно выбрать несколько категорий')}

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        if content is not None and len(content) < 20:
            raise ValidationError({
                "content": "Сообщение не может быть менее 20 символов."
            })

        return cleaned_data