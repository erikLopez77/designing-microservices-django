# user/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

# Limita a 5 intentos por minuto, bloqueando si se excede
@method_decorator(ratelimit(key='ip', rate='2/m', block=True), name='post')
class SignupView(View):
    template_name = 'signup.html'

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')

    def get(self, request):
        return render(request, self.template_name, {'form': UserCreationForm()})
# En tu archivo de vistas (ej. views.py)
from django.shortcuts import render

def ratelimit_error(request, exception):
    return render(request, 'ratelimited.html', status=429)