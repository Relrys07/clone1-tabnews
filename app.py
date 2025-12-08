"""
LotoPro AI: Gerador de palpites otimizados para loterias.

Interface Streamlit com análise estatística baseada em Fibonacci, números primos e paridades.
"""

import streamlit as st
import pandas as pd
from core import GeradorLoteria
from config import LOTTERY_CONFIG


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
            background-color: #0E1117;
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
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0px 4px 15px rgba(0, 200, 83, 0.4);
            width: 100%;
        }
        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0px 6px 20px rgba(0, 200, 83, 0.6);
        }

        /* Cartões de Jogos */
        .game-card {
            background-color: #262730;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #00C853;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        /* Bolinhas de Loteria */
        .ball {
            display: inline-block;
            width: 35px;
            height: 35px;
            line-height: 35px;
            border-radius: 50%;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
            color: white;
            margin-right: 5px;
            box-shadow: inset -2px -2px 5px rgba(0,0,0,0.3);
        }
        .mega { background-color: #209869; }
        .loto { background-color: #930089; }
        .quina { background-color: #26338C; }
        
        /* Texto de Análise */
        .analysis-text {
            color: #A6A6A6;
            font-size: 0.9em;
            margin-top: 10px;
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

        # 3. EXPORTAÇÃO (DOWNLOAD)
        st.write("---")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar Jogos em CSV",
            data=csv,
            file_name=f'lotopro_{tipo_jogo.lower().replace("-", "_")}.csv',
            mime="text/csv",
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
