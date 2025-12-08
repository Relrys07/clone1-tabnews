"""
Módulo para exportação de resultados em PDF com layout profissional.
"""

from datetime import datetime
from typing import List

from fpdf import FPDF

from core import GameResult


class PDFGenerator:
    """Gerador de relatórios em PDF para palpites de loterias."""

    def __init__(self, lottery_type: str):
        """
        Inicializar gerador de PDF.

        Args:
            lottery_type: Tipo de loteria (Mega-Sena, Lotofácil, Quina).
        """
        self.lottery_type = lottery_type
        self.pdf = FPDF(orientation="P", unit="mm", format="A4")
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=10)
        self._setup_fonts()

    def _setup_fonts(self) -> None:
        """Configurar fontes padrão."""
        # Usar fonte padrão do FPDF sem add_font
        pass

    def _add_header(self) -> None:
        """Adicionar cabeçalho do documento."""
        self.pdf.set_font("Helvetica", "B", 24)
        self.pdf.set_text_color(0, 200, 83)  # Verde
        self.pdf.cell(0, 15, "LotoPro AI", ln=True, align="C")

        self.pdf.set_font("Helvetica", "", 10)
        self.pdf.set_text_color(100, 100, 100)
        self.pdf.cell(
            0, 5, f"Relatório de Palpites - {self.lottery_type}", ln=True, align="C"
        )
        self.pdf.cell(
            0,
            5,
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}",
            ln=True,
            align="C",
        )
        self.pdf.ln(5)

    def _add_section_title(self, title: str) -> None:
        """Adicionar título de seção."""
        self.pdf.set_font("Helvetica", "B", 14)
        self.pdf.set_text_color(0, 200, 83)
        self.pdf.cell(0, 8, title, ln=True)
        self.pdf.ln(2)

    def _add_game_card(self, game: GameResult, index: int) -> None:
        """
        Adicionar cartão com um jogo ao PDF.

        Args:
            game: Resultado do jogo.
            index: Número do jogo.
        """
        # Cabeçalho do cartão
        self.pdf.set_font("Helvetica", "B", 11)
        self.pdf.set_text_color(0, 200, 83)
        self.pdf.cell(0, 6, f"JOGO #{index}", ln=True)

        # Números
        self.pdf.set_font("Helvetica", "", 10)
        self.pdf.set_text_color(50, 50, 50)
        numeros_str = " - ".join(f"{n:02d}" for n in game.numeros)
        self.pdf.cell(0, 6, f"Números: {numeros_str}", ln=True)

        # Análise
        analise = f"Soma: {game.soma} | Pares: {game.pares} | Impares: {game.impares}"
        if game.primos is not None:
            analise += f" | Primos: {game.primos}"
        if game.fibo is not None:
            analise += f" | Fibonacci: {game.fibo}"
        self.pdf.cell(0, 6, analise, ln=True)
        self.pdf.ln(2)

    def generate_report(self, games: List[GameResult]) -> bytes:
        """
        Gerar relatório em PDF.

        Args:
            games: Lista de GameResult para incluir no relatório.

        Returns:
            Bytes do PDF gerado.
        """
        self._add_header()

        # Resumo
        self._add_section_title("Resumo Estatistico")
        self.pdf.set_font("Helvetica", "", 10)
        self.pdf.set_text_color(50, 50, 50)
        self.pdf.cell(0, 6, f"Total de Palpites: {len(games)}", ln=True)

        if games:
            somas = [g.soma for g in games]
            media_soma = sum(somas) / len(somas)
            self.pdf.cell(0, 6, f"Média de Soma: {media_soma:.1f}", ln=True)

            pares = [g.pares for g in games]
            media_pares = sum(pares) / len(pares)
            self.pdf.cell(0, 6, f"Média de Pares: {media_pares:.1f}", ln=True)

        self.pdf.ln(5)

        # Palpites
        self._add_section_title("Palpites Gerados")
        for i, game in enumerate(games, 1):
            self._add_game_card(game, i)

        # Footer
        self.pdf.ln(10)
        self.pdf.set_font("Helvetica", "", 8)
        self.pdf.set_text_color(150, 150, 150)
        self.pdf.cell(
            0,
            5,
            "Gerado por LotoPro AI - Análise Estatística de Loterias",
            ln=True,
            align="C",
        )

        return bytes(self.pdf.output())
