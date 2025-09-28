#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# Configurar a página
st.set_page_config(
    page_title="Analisador de Sentimentos",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .positive { color: #2ecc71; }
    .negative { color: #e74c3c; }
    .neutral { color: #f39c12; }
</style>
""", unsafe_allow_html=True)

class AnalisadorWeb:
    def __init__(self):
        self.topicos_populares = {
            "Tecnologia": [
                "ChatGPT está revolucionando tudo! Incrível! 🤖",
                "Odeio quando o Windows atualiza sozinho! 😠",
                "Python é a melhor linguagem para Data Science! 🐍",
                "Meu smartphone novo é fantástico! 📱",
                "Internet lenta me deixa muito frustrado!",
                "Realidade Virtual é uma experiência sensacional! 🕶️",
                "Bateria do celular não dura nada, produto ruim!",
                "GitHub Copilot aumentou minha produtividade!",
                "Redes sociais estão viciantes e prejudiciais!",
                "5G chegando com velocidade maravilhosa! 🚀"
            ],
            "Filmes e Séries": [
                "Filme novo do cinema é espetacular! 🎬",
                "Série cancelada, que decepção enorme!",
                "Netflix com catálogo excelente este mês!",
                "Atuações horríveis no último filme que vi!",
                "Documentário incrível, recomendo muito!",
                "Streaming muito caro pelo que oferece!",
                "Final de série foi perfeito e emocionante!",
                "Efeitos especiais uma porcaria completa!",
                "Diretor fez trabalho fantástico! 👏",
                "Perdi tempo assistindo esse lixo!",
            ],
            "Política": [
                "Governo acertou na nova medida! 👍",
                "Políticos só sabem mentir, que nojo!",
                "Reforma importante para o país!",
                "Corrupção nunca acaba, desanimador!",
                "Projeto excelente para educação!",
                "Situação do país é terrível!",
                "Líder fez discurso inspirador!",
                "Que vergonha do nosso congresso!",
                "Medida vai ajudar os mais pobres!",
                "Furioso com as últimas notícias!",
            ],
            "Esportes": [
                "Jogo incrível, time jogou demais! ⚽",
                "Arbitragem horrível, roubaram o jogo!",
                "Jogador foi fantástico, hat-trick!",
                "Derrota dolorosa, time desistiu!",
                "Contratação excelente para o time!",
                "Que time ruim, não acerta nada!",
                "Torcida maravilhosa, apoiou até o final!",
                "Técnico incompetente, tem que sair!",
                "Gol mais bonito que já vi! 🥅",
                "Precisamos de reforços urgentemente!",
            ]
        }
        
        self.palavras_positivas = {
            'amo': 3, 'adoro': 3, 'incrível': 2, 'fantástico': 2, 'sensacional': 2,
            'maravilhoso': 2, 'perfeito': 2, 'excelente': 2, 'ótimo': 1, 'bom': 1,
            'top': 2, 'show': 2, 'maneiro': 1, 'curti': 1, 'gostei': 1, 'amei': 2,
            'recomendo': 1, 'nota10': 2, 'feliz': 1, 'alegre': 1, 'emocionante': 2,
            'revolucionando': 2, 'absurda': 2, 'melhor': 1, 'espetacular': 2
        }
        
        self.palavras_negativas = {
            'odeio': 3, 'detesto': 3, 'horrível': 2, 'terrível': 2, 'péssimo': 2,
            'ruim': 1, 'lixo': 3, 'porcaria': 2, 'horroroso': 2, 'decepcionante': 2,
            'furada': 2, 'assustadora': 2, 'travando': 1, 'superestimado': 1,
            'nojo': 3, 'vergonha': 2, 'frustrado': 1, 'incompetente': 2
        }

    def analisar_sentimento(self, texto):
        texto = texto.lower()
        score = 0
        palavras_detectadas = []
        
        for palavra in texto.split():
            if palavra in self.palavras_positivas:
                score += self.palavras_positivas[palavra]
                palavras_detectadas.append(f"➕{palavra}")
            elif palavra in self.palavras_negativas:
                score += self.palavras_negativas[palavra]
                palavras_detectadas.append(f"➖{palavra}")
        
        if score >= 3:
            return "😍 MUITO POSITIVO", score, palavras_detectadas, "#2ecc71"
        elif score >= 1:
            return "😊 POSITIVO", score, palavras_detectadas, "#27ae60"
        elif score <= -3:
            return "🤬 MUITO NEGATIVO", score, palavras_detectadas, "#c0392b"
        elif score <= -1:
            return "😠 NEGATIVO", score, palavras_detectadas, "#e74c3c"
        else:
            return "😐 NEUTRO", score, palavras_detectadas, "#f39c12"

    def buscar_tweets_simulados(self, topico, quantidade=10):
        if topico in self.topicos_populares:
            base = self.topicos_populares[topico]
        else:
            # Combinar todos os tópicos para busca genérica
            base = []
            for tweets in self.topicos_populares.values():
                base.extend(tweets)
        
        tweets = random.sample(base, min(quantidade, len(base)))
        
        tweets_com_dados = []
        for texto in tweets:
            sentimento, score, palavras, cor = self.analisar_sentimento(texto)
            tweets_com_dados.append({
                'texto': texto,
                'sentimento': sentimento,
                'score': score,
                'palavras_chave': palavras[:3],
                'cor': cor,
                'usuario': f'user_{random.randint(1000, 9999)}',
                'likes': random.randint(0, 500),
                'retweets': random.randint(0, 100),
                'data': datetime.now().strftime("%d/%m %H:%M")
            })
        
        return tweets_com_dados

def main():
    # Inicializar analisador
    analisador = AnalisadorWeb()
    
    # Header principal
    st.markdown('<h1 class="main-header">🤖 ANALISADOR DE SENTIMENTOS</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configurações")
        
        topico = st.selectbox(
            "Escolha um tópico:",
            ["Tecnologia", "Filmes e Séries", "Política", "Esportes", "Personalizado"]
        )
        
        if topico == "Personalizado":
            topico_personalizado = st.text_input("Digite seu tópico:")
            topico = topico_personalizado if topico_personalizado else "Tecnologia"
        
        quantidade = st.slider("Número de tweets:", 5, 20, 10)
        
        analisar_btn = st.button("🎯 Analisar Sentimentos", type="primary")
    
    # Layout principal
    col1, col2 = st.columns([2, 1])
    
    if analisar_btn:
        with st.spinner("🔍 Analisando tweets..."):
            tweets = analisador.buscar_tweets_simulados(topico, quantidade)
            
            if not tweets:
                st.error("❌ Nenhum tweet encontrado para análise.")
                return
            
            # Métricas principais
            st.subheader(f"📊 Análise: {topico}")
            
            col1, col2, col3, col4 = st.columns(4)
            
            total_positivo = sum(1 for t in tweets if "POSITIVO" in t['sentimento'])
            total_negativo = sum(1 for t in tweets if "NEGATIVO" in t['sentimento'])
            total_neutro = sum(1 for t in tweets if "NEUTRO" in t['sentimento'])
            
            with col1:
                st.metric("😊 Positivos", total_positivo)
            with col2:
                st.metric("😠 Negativos", total_negativo)
            with col3:
                st.metric("😐 Neutros", total_neutro)
            with col4:
                sentimento_geral = "😊 Positivo" if total_positivo > total_negativo else "😠 Negativo" if total_negativo > total_positivo else "😐 Neutro"
                st.metric("🎭 Sentimento Geral", sentimento_geral)
            
            # Gráfico de pizza
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Distribuição de Sentimentos")
                
                # DataFrame para gráfico
                df = pd.DataFrame({
                    'Sentimento': ['Positivos', 'Negativos', 'Neutros'],
                    'Quantidade': [total_positivo, total_negativo, total_neutro],
                    'Cor': ['#2ecc71', '#e74c3c', '#f39c12']
                })
                
                fig = px.pie(df, values='Quantidade', names='Sentimento', 
                            color='Sentimento', color_discrete_map={
                                'Positivos': '#2ecc71',
                                'Negativos': '#e74c3c', 
                                'Neutros': '#f39c12'
                            })
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("📊 Análise Detalhada")
                
                # Gráfico de barras
                categorias = ['Muito Positivo', 'Positivo', 'Neutro', 'Negativo', 'Muito Negativo']
                valores = [
                    sum(1 for t in tweets if "MUITO POSITIVO" in t['sentimento']),
                    sum(1 for t in tweets if t['sentimento'] == "😊 POSITIVO"),
                    sum(1 for t in tweets if t['sentimento'] == "😐 NEUTRO"),
                    sum(1 for t in tweets if t['sentimento'] == "😠 NEGATIVO"),
                    sum(1 for t in tweets if "MUITO NEGATIVO" in t['sentimento'])
                ]
                
                fig = go.Figure(data=[
                    go.Bar(x=categorias, y=valores, 
                          marker_color=['#27ae60', '#2ecc71', '#f39c12', '#e67e22', '#c0392b'])
                ])
                fig.update_layout(xaxis_title="Categorias", yaxis_title="Quantidade")
                st.plotly_chart(fig, use_container_width=True)
            
            # Tweets individuais
            st.markdown("---")
            st.subheader("🐦 Tweets Analisados")
            
            for i, tweet in enumerate(tweets, 1):
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**{i}. {tweet['texto']}**")
                        if tweet['palavras_chave']:
                            st.caption(f"🔍 Palavras-chave: {', '.join(tweet['palavras_chave'])}")
                    
                    with col2:
                        st.markdown(f"""
                        <div style='background-color: {tweet['cor']}20; padding: 10px; border-radius: 5px; border-left: 4px solid {tweet['cor']}'>
                            <strong>{tweet['sentimento']}</strong><br>
                            Score: {tweet['score']}<br>
                            ❤️ {tweet['likes']} | 🔄 {tweet['retweets']}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.write("---")
    
    else:
        # Tela inicial
        st.info("🎯 Selecione um tópico e clique em 'Analisar Sentimentos' para começar!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🚀 Como funciona:")
            st.write("""
            1. **Escolha um tópico** ou digite um personalizado
            2. **Selecione quantos tweets** analisar
            3. **Clique em analisar** e veja os resultados
            4. **Explore os gráficos** e métricas
            """)
        
        with col2:
            st.subheader("📊 Métricas:")
            st.write("""
            - **Sentimento geral** do tópico
            - **Distribuição** positiva/negativa/neutra
            - **Análise detalhada** por categoria
            - **Tweets individuais** com scores
            """)
        
        with col3:
            st.subheader("🎯 Use para:")
            st.write("""
            - **Pesquisa de mercado**
            - **Monitoramento de marca**
            - **Análise de opinião pública**
            - **Estudos acadêmicos**
            """)

if __name__ == "__main__":
    main()