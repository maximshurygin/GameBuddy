from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Max, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from chat.forms import MessageForm
from chat.models import Message, Chat
from users.models import User


# Create your views here.


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user).annotate(
            last_message_time=Max('messages__timestamp')
        ).prefetch_related('participants', 'messages').order_by('-last_message_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for chat in context['chats']:
            chat.last_message = chat.messages.order_by('-timestamp').first()
            chat.other_participant = chat.participants.exclude(id=self.request.user.id).first()
        return context


class ChatView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chat/chat.html'
    context_object_name = 'chat'

    def get_object(self):
        chat_id = self.kwargs.get('pk')
        return get_object_or_404(Chat, id=chat_id, participants=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.object
        context['messages'] = Message.objects.filter(chat=chat).order_by('timestamp')
        context['form'] = MessageForm()
        context['other_user'] = chat.participants.exclude(id=self.request.user.id).first()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()

        unread_messages = self.object.messages.filter(is_read=False).exclude(sender=request.user)
        unread_messages.update(is_read=True)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = self.object
            message.sender = request.user
            message.save()
        return redirect(reverse('chat:chat_detail', kwargs={'pk': self.object.id}))


class GetMessagesView(LoginRequiredMixin, ListView):
    model = Message
    paginate_by = 20  # Количество сообщений на странице

    def get_queryset(self):
        chat = get_object_or_404(Chat, id=self.kwargs['chat_id'], participants=self.request.user)
        queryset = Message.objects.filter(chat=chat).select_related('sender').order_by('-timestamp')
        return queryset

    def render_to_response(self, context, **response_kwargs):
        messages = context['object_list']
        message_list = [
            {
                'sender': msg.sender.nickname if msg.sender else "Удаленный пользователь",
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            } for msg in messages
        ]
        return JsonResponse({
            'messages': message_list,
            'has_next': context['page_obj'].has_next() if 'page_obj' in context else False,
            'page_number': context['page_obj'].number if 'page_obj' in context else 1,
            'total_pages': context['paginator'].num_pages if 'paginator' in context else 1
        })


class StartChatView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)

        # Проверка, существует ли уже чат между этими пользователями
        chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()

        if not chat:
            # Создаём новый чат
            chat = Chat.objects.create()
            chat.participants.add(request.user, other_user)

        return redirect(reverse('chat:chat_detail', kwargs={'pk': chat.id}))
