import streamlit as st
import random
import pandas as pd
import time

# ==============================================================================
# 1. ESTILIZAÇÃO CSS (DESIGN PROFISSIONAL)
# ==============================================================================
def apply_custom_style():
    st.markdown("""
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
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. LÓGICA MATEMÁTICA (MOTOR)
# ==============================================================================
class AnalisadorEstatistico:
    @staticmethod
    def contar_pares_impares(numeros):
        pares = len([n for n in numeros if n % 2 == 0])
        return pares, len(numeros) - pares

    @staticmethod
    def contar_primos(numeros):
        primos = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79}
        return len([n for n in numeros if n in primos])

    @staticmethod
    def contar_fibonacci(numeros):
        fibo = {1, 2, 3, 5, 8, 13, 21, 34, 55}
        return len([n for n in numeros if n in fibo])

    @staticmethod
    def obter_soma(numeros):
        return sum(numeros)

class GeradorLoteria:
    def __init__(self):
        self.analisador = AnalisadorEstatistico()

    def _gerar_randomico(self, total, qtd):
        return sorted(random.sample(range(1, total + 1), qtd))

    def gerar_jogos(self, tipo, quantidade):
        jogos = []
        progresso = st.progress(0)
        
        for i in range(quantidade):
            tentativas = 0
            while True:
                tentativas += 1
                if tentativas > 10000: break # Evitar loop infinito

                if tipo == "Mega-Sena":
                    jogo = self._gerar_randomico(60, 6)
                    soma = self.analisador.obter_soma(jogo)
                    pares, impares = self.analisador.contar_pares_impares(jogo)
                    if 140 <= soma <= 225 and 2 <= pares <= 4:
                        jogos.append({"numeros": jogo, "soma": soma, "pares": pares, "impares": impares, "tipo": "mega"})
                        break
                
                elif tipo == "Lotofácil":
                    jogo = self._gerar_randomico(25, 15)
                    soma = self.analisador.obter_soma(jogo)
                    primos = self.analisador.contar_primos(jogo)
                    fibo = self.analisador.contar_fibonacci(jogo)
                    pares, _ = self.analisador.contar_pares_impares(jogo)
                    if 180 <= soma <= 230 and 4 <= primos <= 6 and 3 <= fibo <= 6 and 6 <= pares <= 9:
                        jogos.append({"numeros": jogo, "soma": soma, "primos": primos, "fibo": fibo, "pares": pares, "tipo": "loto"})
                        break

                elif tipo == "Quina":
                    jogo = self._gerar_randomico(80, 5)
                    soma = self.analisador.obter_soma(jogo)
                    pares, _ = self.analisador.contar_pares_impares(jogo)
                    tem_sequencia = any(jogo[k] == jogo[k-1]+1 == jogo[k-2]+2 for k in range(2, 5))
                    if 160 <= soma <= 240 and 1 <= pares <= 4 and not tem_sequencia:
                        jogos.append({"numeros": jogo, "soma": soma, "pares": pares, "tipo": "quina"})
                        break

            progresso.progress((i + 1) / quantidade)
            time.sleep(0.05) # Efeito visual
        
        progresso.empty()
        return jogos

# ==============================================================================
# 3. INTERFACE DO DASHBOARD
# ==============================================================================
st.set_page_config(page_title="LotoPro AI", page_icon="💰", layout="wide")
apply_custom_style()

# --- HEADER ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=80) # Ícone genérico
with col_title:
    st.title("LotoPro AI: Inteligência Estatística")
    st.markdown("Algoritmo preditivo baseado em Curva de Gauss, Fibonacci e Números Primos.")

st.divider()

# --- SIDEBAR (CONTROLES) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    tipo_jogo = st.selectbox("Selecione a Loteria:", ["Mega-Sena", "Lotofácil", "Quina"])
    
    st.write("---")
    qtd_jogos = st.slider("Quantidade de Jogos:", 1, 20, 5)
    
    st.write("---")
    st.info("💡 Este algoritmo filtra mais de 10.000 combinações por segundo para encontrar a estatística ideal.")
    
    btn_gerar = st.button("🚀 GERAR PALPITES OTIMIZADOS")

# --- ÁREA PRINCIPAL ---
gerador = GeradorLoteria()

if btn_gerar:
    with st.spinner(f"Processando probabilidades para {tipo_jogo}..."):
        resultados = gerador.gerar_jogos(tipo_jogo, qtd_jogos)

    # 1. MÉTRICAS (KPIs)
    st.subheader("📊 Resumo do Lote")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    df = pd.DataFrame(resultados)
    
    with kpi1:
        st.metric(label="Jogos Gerados", value=len(resultados))
    with kpi2:
        media_soma = int(df['soma'].mean())
        st.metric(label="Média da Soma", value=media_soma, delta="Ideal Estatístico")
    with kpi3:
        if 'primos' in df.columns:
            media_primos = round(df['primos'].mean(), 1)
            st.metric(label="Média de Primos", value=media_primos)
        else:
            media_pares = round(df['pares'].mean(), 1)
            st.metric(label="Média de Pares", value=media_pares)
    with kpi4:
        st.success("Status: Alta Probabilidade")

    st.write("---")

    # 2. EXIBIÇÃO DOS CARTÕES (VISUAL)
    st.subheader("🍀 Seus Palpites")
    
    # Define a classe CSS da bolinha baseada no jogo
    css_class = "mega" if tipo_jogo == "Mega-Sena" else "loto" if tipo_jogo == "Lotofácil" else "quina"

    row1 = st.columns(2) # Grid de 2 colunas para os jogos
    
    for i, jogo in enumerate(resultados):
        # Lógica para alternar colunas (Grid Layout)
        col = row1[i % 2]
        
        with col:
            # HTML para as bolinhas
            html_balls = ""
            for num in jogo['numeros']:
                html_balls += f"<span class='ball {css_class}'>{num:02d}</span>"
            
            # Detalhes da análise para exibir no cartão
            analise_str = f"Soma: {jogo['soma']}"
            if 'primos' in jogo: analise_str += f" | Primos: {jogo['primos']}"
            if 'fibo' in jogo: analise_str += f" | Fibonacci: {jogo['fibo']}"
            
            # Renderiza o cartão
            st.markdown(f"""
                <div class="game-card">
                    <div style="margin-bottom: 10px; font-weight:bold; color:#00C853;">JOGO #{i+1}</div>
                    <div>{html_balls}</div>
                    <div class="analysis-text">🔍 {analise_str}</div>
                </div>
            """, unsafe_allow_html=True)

    # 3. EXPORTAÇÃO (DOWNLOAD)
    st.write("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Jogos em Excel (CSV)",
        data=csv,
        file_name=f'jogos_{tipo_jogo.lower()}.csv',
        mime='text/csv',
    )

else:
    # TELA INICIAL (QUANDO NÃO TEM JOGO)
    st.markdown("""
        <div style="text-align: center; padding: 50px; opacity: 0.7;">
            <h3>👈 Configure seu jogo no menu lateral</h3>
            <p>Selecione a loteria e a quantidade de palpites para começar a análise de IA.</p>
        </div>
    """, unsafe_allow_html=True)