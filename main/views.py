from datetime import timedelta
from django.urls import reverse_lazy
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import CommentPost, Image
from .forms import AddPostForm, CommentForm, ImageForm
from django.views.generic import ListView, DetailView
from .models import Category, Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect


class HomePageView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 3

    # pagination
    def get_template_names(self):
        template_name = super(HomePageView, self).get_template_names()
        search = self.request.GET.get('query')
        filter = self.request.GET.get('filter')
        if search:
            template_name = 'search.html'
        elif filter:
            template_name = 'new.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('query')
        filter = self.request.GET.get('filter')
        if search:
            context['posts'] = Post.objects.filter(Q(title__icontains=search)|
                                                   Q(description__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=1)
            context['posts'] = Post.objects.filter(created__gte=start_date)
        else:
            context['posts'] = Post.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'detail_list.html'
    context_object_name = 'category'
    form = CommentForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category_id=self.slug)
        return context


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    image = post.get_image
    images = post.posts.exclude(image=image)
    total_likes = post.get_total_likes()
    return render(request, 'post-detail.html', locals())


def post_single(request, pk):
    post = get_object_or_404(Post, pk=pk)
    image = post.get_image
    images = post.posts.exclude(image=image)
    comment = CommentPost.objects.filter(post=post)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = form.save(commit=False)
            comm.user = request.user
            comm.post = post
            comm.save()

    else:
        form = CommentForm()
    return render(request, "post-detail.html", locals())





@login_required(login_url='login')
def add_post(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5, extra=4)
    if request.method == 'POST':
        post_form = AddPostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            for form in formset.cleaned_data:
                image = form['image']

                Image.objects.create(image=image, posts=post)
            return redirect(post.get_absolute_url())
    else:
        post_form = AddPostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add_post.html', locals())


@login_required(login_url='login')
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
        post_form = AddPostForm(request.POST or None, instance=post)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(posts=post))
        if post_form.is_valid() and formset.is_valid():
            post = post_form.save()

            for form in formset:
                image = form.save(commit=False)
                image.posts = post
                image.save()
            return redirect(post.get_absolute_url())
        return render(request, 'update-post.html', locals())
    else:
        return HttpResponse('<h1>Вы не являетесь создателем этого поста!!!<h1>')


@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        if request.method == 'POST':
            post.delete()
            messages.add_message(request, messages.SUCCESS, 'You delete your blog')
            return redirect('homepage')
        return render(request, 'delete-post.html')
    else:
        return HttpResponse('<h1>Вы не являетесь создателем этого поста!!!<h1>')


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse_lazy('post-detail', args=[str(pk)]))



