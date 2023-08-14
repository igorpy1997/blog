from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import CustomUser, Comment, Post
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "photo"]

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Make the "photo" field not required
        self.fields["photo"].required = False
        self.fields["photo"].widget.clear_checkbox_label = "Delete Photo"

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")

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
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        try:
            user = CustomUser.objects.get(Q(email=email) & Q(username=username))
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("No user found with this email and username.")

        return cleaned_data

    def save(self, request):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")

        user = CustomUser.objects.get(Q(email=email) & Q(username=username))

        # Генерирует новый пароль
        new_password = CustomUser.objects.make_random_password()
        user.set_password(new_password)
        user.save()

        return new_password


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["temporary_name", "text"]
        labels = {
            "text": "",  # Пустий рядок використовується для приховування надписі
            "temporary_name": "",  # Пустий рядок використовується для приховування надписі
        }
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control", "style": "width: 400px; height: 50px;"}),
            "temporary_name": forms.TextInput(attrs={"class": "form-control", "style": "width: 400px; height: 20px;"}),
        }

    def __init__(self, *args, **kwargs):
        custom_user = kwargs.pop("custom_user", None)
        super(CommentForm, self).__init__(*args, **kwargs)

        print("hi", custom_user)
        if custom_user and custom_user.is_authenticated:
            self.fields["temporary_name"].initial = custom_user.username
            self.fields["temporary_name"].widget.attrs["readonly"] = True
        else:
            self.fields["temporary_name"].initial = "anonym_user"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["is_published", "title", "description", "text", "photo"]  # Включаем поля title и photo
        widgets = {
            "is_published": forms.HiddenInput(),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "flex"}),
        }


class PostEditForm(forms.ModelForm):
    delete_photo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Post
        fields = ["is_published", "title", "description", "text", "photo", "delete_photo"]
        widgets = {
            "is_published": forms.HiddenInput(),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control-file"}),
        }


class ContactUsForm(forms.Form):
    name = forms.CharField(
        label="Your Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
    )
    subject = forms.CharField(
        label="Subject",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Message"}),
    )
