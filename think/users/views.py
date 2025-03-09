from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .forms import LoginUserForms


# Create your views here.


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForms(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'],  password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('posts'))
#     else:
#         form = LoginUserForms()
#
#     return render(request, 'users/logging.html', {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForms
    template_name = 'users/logging.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('posts')


