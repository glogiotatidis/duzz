from django import forms

from models import Comment, Topic


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject']


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
