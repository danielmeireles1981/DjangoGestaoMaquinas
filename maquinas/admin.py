from django.contrib import admin
from .models import (
    Setor, Fabricante, Fornecedor,
    Maquina, TipoManutencao,
    Manutencao, Peca, PecaUtilizada
)

# Inline para exibir peças utilizadas diretamente na manutenção
class PecaUtilizadaInline(admin.TabularInline):
    model = PecaUtilizada
    extra = 1

# Admin de Manutenção
@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ('maquina', 'tipo', 'data', 'status', 'responsavel', 'custo')
    list_filter = ('status', 'tipo', 'data', 'maquina')
    search_fields = ('descricao', 'responsavel', 'maquina__nome')
    inlines = [PecaUtilizadaInline]
    date_hierarchy = 'data'
    autocomplete_fields = ['maquina', 'tipo']

# Admin de Máquina
@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'numero_patrimonio', 'setor', 'fabricante', 'fornecedor', 'data_aquisicao', 'status')
    list_filter = ('status', 'setor', 'fabricante', 'fornecedor')
    search_fields = ('nome', 'numero_patrimonio')
    autocomplete_fields = ['setor', 'fabricante', 'fornecedor']

# Admin de Setor
@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'localizacao', 'responsavel')
    search_fields = ('nome', 'responsavel')

# Admin de Fabricante
@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'contato', 'site')
    search_fields = ('nome',)

# Admin de Fornecedor
@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'contato', 'cnpj', 'email')
    search_fields = ('nome', 'cnpj')

# Admin de Tipo de Manutenção
@admin.register(TipoManutencao)
class TipoManutencaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# Admin de Peça
@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'fabricante', 'codigo')
    search_fields = ('nome', 'codigo')
    autocomplete_fields = ['fabricante']

# Admin de Peça Utilizada
@admin.register(PecaUtilizada)
class PecaUtilizadaAdmin(admin.ModelAdmin):
    list_display = ('manutencao', 'peca', 'quantidade')
    autocomplete_fields = ['manutencao', 'peca']
