import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import CustomUser
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'photo']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Make the 'photo' field not required
        self.fields['photo'].required = False
        self.fields['photo'].widget.clear_checkbox_label = "Delete Photo"

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')


        # Check if a photo is uploaded
        if not photo or isinstance(photo, str):
            return self.instance.photo  # Return the existing photo


        # Check the file size (optional, you can set a maximum size if needed)
        # if photo.size > 5 * 1024 * 1024:  # 5 MB
        #     raise forms.ValidationError("The image size should not exceed 5 MB.")

        return photo


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        try:
            user = CustomUser.objects.get(Q(email=email) & Q(username=username))
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("No user found with this email and username.")

        return cleaned_data

    def save(self, request):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        user = CustomUser.objects.get(Q(email=email) & Q(username=username))

        # Генерируйте новый пароль
        new_password = CustomUser.objects.make_random_password()
        user.set_password(new_password)
        user.save()

        return new_password