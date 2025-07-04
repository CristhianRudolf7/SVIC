from django.shortcuts import render

# Create your views here.
def chatView(request):
    return render(request, 'chat/chat.html')