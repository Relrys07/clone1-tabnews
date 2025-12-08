"""
Smoke test rápido para validar funcionalidades principais:
- Gerar jogos para cada loteria
- Salvar CSV
- Gerar PDF via `PDFGenerator`
- Calcular scores via `AnalisadorEstatistico`
- Gerar gráfico Plotly e salvar como HTML

Execute com: .\.venv\Scripts\python.exe smoke_test.py
"""

import os
import traceback
import tempfile
from core import GeradorLoteria, AnalisadorEstatistico
from pdf_generator import PDFGenerator
from config import LOTTERY_CONFIG
import pandas as pd
import plotly.express as px


def run_smoke():
    gerador = GeradorLoteria()
    results_summary = []

    for tipo in LOTTERY_CONFIG.keys():
        print(f"\n== Testando: {tipo} ==")
        try:
            jogos = gerador.gerar_jogos(tipo, 3)
            print(f"Gerados {len(jogos)} jogos para {tipo}")

            # DataFrame
            df = pd.DataFrame([j.to_dict() for j in jogos])
            tmp_csv = os.path.join(tempfile.gettempdir(), f"smoke_{tipo.replace(' ', '_')}.csv")
            df.to_csv(tmp_csv, index=False)
            print(f"CSV salvo: {tmp_csv} (linhas: {len(df)})")

            # Scores
            scores = [AnalisadorEstatistico.calcular_score_probabilidade(j) for j in jogos]
            print("Scores:", scores)

            # PDF
            pdf_gen = PDFGenerator(tipo)
            pdf_bytes = pdf_gen.generate_report(jogos)
            tmp_pdf = os.path.join(tempfile.gettempdir(), f"smoke_{tipo.replace(' ', '_')}.pdf")
            with open(tmp_pdf, "wb") as f:
                f.write(pdf_bytes)
            print(f"PDF salvo: {tmp_pdf} (tamanho: {len(pdf_bytes)} bytes)")

            # Plotly chart
            fig = px.histogram(df, x="soma", nbins=6, title=f"Distribuição de Somas - {tipo}")
            tmp_html = os.path.join(tempfile.gettempdir(), f"smoke_{tipo.replace(' ', '_')}_chart.html")
            fig.write_html(tmp_html, include_plotlyjs='cdn')
            print(f"Gráfico salvo: {tmp_html}")

            results_summary.append((tipo, len(jogos), len(pdf_bytes)))

        except Exception as e:
            print(f"Erro testando {tipo}: {e}")
            traceback.print_exc()

    print("\n=== Resumo ===")
    for tipo, count, pdf_size in results_summary:
        print(f"{tipo}: jogos={count}, pdf_size={pdf_size} bytes")


if __name__ == '__main__':
    run_smoke()
