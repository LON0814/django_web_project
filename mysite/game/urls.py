from django.urls import path
from .import views

app_name = 'game'
urlpatterns = [
    path('<int:pk>/detail/', views.GameDetailView.as_view(), name='detail'),
    path('create/', views.GameCreateView.as_view(), name='game_create'),
    path('<int:pk>/update/', views.GameUpdateView.as_view(), name='game_update'),
    path('<int:pk>/delete/', views.game_delete, name='game_delete'),
    path('<int:pk>/comment/write/', views.comment_write, name='comment_write'),
    path('<int:pk>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('<int:pk>/like/', views.like, name='like'),
    path('list/', views.game_list, name='list'),
    path('search/', views.game_search, name='search'),
]


