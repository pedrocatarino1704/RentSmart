"""RentSmart - ponto de entrada. Execute: python main.py"""
from rentsmart.interface import montar_orcamento
from rentsmart.projecao import gerar_csv


def main():
    print("Bem-vindo ao RentSmart - R.M Imóveis\n")
    orcamento = montar_orcamento()
    print(orcamento.resumo())
    caminho = gerar_csv(orcamento)
    print(f"\nArquivo CSV gerado: {caminho}")


if __name__ == "__main__":
    main()
