import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render

from braces.views import LoginRequiredMixin

from forms import CommentCreateForm, TopicCreateForm
from models import Comment, Topic, DuzzUser
from utils import get_object_or_none


def home(request):
    if request.user.is_authenticated():
        return redirect('topics')
    return render(request, 'base.html')


class ProfileUpdate(UpdateView):
    model = DuzzUser
    fields = ['full_name']
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

    def get_context_data(self, **kwargs):
        context = super(Topics, self).get_context_data(**kwargs)
        context['topic_form'] = TopicCreateForm()
        context['comment_form'] = CommentCreateForm()
        return context


class Comments(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comments'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'comment_include.html'
        return super(Comments, self).get(request, *args, **kwargs)

    def get_queryset(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        after_id = self.request.GET.get('after', 0)
        return Comment.objects.filter(topic=topic, id__gt=after_id)

    def get_context_data(self, **kwargs):
        context = super(Comments, self).get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm()
        context['topic'] = Topic.objects.get(pk=self.kwargs['topic_id'])
        return context


class CommentCreate(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def get(self, request, topic_id):
        return redirect('comments', topic_id=topic_id)

    def get_success_url(self):
        self.kwargs['topic_id'] = self.topic.id
        return reverse('comments', kwargs=self.kwargs)

    def form_valid(self, form):
        user = self.request.user
        if 'topic_id' in self.kwargs:
            self.topic = get_object_or_none(Topic, pk=self.kwargs['topic_id'])
        else:
            topic = Topic(creator=self.request.user)
            self.topic_form = TopicCreateForm(self.request.POST, instance=topic)
            if not self.topic_form.is_valid():
                print "Invalid!"
                raise
            self.topic = self.topic_form.save()

        form.instance.creator = user
        form.instance.topic = self.topic

        return super(CommentCreate, self).form_valid(form)
