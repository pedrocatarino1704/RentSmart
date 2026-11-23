"""Interface de linha de comando: pergunta, valida e monta os objetos."""
from .imoveis import Apartamento, Casa, Estudio, Imovel
from .orcamento import Orcamento, TaxaContratual


def pedir_opcao(pergunta: str, validas: dict):
    """Repete a pergunta até o usuário digitar uma opção válida."""
    while True:
        resposta = input(pergunta).strip().lower()
        if resposta in validas:
            return validas[resposta]
        print(f"  Opção inválida. Escolha entre: {', '.join(validas)}.")


def pedir_inteiro(pergunta: str, minimo: int, maximo: int = None) -> int:
    while True:
        texto = input(pergunta).strip()
        try:
            numero = int(texto)
        except ValueError:
            print("  Digite um número inteiro.")
            continue
        if numero < minimo or (maximo is not None and numero > maximo):
            faixa = f"entre {minimo} e {maximo}" if maximo is not None else f"maior ou igual a {minimo}"
            print(f"  O valor deve ser {faixa}.")
            continue
        return numero


def pedir_sim_nao(pergunta: str) -> bool:
    return pedir_opcao(pergunta + " (s/n): ", {"s": True, "sim": True, "n": False, "não": False, "nao": False})


def montar_imovel() -> Imovel:
    tipo = pedir_opcao("Tipo de imóvel - [1] Apartamento  [2] Casa  [3] Estúdio: ",
                       {"1": "apartamento", "2": "casa", "3": "estudio"})
    if tipo == "estudio":
        vagas = pedir_inteiro("Quantas vagas de estacionamento (0 = nenhuma): ", 0)
        return Estudio(vagas=vagas)
    quartos = pedir_inteiro("Número de quartos (1 ou 2): ", 1, 2)
    garagem = pedir_sim_nao("Deseja vaga de garagem?")
    classe = Apartamento if tipo == "apartamento" else Casa
    return classe(quartos=quartos, tem_garagem=garagem)


def montar_orcamento() -> Orcamento:
    imovel = montar_imovel()
    possui_criancas = True
    if isinstance(imovel, Apartamento):
        possui_criancas = pedir_sim_nao("Possui crianças?")
    parcelas = pedir_inteiro(f"Parcelas da taxa contratual (1 a {TaxaContratual.MAX_PARCELAS}): ",
                             1, TaxaContratual.MAX_PARCELAS)
    return Orcamento(imovel, possui_criancas, TaxaContratual(parcelas))
