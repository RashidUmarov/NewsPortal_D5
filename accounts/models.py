from django.db import models
from django.contrib.auth.models import User
# from news.models import Post, Comment

# автор поста или статьи
class Author(models.Model):
    full_name = models.CharField(max_length=255)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0, db_column='rating')

    # возвращает рейтинг автора
    @property
    def rating(self):
        return self._rating

    # установить новое значение рейтинга
    def update_rating(self, rating):
        self._rating = rating
        self.save()

    def __str__(self):
        return self.full_name +': '+ str(self.author)

    @rating.setter
    def rating(self, rating):
        self.update_rating(rating)

    def __str__(self):
        fio=self.full_name.split()
        return f'{fio[0][0]}. {fio[1][0]}. {fio[2]}'
"""
        # сначала посчитаем рейтинги за статьи
        articles_rating = 0
        posts = Post.objects.filter(author=self)
        for p in posts:
            articles_rating += p.rating
        articles_rating *= 3

        # теперь рейтинги за комментарии пользователя
        user_comments_rating = 0
        comments = Comment.objects.filter(user=self)
        for c in comments:
            user_comments_rating = c.rating

        # теперь рейтинги за комментарии к статье автора
        post_comments_rating = 0
        for p in posts:
            post_comments = Comment.objects.filter(post=p)
            for c in post_comments:
                post_comments_rating += c.rating
                
        return articles_rating + user_comments_rating + post_comments_rating        
"""
