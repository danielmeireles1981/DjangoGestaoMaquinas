from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Maquina
from .models import Manutencao, PecaUtilizada
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from .forms import ManutencaoForm
from .models import Setor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Peca
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Maquina, Setor, Manutencao, TipoManutencao
from django.db.models import Count, Sum
from datetime import datetime

# Contexto para as views que precisam de setores
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['setores'] = Setor.objects.all()
    return context

# Lista todas as máquinas
class MaquinaListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        setor = self.request.GET.get('setor')
        if status:
            queryset = queryset.filter(status=status)
        if setor:
            queryset = queryset.filter(setor__id=setor)
        return queryset

    model = Maquina
    template_name = 'maquinas/maquina_list.html'
    context_object_name = 'maquinas'

# Detalhes de uma máquina
class MaquinaDetailView(LoginRequiredMixin, DetailView):
    model = Maquina
    template_name = 'maquinas/maquina_detail.html'
    context_object_name = 'maquina'

# Cadastro de nova máquina
class MaquinaCreateView(LoginRequiredMixin, CreateView):
    model = Maquina
    template_name = 'maquinas/maquina_form.html'
    fields = ['nome', 'numero_patrimonio', 'setor', 'fabricante', 'fornecedor',
              'data_aquisicao', 'status', 'observacoes', 'imagem']
    success_url = reverse_lazy('maquina_list')

# Edição de máquina
class MaquinaUpdateView(LoginRequiredMixin, UpdateView):
    model = Maquina
    template_name = 'maquinas/maquina_form.html'
    fields = ['nome', 'numero_patrimonio', 'setor', 'fabricante', 'fornecedor',
              'data_aquisicao', 'status', 'observacoes', 'imagem']
    success_url = reverse_lazy('maquina_list')

# Listar manutenções
class ManutencaoListView(LoginRequiredMixin,ListView):
    model = Manutencao
    template_name = 'maquinas/manutencao_list.html'
    context_object_name = 'manutencoes'

# Detalhes de manutenção
class ManutencaoDetailView(LoginRequiredMixin, DetailView):
    model = Manutencao
    template_name = 'maquinas/manutencao_detail.html'
    context_object_name = 'manutencao'

# Criar e Editar Manutenção com peças utilizadas (inline formset)
ManutencaoPecaFormSet = inlineformset_factory(
    Manutencao, PecaUtilizada,
    fields=('peca', 'quantidade'),
    extra=1, can_delete=True
)

from django.shortcuts import render, redirect, get_object_or_404

@login_required
def manutencao_create(request):
    if request.method == "POST":
        form = ManutencaoForm(request.POST)
        formset = ManutencaoPecaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            manutencao = form.save()
            formset.instance = manutencao
            formset.save()
            return redirect('manutencao_list')
    else:
        form = ManutencaoForm()
        formset = ManutencaoPecaFormSet()
    return render(request, 'maquinas/manutencao_form.html', {'form': form, 'formset': formset})

@login_required
def manutencao_update(request, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk)
    if request.method == "POST":
        form = ManutencaoForm(request.POST, instance=manutencao)
        formset = ManutencaoPecaFormSet(request.POST, instance=manutencao)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('manutencao_list')
    else:
        form = ManutencaoForm(instance=manutencao)
        formset = ManutencaoPecaFormSet(instance=manutencao)
    return render(request, 'maquinas/manutencao_form.html', {'form': form, 'formset': formset})


class PecaListView(LoginRequiredMixin,ListView):
    model = Peca
    template_name = 'maquinas/peca_list.html'
    context_object_name = 'pecas'

class PecaDetailView(LoginRequiredMixin, DetailView):
    model = Peca
    template_name = 'maquinas/peca_detail.html'
    context_object_name = 'peca'

class PecaCreateView(LoginRequiredMixin, CreateView):
    model = Peca
    template_name = 'maquinas/peca_form.html'
    fields = ['nome', 'fabricante', 'codigo', 'descricao']
    success_url = reverse_lazy('peca_list')

class PecaUpdateView(LoginRequiredMixin, UpdateView):
    model = Peca
    template_name = 'maquinas/peca_form.html'
    fields = ['nome', 'fabricante', 'codigo', 'descricao']
    success_url = reverse_lazy('peca_list')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'maquinas/home.html'

from django.shortcuts import render
from .models import Maquina, Setor, Manutencao, TipoManutencao
from django.db.models import Count, Sum

@login_required
def relatorios(request):
    # Filtros recebidos da tela
    setor_id = request.GET.get('setor')
    ano = request.GET.get('ano')

    setores = Setor.objects.all()
    tipos = TipoManutencao.objects.all()
    anos = Manutencao.objects.dates('data', 'year')

    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    # Relatório: Quantidade de máquinas por setor
    maq_qs = Maquina.objects.all()
    if setor_id:
        maq_qs = maq_qs.filter(setor_id=setor_id)
    maq_por_setor = maq_qs.values('setor__nome').annotate(total=Count('id'))

    # Relatório: Manutenções por tipo
    manut_qs = Manutencao.objects.all()
    if ano:
        manut_qs = manut_qs.filter(data__year=ano)
    manut_por_tipo = manut_qs.values('tipo__nome').annotate(total=Count('id'))

    # Relatório: Custo total de manutenção por mês no ano escolhido
    manut_por_mes = []
    if ano:
        for mes in range(1, 13):
            total = manut_qs.filter(data__month=mes).aggregate(soma=Sum('custo'))['soma'] or 0
            manut_por_mes.append(float(total))

    # Relatório: Custo de manutenção CONCLUÍDA por máquina
    custo_manutencao_por_maquina = (
        Manutencao.objects
        .filter(status='concluida')
        .values('maquina__nome', 'maquina__numero_patrimonio')
        .annotate(total=Sum('custo'))
        .order_by('-total')
    )
    if setor_id:
        custo_manutencao_por_maquina = custo_manutencao_por_maquina.filter(maquina__setor_id=setor_id)

    context = {
        'setores': setores,
        'tipos': tipos,
        'anos': [a.year for a in anos],
        'meses': meses,
        'maq_por_setor': list(maq_por_setor),
        'manut_por_tipo': list(manut_por_tipo),
        'manut_por_mes': manut_por_mes,
        'custo_manutencao_por_maquina': list(custo_manutencao_por_maquina),
        'filtros': {
            'setor': setor_id,
            'ano': ano,
        }
    }
    return render(request, 'maquinas/relatorios.html', context)
