import json

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render

from braces.views import LoginRequiredMixin
from django_browserid.views import Verify

from forms import AttachmentsFormset, CommentForm
from models import Attachment, Comment, Topic, DuzzUser
from utils import get_object_or_none


class BrowserIDVerify(Verify):
    def login_failure(self, error=None):
        messages.error(self.request, 'Nope. Login error.')
        return super(BrowserIDVerify, self).login_failure(error)


def home(request):
    if request.user.is_authenticated():
        return redirect('topics')
    return render(request, 'login.html')


class ProfileUpdate(UpdateView):
    model = DuzzUser
    fields = ['full_name', 'avatar']
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('topics')


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    From https://docs.djangoproject.com/en/dev/topics/class-based-views/generic-editing/
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response


class Topics(LoginRequiredMixin, ListView):
    model = Topic
    template_name = 'topics.html'
    context_object_name = 'topics'
    paginate_by = 5


class TopicCreate(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ['subject']
    template_name = 'add.html'

    def form_valid(self, form):
        # Topic form is valid, no validate comment form
        comment_form = CommentForm(self.request.POST)
        if not comment_form.is_valid():
            return self.form_invalid()

        form.instance.creator = self.request.user
        topic = form.save()
        comment_form.instance.topic = topic
        comment_form.instance.creator = self.request.user
        comment_form.save()

        return HttpResponseRedirect(topic.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(TopicCreate, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class Comments(LoginRequiredMixin, CreateView, ListView):
    model = Comment
    template_name = 'detail.html'
    context_object_name = 'comments'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        return super(Comments, self).get(request, *args, **kwargs)

    def get_queryset(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        return Comment.objects.filter(topic=topic)

    def get_context_data(self, **kwargs):
        context = super(Comments, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['attachments_formset'] = AttachmentsFormset()
        context['topic'] = Topic.objects.get(pk=self.kwargs['topic_id'])
        return context

    def form_valid(self, form):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        form.instance.topic = topic
        form.instance.creator = self.request.user
        comment = form.save()
        attachments_formset = AttachmentsFormset(
            self.request.POST, self.request.FILES, instance=comment)
        # attachments_formset.save()

        return HttpResponseRedirect(topic.get_absolute_url())
