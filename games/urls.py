from django.urls import path

from games.apps import GamesConfig
from games.views import GameListView, GameDetailView, BuddyRequestCreateView, BuddyRequestDetailView, \
    BuddyRequestDeleteView, BuddyRequestUpdateView

app_name = GamesConfig.name

urlpatterns = [
    path('', GameListView.as_view(), name='game_list'),
    path('games/<slug:slug>/', GameDetailView.as_view(), name='game_detail'),
    path('games/<slug:slug>/create/', BuddyRequestCreateView.as_view(), name='buddy_request_create'),
    path('games/<slug:slug>/<int:pk>/update/', BuddyRequestUpdateView.as_view(), name='buddy_request_update'),
    path('games/<slug:slug>/<int:pk>/', BuddyRequestDetailView.as_view(), name='buddy_request_detail'),
    path('games/<slug:slug>/<int:pk>/delete/', BuddyRequestDeleteView.as_view(), name='buddy_request_delete'),
]