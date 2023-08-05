from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from .forms import RegistrationForm


class RegistrationView(CreateView):
    template_name = 'registration/form.html'
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
        context['user'] = self.request.user
        return context


def get_image_filenames(request):
    # Replace this list with the actual filenames of your images in the static/images/ directory
    image_filenames = ['site_cover.jpg', 'site_cover2.jpg', 'site_cover3.jpg']

    return JsonResponse({'image_filenames': image_filenames})