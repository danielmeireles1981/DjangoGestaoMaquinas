from django.db import models

# 1. Setor/Laboratório
class Setor(models.Model):
    nome = models.CharField('Nome do Setor', max_length=50)
    localizacao = models.CharField('Localização', max_length=100, blank=True)
    responsavel = models.CharField('Responsável', max_length=50, blank=True)

    def __str__(self):
        return self.nome

# 2. Fabricante
class Fabricante(models.Model):
    nome = models.CharField('Nome', max_length=50)
    contato = models.CharField('Contato', max_length=100, blank=True)
    site = models.URLField('Site', blank=True)

    def __str__(self):
        return self.nome

# 3. Fornecedor
class Fornecedor(models.Model):
    nome = models.CharField('Nome', max_length=100)
    contato = models.CharField('Contato', max_length=100, blank=True)
    cnpj = models.CharField('CNPJ', max_length=18, blank=True)
    email = models.EmailField('E-mail', blank=True)

    def __str__(self):
        return self.nome

# 4. Máquina
class Maquina(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('manutencao', 'Parada para Manutenção'),
        ('fora', 'Fora de Uso'),
    ]
    nome = models.CharField('Nome da Máquina', max_length=100)
    numero_patrimonio = models.CharField('Nº Patrimônio', max_length=30, unique=True)
    setor = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name='maquinas')
    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, null=True, blank=True, related_name='maquinas')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='maquinas')
    data_aquisicao = models.DateField('Data de Aquisição')
    status = models.CharField('Status', max_length=15, choices=STATUS_CHOICES, default='ativa')
    observacoes = models.TextField('Observações', blank=True)
    imagem = models.ImageField('Foto da Máquina', upload_to='maquinas/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.numero_patrimonio})"

# 5. Tipo de Manutenção
class TipoManutencao(models.Model):
    nome = models.CharField('Tipo de Manutenção', max_length=30)

    def __str__(self):
        return self.nome

# 6. Peça
class Peca(models.Model):
    nome = models.CharField('Nome da Peça', max_length=100)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, null=True, blank=True)
    codigo = models.CharField('Código', max_length=30, blank=True)
    descricao = models.TextField('Descrição', blank=True)

    def __str__(self):
        return self.nome

# 7. Manutenção
class Manutencao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('concluida', 'Concluída'),
    ]
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='manutencoes')
    data = models.DateField('Data')
    descricao = models.TextField('Descrição do Serviço')
    tipo = models.ForeignKey(TipoManutencao, on_delete=models.SET_NULL, null=True)
    responsavel = models.CharField('Responsável', max_length=50)
    custo = models.DecimalField('Custo', max_digits=10, decimal_places=2)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.tipo} - {self.maquina.nome} ({self.data})"

# 8. Peça Utilizada em Manutenção
class PecaUtilizada(models.Model):
    manutencao = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='pecas_utilizadas')
    peca = models.ForeignKey(Peca, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField('Quantidade', default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.peca.nome} em {self.manutencao}"
