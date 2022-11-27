from django.db import models
from accounts.models import Author
from django.contrib.auth.models import User
from django.urls import reverse

# категория публикации - пост или статья
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


# публикация
class Post(models.Model):
    news = 'NEWS'
    article = 'ART'
    TYPES = [
        (news, 'news'),
        (article, 'article')
    ]
    message_type = models.CharField(max_length=4,
                                    choices=TYPES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # message_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, through='PostCategory')

    # превью длиною 124 символа
    def preview(self):
        # print(f'content length = {len(self.content)}')
        length = min(len(self.content), 121)
        # print(f'content length={length}')
        return self.content[:length] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += - 1
        self.save()

    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'

    # возвращает рейтинг автора
    @property
    def type(self):
        return self.get_message_type_display()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += - 1
        self.save()

    def __str__(self):
        return f'{self.user.title()}: {self.text[:20]}'


def calculate_ratings():
    # получим всех авторо
    authors = Author.objects.all()
    for a in authors:
        # сначала посчитаем рейтинги за статьи
        articles_rating = 0
        print(a)
        posts = Post.objects.filter(author=a)
        for p in posts:
            # берем только статьи
            if p.message_type == Post.article:
                articles_rating += p.rating
        articles_rating *= 3
        print(f'{p.id}: articles_rating={articles_rating}')

        user = a.author_id
        # теперь рейтинги за комментарии пользователя
        user_comments_rating = 0
        comments = Comment.objects.filter(user_id=user)
        for c in comments:
            user_comments_rating += c.rating

        print(f'{a.id}: user_comments_rating={user_comments_rating}')

        # теперь рейтинги за комментарии к статье автора
        post_comments_rating = 0
        for p in posts:
            # берем только статьи
            if p.message_type == Post.article:
                # возьмем все комменты к статье
                post_comments = Comment.objects.filter(post=p)
                for c in post_comments:
                    post_comments_rating += c.rating
        print(f'{a}: post_comments_rating={post_comments_rating}')

        rating = articles_rating + user_comments_rating + post_comments_rating
        print(f'{a.id}: rating={rating}')
        a.update_rating(rating)
