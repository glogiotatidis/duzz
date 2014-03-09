from django import forms
from django.forms.models import inlineformset_factory

from models import Attachment, Comment, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['content']

