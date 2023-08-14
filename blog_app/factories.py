from datetime import datetime

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth import get_user_model
from blog_app.models import Image, Post, Comment, Like

fake = Faker()
User = get_user_model()


class CustomUserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class ImageFactory(factory.Factory):
    class Meta:
        model = Image

    title = factory.Faker("sentence")
    photo = factory.django.ImageField(filename="image.jpg")
    type = factory.Faker("random_element", elements=["header", "profile"])


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(CustomUserFactory)
    title = factory.Faker("sentence")
    text = factory.Faker("text")
    description = factory.Faker("sentence")
    photo = factory.django.ImageField(filename="post_image.jpg")
    is_published = factory.Faker("boolean")
    created_at = factory.Faker("date_time_this_decade", tzinfo=None)

    @classmethod
    def create(cls, **kwargs):
        # Ensure that the author is saved before creating the post
        author = kwargs.get("author")
        if author and not author.pk:
            author.save()
        return super().create(**kwargs)


class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(CustomUserFactory)
    text = factory.Faker("paragraph")
    temporary_name = factory.Faker("user_name")
    approval_status = factory.Faker("random_element", elements=["pending", "approved"])
    created_at = factory.LazyFunction(datetime.now)


class LikeFactory(factory.Factory):
    class Meta:
        model = Like

    author = factory.SubFactory(CustomUserFactory)
    post = factory.SubFactory(PostFactory)
