import streamlit as st
import pandas as pd
import plotly.express as px
import random
from textblob import TextBlob

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Analisador de Sentimentos",
    page_icon="🧠",
    layout="wide"
)

# CSS LIMPO
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 0.5rem 0;
    }
    
    .tweet-card {
        background: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        border-left: 4px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .sentiment-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

class AnalisadorSentimentos:
    def __init__(self):
        self.categorias = [
            "🚀 Tecnologia & Inovação",
            "🎬 Entretenimento & Cultura", 
            "💼 Negócios & Economia",
            "🏆 Esportes & Competições",
            "🌍 Sustentabilidade & Meio Ambiente",
            "🏛️ Política & Sociedade",
            "🎵 Música & Artes",
            "🛒 Consumo & Marcas"
        ]
    
    def buscar_dados(self, topico, quantidade):
        """Dados de exemplo para demonstração"""
        dados_por_topico = {
            "🚀 Tecnologia & Inovação": [
                "Inteligência Artificial está revolucionando tudo! 🤖 Incrível demais!",
                "Novo smartphone com câmera espetacular! 📸 Qualidade impressionante!",
                "Metaverso ainda é uma incógnita... 🤔 Não sei o que pensar",
                "Python continua dominando o mundo da data science! 🐍",
                "Privacidade digital é uma grande preocupação atualmente 😟"
            ],
            "🎬 Entretenimento & Cultura": [
                "Série nova na Netflix é simplesmente perfeita! 🎬",
                "Final decepcionante arruinou toda a temporada 😞",
                "Atuações fenomenais no último filme que assisti! 🌟",
                "Streaming caro demais pelo conteúdo oferecido 💸",
                "Documentário sobre natureza é visualmente deslumbrante! 🌍"
            ],
            "💼 Negócios & Economia": [
                "Mercado de criptomoedas em alta impressionante! 📈",
                "Startup innovando com soluções brilhantes! 💡",
                "Economia global em momento delicado 😰",
                "Empreendedorismo digital crescendo exponencialmente! 🚀",
                "Fusão empresarial beneficiando todos os lados! 🤝"
            ],
            "🏆 Esportes & Competições": [
                "Jogo histórico com performance espetacular! ⚽",
                "Arbitragem controversa decidindo o resultado 😠",
                "Atleta quebrando recordes mundialmente! 🏆",
                "Time favorito decepcionando na temporada 😔",
                "Torcida animada criando atmosfera incrível! 🔥"
            ],
            "🌍 Sustentabilidade & Meio Ambiente": [
                "Energia solar revolucionando matriz energética! ☀️",
                "Projetos de reflorestamento com resultados incríveis! 🌳",
                "Consumo consciente ganhando força na sociedade! 💚",
                "Poluição plástica ainda é desafio enorme 😞",
                "Tecnologias verdes com potencial transformador! 🔋"
            ],
            "🏛️ Política & Sociedade": [
                "Medida governamental beneficiando população! 👍",
                "Corrupção minando desenvolvimento nacional 😠",
                "Diálogo internacional construindo pontes! 🌐",
                "Políticas públicas precisando de ajustes 📋",
                "Liderança inspiradora em momento crucial! 💫"
            ],
            "🎵 Música & Artes": [
                "Álbum novo superando todas as expectativas! 🎵",
                "Show ao vivo com energia contagiante! ⚡",
                "Letras profundas e melodias cativantes! ✨",
                "Produção musical com qualidade questionável 🎧",
                "Artista revelação com talento extraordinário! 🌟"
            ],
            "🛒 Consumo & Marcas": [
                "Produto com design inovador e funcional! 🛍️",
                "Atendimento ao cliente preciso e ágil! 💬",
                "Qualidade abaixo do esperado para o preço 💸",
                "Experiência de compra online fluida! 📱",
                "Entrega rápida e embalagem cuidadosa! 📦"
            ]
        }
        
        dados = dados_por_topico.get(topico, ["Texto de exemplo para análise..."])
        return random.sample(dados, min(quantidade, len(dados)))
    
    def analisar_sentimento(self, texto):
        """Análise de sentimentos usando TextBlob"""
        try:
            analysis = TextBlob(texto)
            polarity = analysis.sentiment.polarity
            
            if polarity > 0.2:
                return "🌟 MUITO POSITIVO", polarity, "#00b894", "🎯"
            elif polarity > 0.05:
                return "✅ POSITIVO", polarity, "#00cec9", "↑"
            elif polarity < -0.2:
                return "💥 MUITO NEGATIVO", polarity, "#d63031", "⚠️"
            elif polarity < -0.05:
                return "❌ NEGATIVO", polarity, "#e17055", "↓"
            else:
                return "⚖️ NEUTRO", polarity, "#fdcb6e", "➡️"
        except:
            return "⚖️ NEUTRO", 0, "#fdcb6e", "➡️"

def main():
    analyzer = AnalisadorSentimentos()
    
    # HEADER
    st.markdown('<h1 class="main-header">🧠 Analisador de Sentimentos</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Análise de sentimentos em textos em português</p>', unsafe_allow_html=True)
    
    # SIDEBAR
    with st.sidebar:
        st.header("🎛️ Configurações")
        
        topico = st.selectbox("Selecione a Categoria:", analyzer.categorias)
        quantidade = st.slider("Quantidade de textos:", 3, 10, 5)
        
        if st.button("🔍 Analisar Sentimentos", use_container_width=True):
            st.session_state.analisar = True
            st.session_state.topico = topico
            st.session_state.quantidade = quantidade
    
    # CONTEÚDO PRINCIPAL
    if st.session_state.get('analisar', False):
        topico = st.session_state.topico
        quantidade = st.session_state.quantidade
        
        with st.spinner("Analisando sentimentos..."):
            textos = analyzer.buscar_dados(topico, quantidade)
            resultados = []
            
            for texto in textos:
                sentimento, score, cor, emoji = analyzer.analisar_sentimento(texto)
                resultados.append({
                    'texto': texto,
                    'sentimento': sentimento,
                    'score': score,
                    'cor': cor,
                    'emoji': emoji
                })
            
            # MÉTRICAS
            col1, col2, col3 = st.columns(3)
            
            with col1:
                positivos = sum(1 for r in resultados if "POSITIVO" in r['sentimento'])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{positivos}</div>
                    <div>Positivos</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                negativos = sum(1 for r in resultados if "NEGATIVO" in r['sentimento'])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{negativos}</div>
                    <div>Negativos</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                neutros = sum(1 for r in resultados if "NEUTRO" in r['sentimento'])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{neutros}</div>
                    <div>Neutros</div>
                </div>
                """, unsafe_allow_html=True)
            
            # GRÁFICO
            st.markdown("---")
            st.subheader("📊 Distribuição de Sentimentos")
            
            df = pd.DataFrame({
                'Sentimento': ['Positivo', 'Negativo', 'Neutro'],
                'Quantidade': [positivos, negativos, neutros]
            })
            
            fig = px.bar(df, x='Sentimento', y='Quantidade', 
                        color='Sentimento',
                        color_discrete_map={
                            'Positivo': '#00b894', 
                            'Negativo': '#d63031', 
                            'Neutro': '#fdcb6e'
                        })
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # ANÁLISE DETALHADA
            st.markdown("---")
            st.subheader(f"🔍 Análise Detalhada: {topico}")

            for resultado in resultados:
                st.markdown(f"""
                <div class="tweet-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <p style="margin: 0; line-height: 1.5;">{resultado['texto']}</p>
                            <small style="color: #666;">Score: {resultado['score']:.2f}</small>
                        </div>
                        <div style="text-align: right;">
                            <div class="sentiment-badge" style="background-color: {resultado['cor']}20; color: {resultado['cor']}; border: 1px solid {resultado['cor']}40;">
                                <strong>{resultado['emoji']} {resultado['sentimento']}</strong>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # TELA INICIAL
        st.info("💡 **Como usar:** Selecione uma categoria no menu lateral e clique em 'Analisar Sentimentos' para começar.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Funcionalidades")
            st.write("""
            - Análise de sentimentos em tempo real
            - Dashboard interativo com gráficos
            - Suporte a múltiplas categorias
            - Interface simples e intuitiva
            """)
        
        with col2:
            st.subheader("🛠️ Tecnologias")
            st.write("""
            - Python
            - Streamlit
            - TextBlob (NLP)
            - Plotly (gráficos)
            - Pandas (dados)
            """)

if __name__ == "__main__":
    if 'analisar' not in st.session_state:
        st.session_state.analisar = False
    
    main()
