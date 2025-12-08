"""
Testes unitários para o módulo core.py
"""

import pytest
from core import AnalisadorEstatistico, GeradorLoteria, GameResult


class TestAnalisadorEstatistico:
    """Testes para AnalisadorEstatistico."""

    def test_contar_pares_impares(self):
        """Testar contagem de pares e impares."""
        pares, impares = AnalisadorEstatistico.contar_pares_impares([1, 2, 3, 4])
        assert pares == 2
        assert impares == 2

    def test_contar_pares_impares_todos_pares(self):
        """Testar contagem com todos pares."""
        pares, impares = AnalisadorEstatistico.contar_pares_impares([2, 4, 6])
        assert pares == 3
        assert impares == 0

    def test_contar_primos(self):
        """Testar contagem de números primos."""
        count = AnalisadorEstatistico.contar_primos([2, 3, 4, 5])
        assert count == 3  # 2, 3, 5 são primos

    def test_contar_fibonacci(self):
        """Testar contagem de números de Fibonacci."""
        count = AnalisadorEstatistico.contar_fibonacci([1, 2, 3, 5, 8, 10])
        assert count == 5  # 1, 2, 3, 5, 8 são Fibonacci

    def test_obter_soma(self):
        """Testar cálculo de soma."""
        soma = AnalisadorEstatistico.obter_soma([1, 2, 3, 4, 5])
        assert soma == 15

    def test_tem_sequencia_consecutiva_true(self):
        """Testar detecção de sequência consecutiva (deve encontrar)."""
        result = AnalisadorEstatistico.tem_sequencia_consecutiva([1, 5, 6, 7, 10])
        assert result is True  # 5, 6, 7 são consecutivos

    def test_tem_sequencia_consecutiva_false(self):
        """Testar detecção de sequência consecutiva (não deve encontrar)."""
        result = AnalisadorEstatistico.tem_sequencia_consecutiva([1, 3, 5, 7, 9])
        assert result is False  # Nenhuma sequência de 3 consecutivos


class TestGeradorLoteria:
    """Testes para GeradorLoteria."""

    def test_gerador_instantiation(self):
        """Testar instanciação do gerador."""
        gerador = GeradorLoteria()
        assert gerador is not None
        assert gerador.analisador is not None

    def test_gerar_randomico(self):
        """Testar geração de números aleatórios únicos."""
        gerador = GeradorLoteria()
        numeros = gerador._gerar_randomico(60, 6)
        assert len(numeros) == 6
        assert len(set(numeros)) == 6  # Todos únicos
        assert all(1 <= n <= 60 for n in numeros)
        assert numeros == sorted(numeros)  # Deve estar ordenado

    def test_gerar_jogos_mega_sena(self):
        """Testar geração de jogos da Mega-Sena."""
        gerador = GeradorLoteria()
        jogos = gerador.gerar_jogos("Mega-Sena", 3)
        assert len(jogos) == 3
        for jogo in jogos:
            assert isinstance(jogo, GameResult)
            assert len(jogo.numeros) == 6
            assert 140 <= jogo.soma <= 225
            assert 2 <= jogo.pares <= 4

    def test_gerar_jogos_lotofacil(self):
        """Testar geração de jogos da Lotofácil."""
        gerador = GeradorLoteria()
        jogos = gerador.gerar_jogos("Lotofácil", 2)
        assert len(jogos) == 2
        for jogo in jogos:
            assert isinstance(jogo, GameResult)
            assert len(jogo.numeros) == 15
            assert 180 <= jogo.soma <= 230

    def test_gerar_jogos_quina(self):
        """Testar geração de jogos da Quina."""
        gerador = GeradorLoteria()
        jogos = gerador.gerar_jogos("Quina", 2)
        assert len(jogos) == 2
        for jogo in jogos:
            assert isinstance(jogo, GameResult)
            assert len(jogo.numeros) == 5
            assert 160 <= jogo.soma <= 240

    def test_gerar_jogos_tipo_invalido(self):
        """Testar erro com tipo de loteria inválido."""
        gerador = GeradorLoteria()
        with pytest.raises(ValueError):
            gerador.gerar_jogos("LoteriaBogus", 1)


class TestGameResult:
    """Testes para GameResult."""

    def test_game_result_creation(self):
        """Testar criação de GameResult."""
        result = GameResult(
            numeros=[1, 2, 3, 4, 5, 6],
            soma=21,
            pares=3,
            impares=3,
            tipo="mega",
        )
        assert result.numeros == [1, 2, 3, 4, 5, 6]
        assert result.soma == 21
        assert result.primos is None

    def test_game_result_to_dict(self):
        """Testar conversão para dicionário."""
        result = GameResult(
            numeros=[1, 2],
            soma=3,
            pares=1,
            impares=1,
            tipo="quina",
            primos=1,
        )
        d = result.to_dict()
        assert d["soma"] == 3
        assert d["primos"] == 1
        assert "numeros" in d
