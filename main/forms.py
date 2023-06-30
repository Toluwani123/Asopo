from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Creator, EndUser, Post, Bid
from django.contrib.auth.models import User


class UserTypeForm(forms.Form):
    user_type = forms.ChoiceField(
        choices=[("creator", "Creator"), ("end_user", "End User")],
        widget=forms.Select(attrs={"class": "form-control"})
    )

class UserCreate(UserCreationForm):
    username = forms.CharField(
        label="",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = [
            "profession",
            "description",
            "location",
            "contact_email",
            "contact_phone",
            "website",
        ]

class CreateBid(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = {"project", "bidder"}


class EndUserForm(forms.ModelForm):
    class Meta:
        model = EndUser
        fields = ["phone_number", "address", 'required']


class CreatorPostForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Project Title"}
        ),
    )
    content = forms.CharField(
        label = "Project Content",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": ""}
        )
    )
   
    class Meta:
        model = Post
        exclude = {"creator", "created_at", 'closed', 'payed'}
