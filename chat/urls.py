from django.urls import path

from chat import views
from chat.apps import ChatConfig
from chat.views import InboxView, ChatView, GetMessagesView, StartChatView

app_name = ChatConfig.name


urlpatterns = [
    path('', InboxView.as_view(), name='inbox'),
    path('chat/<int:pk>/', ChatView.as_view(), name='chat_detail'),  # исправляем chat_id на pk
    path('get_messages/<int:chat_id>/', GetMessagesView.as_view(), name='get_messages'),
    path('start_chat/<int:user_id>/', StartChatView.as_view(), name='start_chat'),
]