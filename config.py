"""
Configurações e constantes da aplicação LotoPro.
"""

# Constantes de números primos (até 80)
PRIMOS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79}

# Constantes de sequência de Fibonacci (até 80)
FIBONACCI = {1, 2, 3, 5, 8, 13, 21, 34, 55}

# Configuração por tipo de loteria: (max_numero, qtd_selecionados, ranges de soma, ranges de pares, etc)
LOTTERY_CONFIG = {
    "Mega-Sena": {
        "max_numero": 60,
        "qtd_selecionados": 6,
        "range_soma": (140, 225),
        "range_pares": (2, 4),
        "max_tentativas": 10000,
    },
    "Lotofácil": {
        "max_numero": 25,
        "qtd_selecionados": 15,
        "range_soma": (180, 230),
        "range_pares": (6, 9),
        "range_primos": (4, 6),
        "range_fibo": (3, 6),
        "max_tentativas": 10000,
    },
    "Quina": {
        "max_numero": 80,
        "qtd_selecionados": 5,
        "range_soma": (160, 240),
        "range_pares": (1, 4),
        "max_tentativas": 10000,
        "evitar_sequencia": True,
    },
}
