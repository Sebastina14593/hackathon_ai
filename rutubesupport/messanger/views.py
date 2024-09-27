from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from messanger.models import Chat
from .gigachat_assistent import gigachat_response

def requestsmenu(request):
    user_requests = Chat.objects.order_by('created_at')
    return render(request, 'messanger/requestsmenu.html', {"requests": user_requests})

def messanger(request, pk):
    chats = Chat.objects.filter(pk=pk)
    if request.method == 'POST':
        # Обработка данных, отправленных через POST запрос
        response_emp = request.POST.get("response_emp")
        if chats.exists():  # Проверяем, что чат существует
            chat = chats.first()
            chat.response_emp = response_emp
            chat.save()

            # Возврат ответа в формате JSON
            return JsonResponse({'response_emp': response_emp})
        else:
            return JsonResponse({'error': 'Chat not found'}, status=404)

    # Если запрос не POST, просто отобразить шаблон
    return render(request, 'messanger/messanger.html', {'chats': chats})
