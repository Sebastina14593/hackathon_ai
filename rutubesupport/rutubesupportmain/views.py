from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .forms import FormResultForm
from messanger.models import Chat
from messanger.gigachat_assistent import gigachat_response
def index(request): # HttpRequest
    if request.method == 'POST':
        form = FormResultForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            chat = Chat.objects.order_by('-id')[:1][0]
            chat.chat_number=chat.id
            chat.response_giga = gigachat_response(chat.problem_description + " " + chat.detailed_description)
            chat.save()
            return redirect('home')# редирект на страницу успешного выполнения
    else:
        form = FormResultForm()  # Создаем пустую форму для GET-запросов

    return render(request, 'rutubesupportmain/index.html', {'form': form})

def userchat(request): # HttpRequest
    return HttpResponse('''<h1>Чат пользователя</h1>''')

def userrequests(request, request_id): # HttpRequest
    return HttpResponse(f'''<h1>Обращения пользователя</h1><p>id: {request_id}</p>''')

def emprequests(request): # HttpRequest
    return HttpResponse('''<h1>Обращения сотрудника</h1>''')
def empchat(request): # HttpRequest
    return HttpResponse('''<h1>Чат сотрудника</h1>''')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('requestsmenu')
        else:
            error_message = 'Некорректное имя пользователя или пароль'
            return render(request, 'rutubesupportmain/login.html', {'error_message': error_message})

    else:
        return render(request, 'rutubesupportmain/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('home')
            except:
                error_message = 'Ошибка при создании аккаунта'
                return render(request, 'rutubesupportmain/register.html', {'error_message': error_message})
        else:
            error_message = 'Пароли не совпали'
            return render(request, 'rutubesupportmain/register.html', {'error_message': error_message})
    return render(request, 'rutubesupportmain/register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')