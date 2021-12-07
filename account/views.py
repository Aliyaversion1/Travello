from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from account.forms import RegistrationForm
from account.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Post
from django.shortcuts import redirect

#favourite
@login_required
def favourite_list(request):
    posts = Post.newmanager.filter(favourites=request.user)
    return render(request, 'favourites.html', locals())



@login_required
def favourite_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
        messages.add_message(request, messages.SUCCESS, 'You remove post from favourites')
        return redirect('homepage')
    else:
        post.favourites.add(request.user)
        messages.add_message(request, messages.SUCCESS, 'You added post to favourites')
        return redirect('homepage')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])




class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'account/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('homepage')
    success_message = 'Аккаунт успешно создан!!!'


class SignInView(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('homepage')


def profile(request):
    return render(request, 'account/profile.html')


