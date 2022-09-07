from django import forms
from django.forms import fields
from .models import Forum, Comment
from django.contrib.auth.models import User


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']




class PostForm(forms.ModelForm):
    class Meta:
        model = Forum
        # fields = '__all__'
        fields = ['post_title', 'post']

        widgets = {
            'post_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Title"
            }),
            'post': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Post Content"
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Comment here"
            }),
        }