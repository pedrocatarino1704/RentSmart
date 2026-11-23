import unittest
from decimal import Decimal as D

from rentsmart.imoveis import Apartamento, Casa, Estudio
from rentsmart.orcamento import Orcamento, TaxaContratual


def orc(imovel, criancas=True, parcelas=1):
    return Orcamento(imovel, criancas, TaxaContratual(parcelas))


class TestRegras(unittest.TestCase):
    def test_bases(self):
        self.assertEqual(orc(Apartamento(1)).aluguel_mensal(), D("700"))
        self.assertEqual(orc(Casa(1)).aluguel_mensal(), D("900"))
        self.assertEqual(orc(Estudio()).aluguel_mensal(), D("1200"))

    def test_dois_quartos(self):
        self.assertEqual(orc(Apartamento(2)).aluguel_mensal(), D("900"))
        self.assertEqual(orc(Casa(2)).aluguel_mensal(), D("1150"))

    def test_garagem(self):
        self.assertEqual(orc(Casa(1, True)).aluguel_mensal(), D("1200"))
        self.assertEqual(orc(Apartamento(2, True)).aluguel_mensal(), D("1200"))

    def test_estudio_vagas(self):
        self.assertEqual(orc(Estudio(2)).aluguel_mensal(), D("1450"))
        self.assertEqual(orc(Estudio(4)).aluguel_mensal(), D("1570"))

    def test_desconto_apartamento_sem_criancas(self):
        # (700 + 200 + 300) = 1200 -> 5% = 60 -> 1140
        o = orc(Apartamento(2, True), criancas=False)
        self.assertEqual(o.desconto(), D("60.00"))
        self.assertEqual(o.aluguel_mensal(), D("1140.00"))

    def test_sem_desconto_casa_e_estudio(self):
        self.assertEqual(orc(Casa(1), criancas=False).desconto(), D("0"))
        self.assertEqual(orc(Estudio(2), criancas=False).desconto(), D("0"))

    def test_taxa_parcelas_somam_2000(self):
        for n in range(1, 6):
            t = TaxaContratual(n)
            self.assertEqual(sum(t.valor_do_mes(m) for m in range(1, 13)), D("2000"))

    def test_taxa_invalida(self):
        with self.assertRaises(ValueError):
            TaxaContratual(6)

    def test_projecao_12_meses(self):
        p = orc(Casa(1), parcelas=5).projecao()
        self.assertEqual(len(p), 12)
        self.assertEqual(p[0]["total"], D("900") + D("400"))
        self.assertEqual(p[5]["total"], D("900"))

    def test_quartos_invalidos(self):
        with self.assertRaises(ValueError):
            Casa(3)


if __name__ == "__main__":
    unittest.main()
