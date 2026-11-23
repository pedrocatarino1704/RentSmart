"""Classes que representam os imóveis e suas regras de preço."""
from abc import ABC, abstractmethod
from decimal import Decimal

D = Decimal


class Imovel(ABC):
    """Classe base: define o contrato que todo imóvel precisa cumprir."""

    TIPO = "Imóvel"
    ALUGUEL_BASE = D("0")

    def __init__(self, vagas: int = 0):
        if vagas < 0:
            raise ValueError("O número de vagas não pode ser negativo.")
        self.vagas = vagas

    @abstractmethod
    def adicional_quartos(self) -> Decimal:
        """Valor adicional mensal pelo número de quartos."""

    @abstractmethod
    def valor_garagem(self) -> Decimal:
        """Valor mensal da garagem/estacionamento."""

    @abstractmethod
    def descricao(self) -> str:
        """Texto curto que descreve o imóvel escolhido."""

    def aluguel_bruto(self) -> Decimal:
        """Aluguel-base + adicionais (antes de qualquer desconto)."""
        return self.ALUGUEL_BASE + self.adicional_quartos() + self.valor_garagem()

    def desconto(self, possui_criancas: bool) -> Decimal:
        """Por padrão, imóveis não têm desconto. Subclasses podem sobrescrever."""
        return D("0")

    def detalhes(self) -> list:
        """Lista (descrição, valor) usada no resumo do orçamento."""
        itens = [(f"Aluguel-base ({self.TIPO})", self.ALUGUEL_BASE)]
        if self.adicional_quartos() > 0:
            itens.append(("Adicional de 2 quartos", self.adicional_quartos()))
        if self.valor_garagem() > 0:
            itens.append((self._rotulo_garagem(), self.valor_garagem()))
        return itens

    def _rotulo_garagem(self) -> str:
        return f"Garagem ({self.vagas} vaga(s))"


class _ImovelComQuartos(Imovel):
    """Comportamento comum de Casa e Apartamento (1 ou 2 quartos, 1 vaga opcional)."""

    ADICIONAL_2_QUARTOS = D("0")
    VALOR_VAGA = D("300.00")

    def __init__(self, quartos: int, tem_garagem: bool = False):
        if quartos not in (1, 2):
            raise ValueError("O número de quartos deve ser 1 ou 2.")
        super().__init__(vagas=1 if tem_garagem else 0)
        self.quartos = quartos

    def adicional_quartos(self) -> Decimal:
        return self.ADICIONAL_2_QUARTOS if self.quartos == 2 else D("0")

    def valor_garagem(self) -> Decimal:
        return self.VALOR_VAGA if self.vagas else D("0")

    def descricao(self) -> str:
        garagem = "com garagem" if self.vagas else "sem garagem"
        return f"{self.TIPO} de {self.quartos} quarto(s), {garagem}"


class Apartamento(_ImovelComQuartos):
    TIPO = "Apartamento"
    ALUGUEL_BASE = D("700.00")
    ADICIONAL_2_QUARTOS = D("200.00")
    DESCONTO_SEM_CRIANCAS = D("0.05")

    def desconto(self, possui_criancas: bool) -> Decimal:
        """5% sobre o aluguel (já com adicionais) se não há crianças."""
        if possui_criancas:
            return D("0")
        return (self.aluguel_bruto() * self.DESCONTO_SEM_CRIANCAS).quantize(D("0.01"))


class Casa(_ImovelComQuartos):
    TIPO = "Casa"
    ALUGUEL_BASE = D("900.00")
    ADICIONAL_2_QUARTOS = D("250.00")


class Estudio(Imovel):
    TIPO = "Estúdio"
    ALUGUEL_BASE = D("1200.00")
    PACOTE_VAGAS = 2
    VALOR_PACOTE = D("250.00")
    VALOR_VAGA_EXTRA = D("60.00")

    def adicional_quartos(self) -> Decimal:
        return D("0")  # estúdio não tem divisão de quartos

    def valor_garagem(self) -> Decimal:
        """Pacote de 2 vagas por R$ 250 + R$ 60 por vaga adicional."""
        if self.vagas == 0:
            return D("0")
        extras = max(0, self.vagas - self.PACOTE_VAGAS)
        return self.VALOR_PACOTE + extras * self.VALOR_VAGA_EXTRA

    def descricao(self) -> str:
        return f"{self.TIPO}, {self.vagas} vaga(s) de estacionamento"

    def _rotulo_garagem(self) -> str:
        extras = max(0, self.vagas - self.PACOTE_VAGAS)
        if extras:
            return f"Estacionamento (pacote 2 vagas + {extras} extra(s))"
        return "Estacionamento (pacote de 2 vagas)"
