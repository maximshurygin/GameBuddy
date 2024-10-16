from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from games.forms import BuddyRequestForm
from games.models import Game, BuddyRequest


# Create your views here.


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buddy_requests'] = BuddyRequest.objects.filter(game=self.object).order_by('-created_at')
        return context


class BuddyRequestCreateView(CreateView):
    model = BuddyRequest
    form_class = BuddyRequestForm
    template_name = 'games/request_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = get_object_or_404(Game, slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        game = get_object_or_404(Game, slug=self.kwargs['slug'])
        form.instance.user = self.request.user  # Устанавливаем пользователя
        form.instance.game = game  # Устанавливаем игру
        self.object = form.save()  # Сохраняем заявку
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('games:buddy_request_detail', kwargs={'slug': self.object.game.slug, 'pk': self.object.pk})


class BuddyRequestUpdateView(UpdateView):
    model = BuddyRequest
    form_class = BuddyRequestForm
    template_name = 'games/request_update.html'

    def get_success_url(self):
        return reverse('games:buddy_request_detail', kwargs={
            'slug': self.object.game.slug,
            'pk': self.object.pk
        })


class BuddyRequestDetailView(DetailView):
    model = BuddyRequest
    template_name = 'games/request_detail.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class BuddyRequestDeleteView(DeleteView):
    model = BuddyRequest
    template_name = 'games/request_delete.html'
    success_url = reverse_lazy('games:game_list')  # ПОДУМАТЬ КУДА НАПРАВЛЯТЬ ПОСЛЕ УДАЛЕНИЯ
