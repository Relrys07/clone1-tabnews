"""
Núcleo de lógica matemática e geração de palpites.
"""

import random
from dataclasses import dataclass
from typing import List, Optional
from config import PRIMOS, FIBONACCI, LOTTERY_CONFIG


@dataclass
class GameResult:
    """Resultado de um jogo gerado com análise estatística."""

    numeros: List[int]
    soma: int
    pares: int
    impares: int
    tipo: str
    primos: Optional[int] = None
    fibo: Optional[int] = None

    def to_dict(self) -> dict:
        """Converter para dicionário (compatível com pandas.DataFrame)."""
        return {
            "numeros": self.numeros,
            "soma": self.soma,
            "pares": self.pares,
            "impares": self.impares,
            "tipo": self.tipo,
            "primos": self.primos,
            "fibo": self.fibo,
        }


class AnalisadorEstatistico:
    """Análise estatística de sequências de números."""

    @staticmethod
    def contar_pares_impares(numeros: List[int]) -> tuple[int, int]:
        """
        Contar pares e impares em uma sequência.

        Args:
            numeros: Lista de números.

        Returns:
            Tupla (quantidade de pares, quantidade de impares).
        """
        pares = sum(1 for n in numeros if n % 2 == 0)
        return pares, len(numeros) - pares

    @staticmethod
    def contar_primos(numeros: List[int]) -> int:
        """
        Contar números primos em uma sequência.

        Args:
            numeros: Lista de números.

        Returns:
            Quantidade de números primos.
        """
        return sum(1 for n in numeros if n in PRIMOS)

    @staticmethod
    def contar_fibonacci(numeros: List[int]) -> int:
        """
        Contar números de Fibonacci em uma sequência.

        Args:
            numeros: Lista de números.

        Returns:
            Quantidade de números de Fibonacci.
        """
        return sum(1 for n in numeros if n in FIBONACCI)

    @staticmethod
    def obter_soma(numeros: List[int]) -> int:
        """
        Retornar a soma de uma sequência.

        Args:
            numeros: Lista de números.

        Returns:
            Soma dos números.
        """
        return sum(numeros)

    @staticmethod
    def tem_sequencia_consecutiva(seq: List[int], tamanho: int = 3) -> bool:
        """
        Verificar se há uma sequência de números consecutivos.

        Args:
            seq: Lista de números (deve estar ordenada).
            tamanho: Comprimento mínimo da sequência consecutiva.

        Returns:
            True se houver sequência consecutiva, False caso contrário.
        """
        for i in range(len(seq) - (tamanho - 1)):
            window = seq[i : i + tamanho]
            if all(window[j] + 1 == window[j + 1] for j in range(len(window) - 1)):
                return True
        return False


class GeradorLoteria:
    """Gerador de palpites otimizados para loterias."""

    def __init__(self):
        """Inicializar com o analisador estatístico."""
        self.analisador = AnalisadorEstatistico()

    def _gerar_randomico(self, total: int, qtd: int) -> List[int]:
        """
        Gerar uma combinação aleatória de números únicos, ordenados.

        Args:
            total: Número máximo do intervalo (1 a total).
            qtd: Quantidade de números a selecionar.

        Returns:
            Lista de números únicos, ordenada.
        """
        return sorted(random.sample(range(1, total + 1), qtd))

    def _validar_jogo_mega_sena(self, jogo: List[int]) -> bool:
        """Validar critérios específicos da Mega-Sena."""
        config = LOTTERY_CONFIG["Mega-Sena"]
        soma = self.analisador.obter_soma(jogo)
        pares, _ = self.analisador.contar_pares_impares(jogo)

        soma_ok = config["range_soma"][0] <= soma <= config["range_soma"][1]
        pares_ok = config["range_pares"][0] <= pares <= config["range_pares"][1]

        return soma_ok and pares_ok

    def _validar_jogo_lotofacil(self, jogo: List[int]) -> bool:
        """Validar critérios específicos da Lotofácil."""
        config = LOTTERY_CONFIG["Lotofácil"]
        soma = self.analisador.obter_soma(jogo)
        primos = self.analisador.contar_primos(jogo)
        fibo = self.analisador.contar_fibonacci(jogo)
        pares, _ = self.analisador.contar_pares_impares(jogo)

        soma_ok = config["range_soma"][0] <= soma <= config["range_soma"][1]
        primos_ok = config["range_primos"][0] <= primos <= config["range_primos"][1]
        fibo_ok = config["range_fibo"][0] <= fibo <= config["range_fibo"][1]
        pares_ok = config["range_pares"][0] <= pares <= config["range_pares"][1]

        return soma_ok and primos_ok and fibo_ok and pares_ok

    def _validar_jogo_quina(self, jogo: List[int]) -> bool:
        """Validar critérios específicos da Quina."""
        config = LOTTERY_CONFIG["Quina"]
        soma = self.analisador.obter_soma(jogo)
        pares, _ = self.analisador.contar_pares_impares(jogo)
        tem_seq = self.analisador.tem_sequencia_consecutiva(jogo, 3)

        soma_ok = config["range_soma"][0] <= soma <= config["range_soma"][1]
        pares_ok = config["range_pares"][0] <= pares <= config["range_pares"][1]
        seq_ok = not (config.get("evitar_sequencia", False) and tem_seq)

        return soma_ok and pares_ok and seq_ok

    def gerar_jogos(self, tipo: str, quantidade: int) -> List[GameResult]:
        """
        Gerar palpites otimizados para uma loteria.

        Args:
            tipo: Tipo de loteria ("Mega-Sena", "Lotofácil", "Quina").
            quantidade: Quantidade de palpites a gerar.

        Returns:
            Lista de GameResult com os palpites gerados.

        Raises:
            ValueError: Se tipo de loteria não for reconhecido.
        """
        if tipo not in LOTTERY_CONFIG:
            raise ValueError(f"Tipo de loteria desconhecido: {tipo}")

        config = LOTTERY_CONFIG[tipo]
        jogos: List[GameResult] = []
        validadores = {
            "Mega-Sena": self._validar_jogo_mega_sena,
            "Lotofácil": self._validar_jogo_lotofacil,
            "Quina": self._validar_jogo_quina,
        }
        validador = validadores[tipo]

        for _ in range(quantidade):
            tentativas = 0
            max_tentativas = config["max_tentativas"]

            while tentativas < max_tentativas:
                tentativas += 1
                jogo = self._gerar_randomico(
                    config["max_numero"], config["qtd_selecionados"]
                )

                if validador(jogo):
                    soma = self.analisador.obter_soma(jogo)
                    pares, impares = self.analisador.contar_pares_impares(jogo)

                    result = GameResult(
                        numeros=jogo,
                        soma=soma,
                        pares=pares,
                        impares=impares,
                        tipo=tipo.lower().replace("-", "_"),
                    )

                    # Adicionar atributos opcionais
                    if tipo == "Lotofácil":
                        result.primos = self.analisador.contar_primos(jogo)
                        result.fibo = self.analisador.contar_fibonacci(jogo)

                    jogos.append(result)
                    break

        return jogos
