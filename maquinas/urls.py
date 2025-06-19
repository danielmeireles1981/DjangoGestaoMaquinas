from django.urls import path
from .views import (
    MaquinaListView, MaquinaDetailView,
    MaquinaCreateView, MaquinaUpdateView,
    ManutencaoListView, ManutencaoDetailView,
    manutencao_create, manutencao_update,
    PecaListView, PecaDetailView,
    PecaCreateView, PecaUpdateView,
    relatorios
)

urlpatterns = [
    path('maquinas/', MaquinaListView.as_view(), name='maquina_list'),
    path('maquinas/<int:pk>/', MaquinaDetailView.as_view(), name='maquina_detail'),
    path('maquinas/novo/', MaquinaCreateView.as_view(), name='maquina_create'),
    path('maquinas/<int:pk>/editar/', MaquinaUpdateView.as_view(), name='maquina_update'),
    path('manutencoes/', ManutencaoListView.as_view(), name='manutencao_list'),
    path('manutencoes/<int:pk>/', ManutencaoDetailView.as_view(), name='manutencao_detail'),
    path('manutencoes/novo/', manutencao_create, name='manutencao_create'),
    path('manutencoes/<int:pk>/editar/', manutencao_update, name='manutencao_update'),
    path('pecas/', PecaListView.as_view(), name='peca_list'),
    path('pecas/<int:pk>/', PecaDetailView.as_view(), name='peca_detail'),
    path('pecas/novo/', PecaCreateView.as_view(), name='peca_create'),
    path('pecas/<int:pk>/editar/', PecaUpdateView.as_view(), name='peca_update'),
    path('relatorios/', relatorios, name='relatorios'),
]
