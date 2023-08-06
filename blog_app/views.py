import os

from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.files.storage import default_storage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import TemplateView, UpdateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from .forms import RegistrationForm, EditProfileForm, CustomPasswordResetForm
from .models import CustomUser
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



class MainPageView(TemplateView):
    template_name = "main_page.html"


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


