from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .api_chat import get_response

class ChatView(TemplateView):
    template_name = "chat/chat.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_response'] = self.request.session.get('last_response', '')
        return context
    
    def post(self, request, *args, **kwargs):
        user_message = request.POST.get('user_message', '')
        api_response = get_response(user_message)
        request.session['last_response'] = api_response
        return HttpResponseRedirect(request.path)