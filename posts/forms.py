from django import forms
from .models import Post,Like , Comment

class PostModelForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('content' , 'image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Add You Comment'}))
    class Meta:
        model = Comment
        fields = ('body',)