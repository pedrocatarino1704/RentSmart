"""Orçamento de locação: junta imóvel, taxa contratual e parcelamento."""
from decimal import Decimal, ROUND_HALF_UP

from .imoveis import Imovel

D = Decimal
CENT = D("0.01")


def moeda(valor: Decimal) -> str:
    """Formata como moeda brasileira: R$ 1.234,56."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class TaxaContratual:
    """Taxa de contrato de R$ 2.000,00, parcelável em até 5 vezes."""

    VALOR = D("2000.00")
    MAX_PARCELAS = 5

    def __init__(self, parcelas: int = 1):
        if not 1 <= parcelas <= self.MAX_PARCELAS:
            raise ValueError(f"As parcelas devem estar entre 1 e {self.MAX_PARCELAS}.")
        self.parcelas = parcelas

    def valor_parcela(self) -> Decimal:
        return (self.VALOR / self.parcelas).quantize(CENT, rounding=ROUND_HALF_UP)

    def valor_do_mes(self, mes: int) -> Decimal:
        """Valor da taxa devido no mês (1..12). Última parcela absorve a diferença."""
        if mes < 1 or mes > self.parcelas:
            return D("0")
        if mes == self.parcelas:
            return self.VALOR - self.valor_parcela() * (self.parcelas - 1)
        return self.valor_parcela()


class Orcamento:
    """Calcula e descreve o orçamento completo de uma locação."""

    MESES = 12

    def __init__(self, imovel: Imovel, possui_criancas: bool, taxa: TaxaContratual):
        self.imovel = imovel
        self.possui_criancas = possui_criancas
        self.taxa = taxa

    def desconto(self) -> Decimal:
        return self.imovel.desconto(self.possui_criancas)

    def aluguel_mensal(self) -> Decimal:
        return self.imovel.aluguel_bruto() - self.desconto()

    def total_mes(self, mes: int) -> Decimal:
        return self.aluguel_mensal() + self.taxa.valor_do_mes(mes)

    def projecao(self) -> list:
        """Lista de dicts com a projeção dos 12 meses."""
        linhas = []
        for mes in range(1, self.MESES + 1):
            linhas.append({
                "mes": mes,
                "aluguel": self.aluguel_mensal(),
                "taxa_contratual": self.taxa.valor_do_mes(mes),
                "total": self.total_mes(mes),
            })
        return linhas

    def total_primeiro_ano(self) -> Decimal:
        return sum((l["total"] for l in self.projecao()), D("0"))

    def resumo(self) -> str:
        linhas = ["", "=" * 56, "      RENTSMART - ORÇAMENTO DE LOCAÇÃO (R.M Imóveis)",
                  "=" * 56, f"Imóvel: {self.imovel.descricao()}", "",
                  "ALUGUEL MENSAL"]
        for nome, valor in self.imovel.detalhes():
            linhas.append(f"  {nome:<42}{moeda(valor):>12}")
        linhas.append(f"  {'Subtotal':<42}{moeda(self.imovel.aluguel_bruto()):>12}")
        if self.desconto() > 0:
            linhas.append(f"  {'Desconto 5% (sem crianças)':<42}{'- ' + moeda(self.desconto()):>12}")
        linhas.append(f"  {'ALUGUEL MENSAL FINAL':<42}{moeda(self.aluguel_mensal()):>12}")
        linhas += ["", "TAXA CONTRATUAL (cobrada separadamente do aluguel)",
                   f"  {'Valor total da taxa':<42}{moeda(self.taxa.VALOR):>12}",
                   f"  {'Parcelamento':<42}{str(self.taxa.parcelas) + 'x de ' + moeda(self.taxa.valor_parcela()):>12}",
                   "", f"TOTAL PREVISTO NO 1º ANO (12 meses): {moeda(self.total_primeiro_ano())}",
                   "=" * 56]
        return "\n".join(linhas)
