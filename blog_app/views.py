import os

from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count, Q
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, UpdateView, ListView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from .forms import RegistrationForm, EditProfileForm, CustomPasswordResetForm, CommentForm, PostForm
from .models import CustomUser, Post, Comment
from django.contrib.auth.forms import PasswordChangeForm

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'user_forms/edit_profile_form.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['password_form'] = PasswordChangeForm(self.request.user)
        return context


    def form_valid(self, form):
        response = super().form_valid(form)

        clear_checkbox_value = self.request.POST.get('photo-clear', False)

        # Проверьте, если чекбокс "photo-clear" выбран
        if clear_checkbox_value == 'on':
            # Если чекбокс "photo-clear" выбран, удаляем и файл фотографии, и информацию о фото из поля "photo"
            if self.object.photo:
                file_path = os.path.relpath(self.object.photo.path, settings.MEDIA_ROOT)

                # Удалить файл фотографии из системы хранения файлов, если он существует
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
                # Удалить информацию о фото из поля "photo" объекта "CustomUser"
                self.object.photo.delete()

        password_form = PasswordChangeForm(self.request.user, self.request.POST)
        print("pasport", password_form.errors)
        if password_form.is_valid():
            # Change the user_forms's password
            new_password = password_form.cleaned_data['new_password1']
            self.request.user.set_password(new_password)
            self.request.user.save()

            # Update the session auth hash to avoid automatic logout
            update_session_auth_hash(self.request, self.request.user)

        # Do any additional processing here if needed
        return response

    def form_invalid(self, form):
        return JsonResponse({
            'status': 'error',
            'message': 'Registration failed.',
            'errors': form.errors.as_json(),  # Convert form errors to JSON
        })



class RegistrationView(CreateView):
    template_name = 'user_forms/registration_form.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('main')  # Замените 'success_page' на URL успешной регистрации

    def form_valid(self, form):
        response = super().form_valid(form)
        # Do any additional processing here if needed
        return response



    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'message': 'Registration failed.', 'errors': form.errors})


class CustomLoginView(LoginView):

    def form_invalid(self, form):
        response = super().form_invalid(form)

        return JsonResponse({'status': 'error', 'message': 'Login failed. Please check your credentials.'})

    def form_valid(self, form):

        response = super().form_valid(form)
        user = self.request.user  # Получаем объект пользователя, который успешно авторизовался
        if user.is_authenticated:
            return redirect("main")
        print(user.is_authenticated)
        return JsonResponse({'status': 'success', 'username': user.username})


class MainPageView(ListView):
    model = Post
    template_name = "main_page.html"
    context_object_name = "posts"
    paginate_by = 10  # Количество постов на странице

    def get(self, request, *args, **kwargs):
        if request.GET.get('ajax') == 'true':
            data = self.get_json_response()
            return JsonResponse({'posts': data}, safe=False)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(comment_count=Count('comment', filter=Q(comment__approval_status='approved')))
        queryset = queryset.order_by('-created_at')
        return queryset

    def get_json_response(self):
        posts = self.get_queryset()
        serialized_posts = []  # Список для хранения сериализованных данных постов

        paginator = Paginator(posts, self.paginate_by)  # Создаем пагинатор
        page_number = self.request.GET.get('page')
        print(page_number)

        current_page = paginator.page(page_number)
        print(self.paginate_by)
        for post in posts:
            serialized_posts.append({
                'id': post.id,
                'author': {
                    'username': post.author.username,
                    'photo_url': post.author.photo.url if post.author.photo else None
                },
                'text': post.text,
                'title': post.title,
                'photo_url': post.photo.url if post.photo else None,
                'likes_count': post.likes.count(),
                'comment_count': post.comment_count,
                'is_liked_by_current_user': self.request.user in post.likes.all(),
                "created_at": post.created_at.strftime("%B %d, %Y %H:%M"),
                'is_paginated': current_page.has_other_pages(),
                'paginate_by': self.paginate_by,
                'page_obj': {
                    'number': current_page.number,  # Номер текущей страницы
                    'paginator': {
                        'num_pages': paginator.num_pages,  # Общее количество страниц
                    },
                    'has_next': current_page.has_next(),  # Добавляем информацию о наличии следующей страницы
                    'next_page_number': current_page.next_page_number() if current_page.has_next() else None,
                    # Добавляем номер следующей страницы

                }

            })
        return serialized_posts


class GetCommentsView(ListView):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 5

    def render_to_response(self, context, **response_kwargs):
        comments_html = render_to_string(self.template_name, context)
        return JsonResponse({'comments_html': comments_html})
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post, approval_status='approved')





class LikePostView(View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            status = 'removed'
        else:
            post.likes.add(request.user)
            status = 'added'

        likes_count = post.likes.count()

        response = JsonResponse({'status': status, 'likes_count': likes_count})
        response.set_cookie('countryCode', value='PL', samesite='None', secure=True)

        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_forms'] = self.request.user
        return context


def get_image_filenames(request):
    # Replace this list with the actual filenames of your images in the static/images/ directory
    image_filenames = ['site_cover.jpg', 'site_cover2.jpg', 'site_cover3.jpg']

    return JsonResponse({'image_filenames': image_filenames})


class CustomPasswordResetView(TemplateView):
    template_name = 'user_forms/password_reset_form.html'

    def get(self, request):
        form = CustomPasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.save(request)
            return JsonResponse({'status': 'success', 'new_password': new_password})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form not valid'})






class AddCommentView(LoginRequiredMixin, FormView):
    form_class = CommentForm
    template_name = 'comment_form.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs['post_id']
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        comment.save()


        return response

    def form_invalid(self, form):
        comment_form_html = render_to_string('comment_form_content.html', {'form': form})
        return JsonResponse({
            'status': 'error',
            'comment_form_html': comment_form_html,
        })

class GetPostView(View):
    def get(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.annotate(approved_comment_count=Count('comment', filter=Q(comment__approval_status='approved'))).get(pk=post_id)
            return render(request, 'post_info.html', {'post': post})
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)


class PostCreateView(LoginRequiredMixin, TemplateView):
    template_name = "post_create.html"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return JsonResponse({'status': 'success', 'message': 'Post created successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is not valid.'})
