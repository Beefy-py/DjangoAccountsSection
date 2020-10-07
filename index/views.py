from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Person, PersonUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import PersonRegisterForm, PersonLoginForm
from django.core.paginator import Paginator
from django.views.generic import ListView, FormView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib import messages


# Create your views here.
@unauthenticated_user
def user_register(request):
    if request.method == 'POST':
        form = PersonRegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                cd = form.cleaned_data
                new_user = Person.objects.create_user(username=cd['username'], email=cd['email'],
                                                      password=cd['password'],
                                                      first_name=cd['first_name'], last_name=cd['last_name'])
                messages.success(request, f'You are successfully registered as {new_user.username}!')
                return redirect("profile", new_user.id)
    else:
        form = PersonRegisterForm()
    context = {
        'form': form,
        'title': 'Register',
    }
    return render(request, 'index/register.html', context)


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        form = PersonLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Successfully logged in as {request.user}!')
                return redirect('all_users')

    else:
        form = PersonLoginForm()
    context = {
        'form': form,
        'title': 'Login',
    }
    return render(request, 'index/login.html', context)


@login_required(redirect_field_name='user_login', login_url='/login/')
def user_logout(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        messages.warning(request, f'Logged out as {user}!')
        return redirect('all_users')
    return render(request, 'index/logout.html')


@login_required(redirect_field_name='user_login', login_url='/login/')
def profile(request, pk):
    user = Person.objects.get(id=pk)
    context = {
        'user': user,
        'title': 'Profile'
    }
    return render(request, 'index/profile.html', context)


def update_person(request):
    if request.method == 'POST':
        form = PersonUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if form.changed_data:
                messages.success(request, f'Your info is successfully updated!')
            else:
                messages.info(request, f'Nothing is updated.')
            return redirect('profile', request.user.id)
    else:
        form = PersonUpdateForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'index/edit-user.html', context)


class AllUsers(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'user_login'
    model = Person
    template_name = 'index/users.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = Person.objects.all()
        context['title'] = 'All Users'
        return context


def error_404_view(request, exception):
    context = {
        'title': 'PageNotFound'
    }
    return render(request, '404.html', context)


def error_500_view(request):
    context = {
        'title': 'InternalServerError'
    }
    return render(request, '500.html', context)
