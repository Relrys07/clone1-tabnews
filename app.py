"""
LotoPro AI: Gerador de palpites otimizados para loterias.

Interface Streamlit com análise estatística baseada em Fibonacci, números primos e paridades.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from core import GeradorLoteria
from config import LOTTERY_CONFIG
from pdf_generator import PDFGenerator


@st.cache_data
def get_gerador() -> GeradorLoteria:
    """
    Retornar instância cacheada de GeradorLoteria.
    Evita reinicialização a cada rerun do Streamlit.
    """
    return GeradorLoteria()


def apply_custom_style() -> None:
    """Aplicar estilos CSS personalizados ao app."""
    st.markdown(
        """
        <style>
        /* Fundo e Fontes */
        .stApp {
            background: linear-gradient(135deg, #0E1117 0%, #1a1f2e 100%);
            color: #FAFAFA;
        }
        
        /* Botão Personalizado */
        div.stButton > button {
            background: linear-gradient(90deg, #00C853 0%, #64DD17 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            transition: all 0.3s ease;
            box-shadow: 0px 4px 15px rgba(0, 200, 83, 0.4);
            width: 100%;
            cursor: pointer;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0px 8px 25px rgba(0, 200, 83, 0.8);
            background: linear-gradient(90deg, #00B84D 0%, #5FC614 100%);
        }

        /* Cartões de Jogos */
        .game-card {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            padding: 20px;
            border-radius: 15px;
            border-left: 6px solid #00C853;
            margin-bottom: 15px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
            border: 1px solid rgba(0, 200, 83, 0.2);
        }
        
        .game-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 200, 83, 0.3);
            border-left-color: #64DD17;
        }

        /* Bolinhas de Loteria */
        .ball {
            display: inline-block;
            width: 40px;
            height: 40px;
            line-height: 40px;
            border-radius: 50%;
            text-align: center;
            font-weight: bold;
            font-size: 13px;
            color: white;
            margin-right: 6px;
            margin-bottom: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: all 0.2s ease;
        }
        
        .ball:hover {
            transform: scale(1.1) rotate(5deg);
        }
        
        .mega { background: linear-gradient(135deg, #209869 0%, #1a7d54 100%); }
        .loto { background: linear-gradient(135deg, #930089 0%, #6b0066 100%); }
        .quina { background: linear-gradient(135deg, #26338C 0%, #1a2365 100%); }
        
        /* Texto de Análise */
        .analysis-text {
            color: #A6A6A6;
            font-size: 0.9em;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
        }
        
        /* Métrica personalizada */
        .metric-card {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(0, 200, 83, 0.2);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            border-color: rgba(0, 200, 83, 0.8);
            box-shadow: 0 4px 12px rgba(0, 200, 83, 0.2);
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# INTERFACE DO DASHBOARD
# ==============================================================================
st.set_page_config(page_title="LotoPro AI", page_icon="💰", layout="wide")
apply_custom_style()

# --- HEADER ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=80)
with col_title:
    st.title("LotoPro AI: Inteligência Estatística")
    st.markdown("Gerador de palpites com análise estatística otimizada.")

st.divider()

# --- SIDEBAR (CONTROLES COM st.form) ---
gerador = get_gerador()

with st.sidebar:
    st.header("⚙️ Configurações")

    with st.form("lottery_config"):
        tipo_jogo = st.selectbox(
            "Selecione a Loteria:",
            list(LOTTERY_CONFIG.keys()),
            help="Escolha o tipo de loteria para gerar palpites.",
        )

        qtd_jogos = st.slider(
            "Quantidade de Jogos:",
            min_value=1,
            max_value=50,
            value=5,
            help="Número de palpites a gerar (máx: 50).",
        )

        st.markdown("---")
        st.info(
            "✨ Análise otimizada com Fibonacci, números primos e balanceamento de paridades."
        )

        submit_button = st.form_submit_button(
            "🚀 GERAR PALPITES", use_container_width=True
        )

# --- ÁREA PRINCIPAL ---
if submit_button:
    with st.spinner(f"Processando análise para {tipo_jogo}..."):
        try:
            resultados = gerador.gerar_jogos(tipo_jogo, qtd_jogos)
        except Exception as e:
            st.error(f"❌ Erro ao gerar palpites: {str(e)}")
            resultados = []

    if resultados:
        # 1. MÉTRICAS (KPIs)
        st.subheader("📊 Resumo do Lote")

        # Converter GameResult para dicts
        resultados_dicts = [r.to_dict() for r in resultados]
        df = pd.DataFrame(resultados_dicts)

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        with kpi1:
            st.metric(label="Jogos Gerados", value=len(resultados))
        with kpi2:
            media_soma = int(df["soma"].mean())
            st.metric(label="Média da Soma", value=media_soma)
        with kpi3:
            if "primos" in df.columns and df["primos"].notna().any():
                media_primos = round(df["primos"].mean(), 1)
                st.metric(label="Média de Primos", value=media_primos)
            else:
                media_pares = round(df["pares"].mean(), 1)
                st.metric(label="Média de Pares", value=media_pares)
        with kpi4:
            st.success("✅ Análise Concluída")

        st.write("---")

        # 2. EXIBIÇÃO DOS CARTÕES (VISUAL)
        st.subheader("🍀 Seus Palpites")

        css_class = (
            "mega"
            if tipo_jogo == "Mega-Sena"
            else "loto" if tipo_jogo == "Lotofácil" else "quina"
        )
        row1 = st.columns(2)

        for i, resultado in enumerate(resultados):
            col = row1[i % 2]

            with col:
                html_balls = "".join(
                    f"<span class='ball {css_class}'>{num:02d}</span>"
                    for num in resultado.numeros
                )

                analise_str = f"Soma: {resultado.soma}"
                if resultado.primos:
                    analise_str += f" | Primos: {resultado.primos}"
                if resultado.fibo:
                    analise_str += f" | Fibonacci: {resultado.fibo}"

                st.markdown(
                    f"""
                    <div class="game-card">
                        <div style="margin-bottom: 10px; font-weight:bold; color:#00C853;">JOGO #{i+1}</div>
                        <div>{html_balls}</div>
                        <div class="analysis-text">🔍 {analise_str}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

        st.write("---")

        # 3. GRÁFICOS E ANÁLISE
        st.subheader("📈 Análise Estatística")

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            # Gráfico de distribuição de somas
            fig_soma = px.histogram(
                df,
                x="soma",
                nbins=15,
                title="Distribuição de Somas",
                labels={"soma": "Soma", "count": "Frequência"},
            )
            fig_soma.update_traces(marker_color="#00C853")
            fig_soma.update_layout(
                plot_bgcolor="#1f2937",
                paper_bgcolor="#0E1117",
                font=dict(color="#FAFAFA"),
                hovermode="x unified",
            )
            st.plotly_chart(fig_soma, use_container_width=True)

        with col_chart2:
            # Gráfico de paridades
            pares_impares_count = {
                "Pares": df["pares"].mean(),
                "Impares": df["impares"].mean(),
            }
            fig_parity = px.bar(
                x=list(pares_impares_count.keys()),
                y=list(pares_impares_count.values()),
                title="Média de Pares vs Impares",
                labels={"x": "Tipo", "y": "Média"},
            )
            fig_parity.update_traces(marker_color=["#00C853", "#FF6B6B"])
            fig_parity.update_layout(
                plot_bgcolor="#1f2937",
                paper_bgcolor="#0E1117",
                font=dict(color="#FAFAFA"),
                showlegend=False,
            )
            st.plotly_chart(fig_parity, use_container_width=True)

        st.write("---")

        # 4. EXPORTAÇÃO (DOWNLOAD - CSV + PDF)
        st.subheader("💾 Exportar Resultados")

        col_csv, col_pdf = st.columns(2)

        with col_csv:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Baixar em CSV",
                data=csv,
                file_name=f'lotopro_{tipo_jogo.lower().replace("-", "_")}.csv',
                mime="text/csv",
                use_container_width=True,
            )

        with col_pdf:
            pdf_generator = PDFGenerator(tipo_jogo)
            pdf_bytes = pdf_generator.generate_report(resultados)
            st.download_button(
                label="📄 Baixar em PDF",
                data=pdf_bytes,
                file_name=f'lotopro_{tipo_jogo.lower().replace("-", "_")}.pdf',
                mime="application/pdf",
                use_container_width=True,
            )

else:
    # TELA INICIAL
    st.markdown(
        """
        <div style="text-align: center; padding: 50px; opacity: 0.7;">
            <h3>👈 Configure seu jogo no menu lateral</h3>
            <p>Selecione a loteria e a quantidade de palpites para começar a análise.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
