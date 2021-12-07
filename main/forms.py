from django import forms
from main.models import CommentPost, Image, Post
from datetime import datetime


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ('text',)


class AddPostForm(forms.ModelForm):
    created = forms.DateField(initial=datetime.now().strftime('%Y-%m-%d'))

    class Meta:
        model = Post
        exclude = ('user',)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)