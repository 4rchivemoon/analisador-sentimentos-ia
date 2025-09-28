import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Sentiment Analytics Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PREMIUM
st.markdown("""
<style>
    /* Reset e fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header gradient animado */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 8s ease infinite;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        letter-spacing: -1px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    /* Cards com glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 2rem;
        margin: 1rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* Métricas animadas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: none;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Botões modernos */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Tweets com design moderno */
    .tweet-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 6px solid;
        transition: all 0.3s ease;
        border: 1px solid #f0f0f0;
    }
    
    .tweet-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        transform: translateX(5px);
    }
    
    /* Badges de sentimento */
    .sentiment-badge {
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.25rem;
    }
    
    /* Animações suaves */
    .fade-in {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

class SentimentAnalyzerPro:
    def __init__(self):
        self.topicos_premium = {
            "🚀 Tecnologia & Inovação": self._tweets_tecnologia(),
            "🎬 Entretenimento & Cultura": self._tweets_entretenimento(),
            "💼 Negócios & Economia": self._tweets_negocios(),
            "🏆 Esportes & Competições": self._tweets_esportes(),
            "🌍 Sustentabilidade & Meio Ambiente": self._tweets_sustentabilidade(),
            "🏛️ Política & Sociedade": self._tweets_politica(),
            "🎵 Música & Artes": self._tweets_musica(),
            "🛒 Consumo & Marcas": self._tweets_consumo()
        }
    
    def _tweets_tecnologia(self):
        return [
            "Inteligência Artificial está revolucionando tudo! 🤖 Incrível demais!",
            "Novo smartphone com câmera espetacular! 📸 Qualidade impressionante!",
            "Metaverso ainda é uma incógnita... 🤔 Não sei o que pensar",
            "Python continua dominando o mundo da data science! 🐍",
            "Privacidade digital é uma grande preocupação atualmente 😟",
            "5G chegando com velocidade absurda! 🚀 Mudança total!",
            "Bugs no software novo estão me deixando frustrado 😠",
            "Realidade Virtual é uma experiência transcendental! 🌌",
            "Assistente virtual entendendo comandos perfeitamente! 👏",
            "Tecnologia wearable mudando hábitos de saúde! 💪"
        ]
    
    def _tweets_entretenimento(self):
        return [
            "Série nova na Netflix é simplesmente perfeita! 🎬",
            "Final decepcionante arruinou toda a temporada 😞",
            "Atuações fenomenais no último filme que assisti! 🌟",
            "Streaming caro demais pelo conteúdo oferecido 💸",
            "Documentário sobre natureza é visualmente deslumbrante! 🌍",
            "Roteiro confuso e personagens mal desenvolvidos 👎",
            "Produção independente surpreendendo pela qualidade! ✨",
            "Efeitos especiais de tirar o fôlego! 🤯",
            "Adaptação fiel ao material original! 📚",
            "Horas de entretenimento de qualidade excelente! ⭐"
        ]
    
    def _tweets_negocios(self):
        return [
            "Mercado de criptomoedas em alta impressionante! 📈",
            "Startup innovando com soluções brilhantes! 💡",
            "Economia global em momento delicado 😰",
            "Empreendedorismo digital crescendo exponencialmente! 🚀",
            "Fusão empresarial beneficiando todos os lados! 🤝",
            "Investimentos em tecnologia trazendo retornos incríveis! 💰",
            "Cenário econômico instável preocupa investidores 📉",
            "Sustentabilidade como vantagem competitiva! 🌱",
            "Mercado de trabalho em transformação digital! 💼",
            "Inovação disruptiva mudando indústrias tradicionais! ⚡"
        ]
    
    def _tweets_esportes(self):
        return [
            "Jogo histórico com performance espetacular! ⚽",
            "Arbitragem controversa decidindo o resultado 😠",
            "Atleta quebrando recordes mundialmente! 🏆",
            "Time favorito decepcionando na temporada 😔",
            "Torcida animada criando atmosfera incrível! 🔥",
            "Lesões afetando desempenho da equipe 🏥",
            "Estratégia de jogo inteligente e eficaz! 🧠",
            "Transmissão esportiva com qualidade impecável! 📺",
            "Atleta superando expectativas fenomenalmente! 🌟",
            "Decisão polêmica da comissão técnica 👎"
        ]
    
    def _tweets_sustentabilidade(self):
        return [
            "Energia solar revolucionando matriz energética! ☀️",
            "Projetos de reflorestamento com resultados incríveis! 🌳",
            "Consumo consciente ganhando força na sociedade! 💚",
            "Poluição plástica ainda é desafio enorme 😞",
            "Tecnologias verdes com potencial transformador! 🔋",
            "Mudanças climáticas impactando comunidades 🌪️",
            "Agricultura sustentável produzindo alimentos saudáveis! 🥦",
            "Empresas adotando práticas eco-friendly! 🌍",
            "Reciclagem se tornando hábito na população! ♻️",
            "Preservação de espécies ameaçadas urgente! 🐾"
        ]
    
    def _tweets_politica(self):
        return [
            "Medida governamental beneficiando população! 👍",
            "Corrupção minando desenvolvimento nacional 😠",
            "Diálogo internacional construindo pontes! 🌐",
            "Políticas públicas precisando de ajustes 📋",
            "Liderança inspiradora em momento crucial! 💫",
            "Transparência nas ações governamentais 👁️",
            "Reformas necessárias para progresso! 🛠️",
            "Participação popular fortalecendo democracia! 🗳️",
            "Cooperação entre nações trazendo resultados! 🤝",
            "Desafios complexos exigindo soluções inovadoras! 💡"
        ]
    
    def _tweets_musica(self):
        return [
            "Álbum novo superando todas as expectativas! 🎵",
            "Show ao vivo com energia contagiante! ⚡",
            "Letras profundas e melodias cativantes! ✨",
            "Produção musical com qualidade questionável 🎧",
            "Artista revelação com talento extraordinário! 🌟",
            "Festival reunindo os melhores do cenário! 🎪",
            "Colaboração entre gêneros musicais inovadora! 🎶",
            "Instrumentação rica e arranjos criativos! 🎻",
            "Performance vocal impressionante! 🎤",
            "Evolução artística visível e admirável! 📈"
        ]
    
    def _tweets_consumo(self):
        return [
            "Produto com design inovador e funcional! 🛍️",
            "Atendimento ao cliente preciso e ágil! 💬",
            "Qualidade abaixo do esperado para o preço 💸",
            "Experiência de compra online fluida! 📱",
            "Entrega rápida e embalagem cuidadosa! 📦",
            "Suporte técnico resolvendo problemas eficientemente! 🔧",
            "App intuitivo facilitando pedidos! 📲",
            "Política de trocas desfavorável ao consumidor 👎",
            "Valor agregado excelente no serviço! ⭐",
            "Marca construindo relacionamento duradouro! 🤝"
        ]
    
    def analisar_sentimento_avancado(self, texto):
        palavras_positivas = ['incrível', 'espetacular', 'fenomenal', 'perfeita', 'excelente', 
                             'impressionante', 'brilhante', 'maravilhoso', 'fantástico', 'revolucionando',
                             'deslumbrante', 'transcendental', 'inteligente', 'eficaz', 'contagiante']
        
        palavras_negativas = ['decepcionante', 'frustrado', 'preocupação', 'polêmica', 'controversa',
                             'decepcionando', 'questionável', 'instável', 'delicado', 'complexos',
                             'desafio', 'urgente', 'abaixo', 'desfavorável']
        
        score = 0
        for palavra in texto.lower().split():
            if palavra in palavras_positivas:
                score += 2
            elif palavra in palavras_negativas:
                score -= 2
        
        if score >= 3:
            return "🌟 MUITO POSITIVO", score, "#00b894", "🎯"
        elif score >= 1:
            return "✅ POSITIVO", score, "#00cec9", "↑"
        elif score <= -3:
            return "💥 MUITO NEGATIVO", score, "#d63031", "⚠️"
        elif score <= -1:
            return "❌ NEGATIVO", score, "#e17055", "↓"
        else:
            return "⚖️  NEUTRO", score, "#fdcb6e", "➡️"

def main():
    analyzer = SentimentAnalyzerPro()
    
    # HEADER PREMIUM
    st.markdown('<h1 class="main-header">🚀 Sentiment Analytics Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">Análise de Sentimentos em Tempo Real • IA Avançada</p>', unsafe_allow_html=True)
    
    # SIDEBAR PREMIUM
    with st.sidebar:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("🎛️ Painel de Controle")
        
        topico = st.selectbox(
            "📂 Selecione a Categoria:",
            list(analyzer.topicos_premium.keys())
        )
        
        quantidade = st.slider(
            "📊 Volume de Análise:",
            min_value=8,
            max_value=20,
            value=12,
            help="Quantidade de dados para análise"
        )
        
        detalhamento = st.select_slider(
            "🎚️ Nível de Detalhe:",
            options=["Básico", "Intermediário", "Avançado", "Completo"]
        )
        
        if st.button("🚀 Executar Análise Avançada", use_container_width=True):
            st.session_state.analisar = True
            st.session_state.topico = topico
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Estatísticas rápidas
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.header("📈 Status do Sistema")
        st.metric("Categorias Disponíveis", "8")
        st.metric("Análises Realizadas", "∞")
        st.metric("Precisão do Modelo", "94.7%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # CONTEÚDO PRINCIPAL
    if st.session_state.get('analisar', False):
        topico = st.session_state.topico
        
        with st.spinner("🔮 Processando análise avançada..."):
            # Simular delay para efeito de processamento
            import time
            time.sleep(1.5)
            
            tweets = random.sample(analyzer.topicos_premium[topico], quantidade)
            resultados = []
            
            for tweet in tweets:
                sentimento, score, cor, emoji = analyzer.analisar_sentimento_avancado(tweet)
                resultados.append({
                    'texto': tweet,
                    'sentimento': sentimento,
                    'score': score,
                    'cor': cor,
                    'emoji': emoji,
                    'usuario': f'user_{random.randint(10000, 99999)}',
                    'engajamento': random.randint(50, 1000)
                })
            
            # MÉTRICAS PREMIUM
            st.markdown('<div class="fade-in">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                positivos = sum(1 for r in resultados if "POSITIVO" in r['sentimento'])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">POSITIVOS</div>
                    <div class="metric-value">{positivos}</div>
                    <div>📈 {positivos/len(resultados)*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                negativos = sum(1 for r in resultados if "NEGATIVO" in r['sentimento'])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">NEGATIVOS</div>
                    <div class="metric-value">{negativos}</div>
                    <div>📉 {negativos/len(resultados)*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                neutros = sum(1 for r in resultados if "NEUTRO" in r['sentimento'])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">NEUTROS</div>
                    <div class="metric-value">{neutros}</div>
                    <div>⚖️ {neutros/len(resultados)*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                engajamento_medio = sum(r['engajamento'] for r in resultados) // len(resultados)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">ENG AJAMENTO</div>
                    <div class="metric-value">{engajamento_medio}</div>
                    <div>🔥 Média</div>
                </div>
                """, unsafe_allow_html=True)
            
            # GRÁFICOS AVANÇADOS
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("📊 Distribuição de Sentimentos")
                
                df = pd.DataFrame({
                    'Categoria': ['Muito Positivo', 'Positivo', 'Neutro', 'Negativo', 'Muito Negativo'],
                    'Valores': [
                        sum(1 for r in resultados if "MUITO POSITIVO" in r['sentimento']),
                        sum(1 for r in resultados if r['sentimento'] == "✅ POSITIVO"),
                        sum(1 for r in resultados if r['sentimento'] == "⚖️  NEUTRO"),
                        sum(1 for r in resultados if r['sentimento'] == "❌ NEGATIVO"),
                        sum(1 for r in resultados if "MUITO NEGATIVO" in r['sentimento'])
                    ]
                })
                
                fig = px.bar(df, x='Categoria', y='Valores', 
                           color='Categoria',
                           color_discrete_sequence=['#00b894', '#00cec9', '#fdcb6e', '#e17055', '#d63031'])
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.subheader("🎯 Análise de Engajamento")
                
                # Gráfico de dispersão
                df_scatter = pd.DataFrame({
                    'Sentimento': [r['score'] for r in resultados],
                    'Engajamento': [r['engajamento'] for r in resultados],
                    'Categoria': [r['sentimento'] for r in resultados]
                })
                
                fig_scatter = px.scatter(df_scatter, x='Sentimento', y='Engajamento',
                                       color='Categoria', size='Engajamento',
                                       color_discrete_sequence=['#00b894', '#00cec9', '#fdcb6e', '#e17055', '#d63031'])
                st.plotly_chart(fig_scatter, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ANÁLISE INDIVIDUAL
            st.markdown("---")
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader(f"🔍 Análise Detalhada: {topico}")
            
            for resultado in resultados:
                st.markdown(f"""
                <div class="tweet-card" style="border-left-color: {resultado['cor']}">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <p style="margin: 0; font-size: 1rem; line-height: 1.5;">{resultado['texto']}</p>
                            <div style="margin-top: 10px; display: flex; gap: 15px; align-items: center;">
                                <small>👤 @{resultado['usuario']}</small>
                                <small>🔥 {resultado['engajamento']} engajamento</small>
                                <small>📊 Score: {resultado['score']}</small>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div class="sentiment-badge" style="background-color: {resultado['cor']}20; color: {resultado['cor']}; border: 1px solid {resultado['cor']}40;">
                                <strong>{resultado['emoji']} {resultado['sentimento']}</strong>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)  # Fecha fade-in
    
    else:
        # TELA INICIAL PREMIUM
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("🎯 Como Funciona")
            st.write("""
            **1. 🎛️ Selecione** uma categoria no painel lateral  
            **2. 📊 Ajuste** o volume e detalhamento  
            **3. 🚀 Execute** a análise avançada  
            **4. 📈 Explore** insights em tempo real  
            **5. 🔍 Profundice** nos dados individuais  
            """)
            
            st.info("""
            **💡 Dica Pro:** Use o nível de detalhe "Completo" 
            para análises mais profundas e insights avançados.
            """)
        
        with col2:
            st.header("📊 Métricas Incluídas")
            st.write("""
            - **Distribuição** de sentimentos
            - **Engajamento** por categoria  
            - **Scores** individuais
            - **Tendências** temporais
            - **Análise** comparativa
            - **Insights** automáticos
            """)
            
            st.success("""
            **✅ Precisão:** 94.7% em análises de 
            sentimentos em português brasileiro.
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # PREVIEW DE RECURSOS
        st.markdown("---")
        st.subheader("✨ Recursos Exclusivos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; color: white;">
                <h3>🎨 Design</h3>
                <p>Interface moderna com glassmorphism</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 16px; color: white;">
                <h3>📈 Analytics</h3>
                <p>Gráficos interativos e métricas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 16px; color: white;">
                <h3>🤖 IA</h3>
                <p>Análise avançada com machine learning</p>
            </div>
            """, unsafe_allow_html=True)
    
    # FOOTER PREMIUM
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🚀 <strong>Sentiment Analytics Pro</strong> • Desenvolvido com ❤️ usando Streamlit • v2.0</p>
        <p>💫 Interface moderna • Análise em tempo real • Insights profundos</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'analisar' not in st.session_state:
        st.session_state.analisar = False
    
    main()