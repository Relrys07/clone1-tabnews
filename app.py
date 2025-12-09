"""
LotoPro AI: Gerador de palpites otimizados para loterias.

Interface Streamlit com análise estatística baseada em Fibonacci, números primos e paridades.
"""

import streamlit as st
import streamlit.components.v1 as components
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
    """Aplicar estilos CSS profissionais e modernos ao app."""
    st.markdown(
        """
        <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        /* Fundo principal - gradiente premium */
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0f1729 100%);
            color: #E0E7FF;
        }
        
        /* Remove padding padrão */
        .main {
            padding: 0;
        }
        
        /* Sidebar customizado */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f1729 0%, #1a1f3a 100%);
            border-right: 1px solid rgba(99, 102, 241, 0.2);
        }
        
        [data-testid="stSidebarNav"] {
            background: transparent;
        }
        
        /* Botão Principal - Premium */
        div.stButton > button {
            background: linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #4338CA 100%);
            color: white;
            border: none;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 0.5px;
            border-radius: 10px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
            width: 100%;
            cursor: pointer;
            text-transform: uppercase;
        }
        
        div.stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 16px 40px rgba(99, 102, 241, 0.6);
            background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 50%, #5B21B6 100%);
        }
        
        div.stButton > button:active {
            transform: translateY(-1px);
        }

        /* Cards de Jogos - Design Premium */
        .game-card {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(79, 70, 229, 0.04) 100%);
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 16px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .game-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.2), transparent);
            transition: left 0.6s ease;
        }
        
        .game-card:hover::before {
            left: 100%;
        }
        
        .game-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 50px rgba(99, 102, 241, 0.4);
            border-color: rgba(99, 102, 241, 0.6);
        }
        
        /* Removed the golden animated "best" card effect because it caused
           inconsistent rendering in Streamlit for some users. We keep visuals
           subtle and stable below when marking a best candidate. */
        
        .game-card-title {
            color: #6366F1;
            font-weight: 700;
            font-size: 14px;
            letter-spacing: 1px;
            margin-bottom: 12px;
            text-transform: uppercase;
        }

        /* Bolinhas de Loteria - Estilo Premium */
        .ball {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            font-weight: 800;
            font-size: 14px;
            color: white;
            margin-right: 8px;
            margin-bottom: 8px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .ball::after {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 50%;
            background: inherit;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .ball:hover {
            transform: scale(1.15) rotateY(360deg);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
        }
        
        .mega { background: linear-gradient(135deg, #10B981 0%, #059669 100%); }
        .loto { background: linear-gradient(135deg, #A855F7 0%, #9333EA 100%); }
        .quina { background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); }

        /* Texto de Análise */
        .analysis-text {
            color: #94A3B8;
            font-size: 13px;
            margin-top: 12px;
            font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
            line-height: 1.6;
        }

        /* Container de Métricas Premium */
        .metric-container {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(79, 70, 229, 0.05) 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 20px;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .metric-container:hover {
            border-color: rgba(99, 102, 241, 0.5);
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
        }

        /* Títulos e Headers */
        h1 {
            background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            letter-spacing: -1px;
        }

        h2 {
            color: #E0E7FF;
            font-weight: 700;
            letter-spacing: -0.5px;
            border-bottom: 2px solid rgba(99, 102, 241, 0.3);
            padding-bottom: 12px;
            margin-bottom: 20px;
        }

        h3 {
            color: #C7D2FE;
            font-weight: 600;
        }

        /* Divider */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
            margin: 24px 0;
        }

        /* Info Box */
        [data-testid="stInfo"] {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%);
            border-left: 4px solid #6366F1;
            border-radius: 8px;
            padding: 16px;
        }

        /* Success Box */
        [data-testid="stSuccess"] {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
            border-left: 4px solid #10B981;
        }

        /* Error Box */
        [data-testid="stError"] {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.05) 100%);
            border-left: 4px solid #EF4444;
        }

        /* Scrollbar customizado */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(99, 102, 241, 0.05);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #6366F1 0%, #A855F7 100%);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #7C3AED 0%, #C084FC 100%);
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

# --- HEADER PREMIUM ---
st.markdown(
    """
    <div style="text-align: center; padding: 40px 20px 30px;">
        <h1 style="font-size: 48px; margin-bottom: 8px;">🎰 LotoPro AI</h1>
        <p style="font-size: 18px; color: #A78BFA; letter-spacing: 1px; margin-bottom: 4px;">
            Inteligência Estatística Aplicada a Loterias
        </p>
        <p style="font-size: 13px; color: #94A3B8; margin-top: 8px;">
            Gerador de palpites otimizados com análise profunda de padrões
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

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

        submit_button = st.form_submit_button("🚀 GERAR PALPITES")

# --- ÁREA PRINCIPAL ---
if submit_button:
    with st.spinner(f"Processando análise para {tipo_jogo}..."):
        try:
            resultados = gerador.gerar_jogos(tipo_jogo, qtd_jogos)
        except Exception as e:
            st.error(f"❌ Erro ao gerar palpites: {str(e)}")
            resultados = []

    if resultados:
        # 1. MÉTRICAS (KPIs) - Redesenhado
        st.markdown(
            """
            <div style="margin: 30px 0; padding: 24px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.04) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px;">
                <h2 style="margin: 0 0 16px 0; border: none; padding: 0;">📊 Resumo da Análise</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Converter GameResult para dicts
        resultados_dicts = [r.to_dict() for r in resultados]
        df = pd.DataFrame(resultados_dicts)

        kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="medium")

        with kpi1:
            st.markdown(
                f"""
                <div class="metric-container">
                    <div style="font-size: 32px; font-weight: 800; color: #6366F1; margin-bottom: 8px;">{len(resultados)}</div>
                    <div style="color: #94A3B8; font-size: 13px; letter-spacing: 0.5px; text-transform: uppercase;">Jogos Gerados</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with kpi2:
            media_soma = int(df["soma"].mean())
            st.markdown(
                f"""
                <div class="metric-container">
                    <div style="font-size: 32px; font-weight: 800; color: #A855F7; margin-bottom: 8px;">{media_soma}</div>
                    <div style="color: #94A3B8; font-size: 13px; letter-spacing: 0.5px; text-transform: uppercase;">Média da Soma</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with kpi3:
            if "primos" in df.columns and df["primos"].notna().any():
                media_primos = round(df["primos"].mean(), 1)
                st.markdown(
                    f"""
                    <div class="metric-container">
                        <div style="font-size: 32px; font-weight: 800; color: #10B981; margin-bottom: 8px;">{media_primos}</div>
                        <div style="color: #94A3B8; font-size: 13px; letter-spacing: 0.5px; text-transform: uppercase;">Primos/Jogo</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                media_pares = round(df["pares"].mean(), 1)
                st.markdown(
                    f"""
                    <div class="metric-container">
                        <div style="font-size: 32px; font-weight: 800; color: #10B981; margin-bottom: 8px;">{media_pares}</div>
                        <div style="color: #94A3B8; font-size: 13px; letter-spacing: 0.5px; text-transform: uppercase;">Pares/Jogo</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with kpi4:
            st.markdown(
                f"""
                <div class="metric-container" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%); border-color: rgba(16, 185, 129, 0.3);">
                    <div style="font-size: 32px; font-weight: 800; color: #10B981; margin-bottom: 8px;">✓</div>
                    <div style="color: #10B981; font-size: 13px; letter-spacing: 0.5px; text-transform: uppercase; font-weight: 600;">Análise Concluída</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # 2. EXIBIÇÃO DOS CARTÕES (VISUAL) - Redesenhado
        st.markdown(
            """
            <div style="margin: 30px 0; padding: 24px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.04) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px;">
                <h2 style="margin: 0 0 16px 0; border: none; padding: 0;">🍀 Seus Palpites Otimizados</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        css_class = (
            "mega"
            if tipo_jogo == "Mega-Sena"
            else "loto" if tipo_jogo == "Lotofácil" else "quina"
        )

        # Calcular scores e encontrar melhor palpite
        from core import AnalisadorEstatistico

        scores = [
            AnalisadorEstatistico.calcular_score_probabilidade(r) for r in resultados
        ]
        melhor_indice = scores.index(max(scores)) if scores else 0

        # Grid responsivo
        cols = st.columns(2, gap="large")

        for i, resultado in enumerate(resultados):
            col = cols[i % 2]
            is_melhor = i == melhor_indice
            score = scores[i] if i < len(scores) else 0

            with col:
                # Definir gradiente de cor baseado na loteria
                if css_class == "mega":
                    ball_gradient = "linear-gradient(135deg, #10B981 0%, #059669 100%)"
                elif css_class == "loto":
                    ball_gradient = "linear-gradient(135deg, #A855F7 0%, #9333EA 100%)"
                else:  # quina
                    ball_gradient = "linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)"

                # Bolinhas com estilos inline 100%
                html_balls = "".join(
                    f"<span style='display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: 50%; font-weight: 800; font-size: 14px; color: white; margin-right: 8px; margin-bottom: 8px; background: {ball_gradient}; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4); border: 2px solid rgba(255, 255, 255, 0.2);'>{num:02d}</span>"
                    for num in resultado.numeros
                )

                analise_str = f"<b>Soma:</b> {resultado.soma}"
                if resultado.primos:
                    analise_str += f" | <b>Primos:</b> {resultado.primos}"
                if resultado.fibo:
                    analise_str += f" | <b>Fibonacci:</b> {resultado.fibo}"

                # Estilos inline para o card
                # Se for o melhor palpite, aplicamos um destaque estático e sutil (sem animação)
                if is_melhor:
                    card_style = (
                        "background: linear-gradient(135deg, rgba(255, 244, 220, 0.06) 0%, rgba(255, 244, 220, 0.03) 100%);"
                        "border: 2px solid rgba(255, 215, 0, 0.7); box-shadow: 0 8px 28px rgba(255, 215, 0, 0.12), 0 10px 30px rgba(0,0,0,0.2);"
                    )
                    score_badge = (
                        f"<div style='position:absolute; top:8px; right:8px; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color:#1a1f3a; padding:6px 10px; border-radius:16px; font-size:12px; font-weight:700;'>TOP {int(score)}%</div>"
                    )
                else:
                    score_badge = ""
                    card_style = (
                        "background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(79, 70, 229, 0.04) 100%);"
                        "border: 1px solid rgba(99, 102, 241, 0.3); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);"
                    )

                html_content = f"""<div style="padding: 24px; border-radius: 16px; margin-bottom: 16px; backdrop-filter: blur(10px); position: relative; overflow: hidden; {card_style}">
                    {score_badge}
                    <div style="color: #6366F1; font-weight: 700; font-size: 14px; letter-spacing: 1px; margin-bottom: 12px; text-transform: uppercase;">🎯 Jogo #{i+1}</div>
                    <div style="margin-bottom: 16px;">
                        {html_balls}
                    </div>
                    <div style="color: #94A3B8; font-size: 13px; margin-top: 12px; font-family: 'SF Mono', 'Monaco', 'Courier New', monospace; line-height: 1.6;">
                        {analise_str}
                    </div>
                </div>"""

                # Use components.html — more reliable full-HTML rendering inside columns
                # Height is a safe guess; Streamlit will show a vertical scrollbar if content overflows.
                components.html(html_content, height=180)

        # 3. GRÁFICOS E ANÁLISE - Premium
        st.markdown(
            """
            <div style="margin: 30px 0; padding: 24px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.04) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px;">
                <h2 style="margin: 0 0 16px 0; border: none; padding: 0;">📈 Análise Estatística Detalhada</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_chart1, col_chart2 = st.columns(2, gap="large")

        with col_chart1:
            # Gráfico de distribuição de somas
            fig_soma = px.histogram(
                df,
                x="soma",
                nbins=15,
                title="📊 Distribuição de Somas",
                labels={"soma": "Soma", "count": "Frequência"},
            )
            fig_soma.update_traces(marker_color="#6366F1")
            fig_soma.update_layout(
                plot_bgcolor="rgba(0,0,0,0.2)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E7FF", size=12),
                hovermode="x unified",
                title_font_size=16,
                xaxis_title="Soma dos Números",
                yaxis_title="Frequência",
                showlegend=False,
                margin=dict(l=50, r=50, t=50, b=50),
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
                title="⚖️ Média de Pares vs Impares",
                labels={"x": "Tipo", "y": "Média"},
            )
            fig_parity.update_traces(
                marker_color=["#6366F1", "#A855F7"],
                marker_line_color="rgba(255,255,255,0.2)",
                marker_line_width=2,
            )
            fig_parity.update_layout(
                plot_bgcolor="rgba(0,0,0,0.2)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E7FF", size=12),
                showlegend=False,
                title_font_size=16,
                xaxis_title="",
                yaxis_title="Média por Jogo",
                margin=dict(l=50, r=50, t=50, b=50),
            )
            st.plotly_chart(fig_parity, use_container_width=True)

        # 4. EXPORTAÇÃO (DOWNLOAD - CSV + PDF) - Premium
        st.markdown(
            """
            <div style="margin: 30px 0; padding: 24px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.04) 100%); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px;">
                <h2 style="margin: 0 0 16px 0; border: none; padding: 0;">💾 Exportar Resultados</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_csv, col_pdf = st.columns(2, gap="large")

        with col_csv:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📊 Baixar em CSV",
                data=csv,
                file_name=f'lotopro_{tipo_jogo.lower().replace("-", "_")}.csv',
                mime="text/csv",
            )

        with col_pdf:
            pdf_generator = PDFGenerator(tipo_jogo)
            pdf_bytes = pdf_generator.generate_report(resultados)
            st.download_button(
                label="📄 Baixar em PDF",
                data=pdf_bytes,
                file_name=f'lotopro_{tipo_jogo.lower().replace("-", "_")}.pdf',
                mime="application/pdf",
            )

else:
    # TELA INICIAL - Redesenhada
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; min-height: 60vh;">
            <div style="text-align: center;">
                <div style="font-size: 72px; margin-bottom: 20px;">🎯</div>
                <h2 style="font-size: 28px; margin-bottom: 12px; border: none;">Pronto para Gerar Palpites?</h2>
                <p style="font-size: 16px; color: #94A3B8; margin-bottom: 20px; max-width: 500px;">
                    Configure seu jogo no menu lateral selecionando a loteria desejada e a quantidade de palpites otimizados.
                </p>
                <div style="display: inline-block; padding: 16px 32px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.1) 100%); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 10px; color: #A78BFA; font-size: 14px;">
                    ⚙️ Menu Lateral → Selecione a Loteria → Clique em Gerar
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Seção de informações
    st.markdown(
        """
        <div style="margin-top: 60px; padding: 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
                <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.2);">
                    <div style="font-size: 24px; margin-bottom: 8px;">🔍</div>
                    <div style="font-weight: 600; color: #E0E7FF; margin-bottom: 8px;">Análise Inteligente</div>
                    <div style="font-size: 13px; color: #94A3B8;">Algoritmos baseados em sequências de Fibonacci e números primos</div>
                </div>
                <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(79, 70, 229, 0.05) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.2);">
                    <div style="font-size: 24px; margin-bottom: 8px;">📊</div>
                    <div style="font-weight: 600; color: #E0E7FF; margin-bottom: 8px;">Estatísticas Completas</div>
                    <div style="font-size: 13px; color: #94A3B8;">Análise de padrões, distribuições e balanceamento</div>
                </div>
                <div style="background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(132, 39, 212, 0.05) 100%); padding: 20px; border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.2);">
                    <div style="font-size: 24px; margin-bottom: 8px;">📥</div>
                    <div style="font-weight: 600; color: #E0E7FF; margin-bottom: 8px;">Múltiplos Formatos</div>
                    <div style="font-size: 13px; color: #94A3B8;">Exporte em CSV ou PDF para usar em qualquer lugar</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
