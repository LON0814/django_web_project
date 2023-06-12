from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Game, Genre_list, Comment
from .forms import GameCreateForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class GameDetailView(DetailView):
    template_name = 'game/game_detail.html'
    model = Game
class GameCreateView(CreateView):
    template_name = 'game/game_create.html'
    form_class = GameCreateForm

    def get_success_url(self):
        return reverse('game:detail', args=[self.object.pk])

class GameUpdateView(UpdateView):
    template_name = 'game/game_update.html'
    form_class = GameCreateForm
    model = Game

    def get_success_url(self):
        return reverse('game:detail', args=[self.object.pk])

def game_delete(request, pk):
    game = Game.objects.get(pk=pk)
    game.delete()
    return redirect(reverse('game:list'))

def game_list(request):
    paginate_by = 7;
    context = {}

    context['is_paginated']=True

    all_games = Game.objects.all()
    paginator = Paginator(all_games, paginate_by)
    page_number_range = 5
    current_page = int(request.GET.get('page', 1))
    context['current_page']=current_page

    start_index = int((current_page-1)/page_number_range)*page_number_range
    end_index = start_index + page_number_range

    current_page_group_range = paginator.page_range[start_index : end_index]
    print("current_page_group_range", current_page_group_range)

    start_page = paginator.page(current_page_group_range[0])
    end_page = paginator.page(current_page_group_range[-1])

    has_previous_page = start_page.has_previous()
    has_next_page = end_page.has_next()

    context['current_page_group_range'] = current_page_group_range
    if has_previous_page:
        context['has_previous_page'] = has_previous_page
        context['previous_page'] = start_page.previous_page_number

    if has_next_page:
        context['has_next_page'] = has_next_page
        context['next_page'] = end_page.next_page_number

    e = paginate_by * current_page
    s = e - paginate_by
    print("내용 index", s, e)
    game_list = Game.objects.all()[s:e]

    genre_list = Genre_list.objects.all()
    context['genre_list'] = genre_list
    context['game_list'] = game_list

    return render(request, 'game/game_list.html', context)

def game_search(request):
    paginate_by = 7
    context = {}
    game_list = Game.objects.all()

    b = request.GET.get('b','')
    f = request.GET.getlist('f')


    if f:
        print(f)
        query = Q()
        for i in f:
            query = query | Q(genre__icontains=i)
            game_list = game_list.filter(query)
    if b:
        print(b)
        game_list = game_list.filter(Q(title__icontains=b) | Q(developer__icontains=b))
    context['is_paginated'] = True

    paginator = Paginator(game_list, paginate_by)
    page_number_range = 5
    current_page = int(request.GET.get('page', 1))
    context['current_page'] = current_page

    start_index = int((current_page-1)/page_number_range)*page_number_range
    end_index = start_index + page_number_range

    current_page_group_range = paginator.page_range[start_index : end_index]
    print("current_page_group_range", current_page_group_range)

    start_page = paginator.page(current_page_group_range[0])
    end_page = paginator.page(current_page_group_range[-1])

    has_previous_page = start_page.has_previous()
    has_next_page = end_page.has_next()

    context['current_page_group_range'] = current_page_group_range
    if has_previous_page:
        context['has_previous_page'] = has_previous_page
        context['previous_page'] = start_page.previous_page_number

    if has_next_page:
        context['has_next_page'] = has_next_page
        context['next_page'] = end_page.next_page_number()

    genre_list = Genre_list.objects.all()
    context['genre_list'] = genre_list

    e = paginate_by * current_page
    s = e - paginate_by
    print("내용 index", s, e)

    game_list = game_list[s:e]
    context['game_list'] = game_list

    return render(request, 'game/game_search.html', context)

@login_required(login_url='common:login')
def comment_write(request,pk):
    if request.method == 'POST':
        post = get_object_or_404(Game, pk=pk)
        content = request.POST.get('content')
        conn_user = request.user
        Comment.objects.create(post=post, comment_writer=conn_user, comment_contents=content)
        return redirect(reverse('game:detail', args=[pk]))
@login_required(login_url='common:login')
def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    game_pk = comment.post.pk

    if comment.comment_writer == User.objects.get(username = request.user.get_username()):
        comment.delete()
        return redirect(reverse('game:detail', args=[game_pk]))
    else :
        return redirect(request, 'game/game_detail.html', {'comment':comment, "auth_error":"'해당댓글에 대한 삭제 권한이 없습니다."})

@login_required(login_url='common:login')
def like(request, pk):
    game = get_object_or_404(Game, id=pk)

    if request.user in game.like_users.all():
        game.like_users.remove(request.user)
    else:
        game.like_users.add(request.user)

    return redirect('game:detail', pk = pk)