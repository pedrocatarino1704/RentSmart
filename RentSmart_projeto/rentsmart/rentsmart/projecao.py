"""Geração do arquivo CSV com a projeção de 12 meses."""
import csv

from .orcamento import Orcamento

CABECALHO = ["mes", "aluguel", "taxa_contratual", "total_mes"]


def gerar_csv(orcamento: Orcamento, caminho: str = "projecao_12_meses.csv") -> str:
    """Grava o CSV (separador ';' e vírgula decimal, para abrir direto no Excel BR)."""
    with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(CABECALHO)
        for linha in orcamento.projecao():
            escritor.writerow([
                linha["mes"],
                _fmt(linha["aluguel"]),
                _fmt(linha["taxa_contratual"]),
                _fmt(linha["total"]),
            ])
    return caminho


def _fmt(valor) -> str:
    return f"{valor:.2f}".replace(".", ",")
