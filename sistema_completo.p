#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import sqlite3
from datetime import datetime, timedelta
import random
import os

# Configuração da página
st.set_page_config(
    page_title="Sistema Completo de Análise",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS premium
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .premium-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid;
        margin: 0.5rem;
        transition: transform 0.2s;
    }
    .premium-card:hover {
        transform: translateY(-5px);
    }
    .positive-card { border-left-color: #00b894; }
    .negative-card { border-left-color: #e17055; }
    .neutral-card { border-left-color: #fdcb6e; }
    .tweet-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.8rem 0;
        border-left: 5px solid;
        transition: all 0.3s ease;
    }
    .tweet-card:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

class DatabaseManager:
    def __init__(self):
        self.db_path = "analises_sentimentos.db"
        self._init_database()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topico TEXT NOT NULL,
                data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_tweets INTEGER,
                positivos INTEGER,
                negativos INTEGER,
                neutros INTEGER,
                sentimento_geral TEXT,
                dados_tweets TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def salvar_analise(self, topico, tweets, resultados):
        """Salva uma análise no banco de dados"""
        total_positivo = sum(1 for t in tweets if "POSITIVO" in t['sentimento'])
        total_negativo = sum(1 for t in tweets if "NEGATIVO" in t['sentimento'])
        total_neutro = sum(1 for t in tweets if "NEUTRO" in t['sentimento'])
        
        sentimento_geral = "POSITIVO" if total_positivo > total_negativo else "NEGATIVO" if total_negativo > total_positivo else "NEUTRO"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analises 
            (topico, total_tweets, positivos, negativos, neutros, sentimento_geral, dados_tweets)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (topico, len(tweets), total_positivo, total_negativo, total_neutro, sentimento_geral, json.dumps(tweets)))
        
        conn.commit()
        conn.close()
    
    def obter_historico(self, limite=10):
        """Obtém o histórico de análises"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analises 
            ORDER BY data_analise DESC 
            LIMIT ?
        ''', (limite,))
        
        resultados = cursor.fetchall()
        conn.close()
        
        historico = []
        for row in resultados:
            historico.append({
                'id': row[0],
                'topico': row[1],
                'data': row[2],
                'total_tweets': row[3],
                'positivos': row[4],
                'negativos': row[5],
                'neutros': row[6],
                'sentimento_geral': row[7],
                'tweets': json.loads(row[8]) if row[8] else []
            })
        
        return historico
    
    def obter_estatisticas(self):
        """Obtém estatísticas gerais"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM analises')
        total_analises = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT topico) FROM analises')
        topicos_unicos = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(total_tweets) FROM analises')
        total_tweets = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_analises': total_analises,
            'topicos_unicos': topicos_unicos,
            'total_tweets': total_tweets
        }

class SistemaAnaliseCompleto:
    def __init__(self):
        self.db = DatabaseManager()
        self.topicos_populares = {
            "🤖 Tecnologia": self._gerar_tweets_tecnologia(),
            "🎬 Entretenimento": self._gerar_tweets_entretenimento(),
            "🏛️ Política": self._gerar_tweets_politica(),
            "⚽ Esportes": self._gerar_tweets_esportes(),
            "🛒 Compras": self._gerar_tweets_compras(),
            "🍔 Alimentação": self._gerar_tweets_alimentacao(),
            "🚗 Automóveis": self._gerar_tweets_automoveis(),
            "🎮 Games": self._gerar_tweets_games()
        }
        
        self.palavras_positivas = {
            'amo': 3, 'adoro': 3, 'incrível': 2, 'fantástico': 2, 'sensacional': 2,
            'maravilhoso': 2, 'perfeito': 2, 'excelente': 2, 'ótimo': 1, 'bom': 1,
            'top': 2, 'show': 2, 'maneiro': 1, 'curti': 1, 'gostei': 1, 'amei': 2,
            'recomendo': 1, 'nota10': 2, 'feliz': 1, 'alegre': 1, 'emocionante': 2,
            'revolucionando': 2, 'absurda': 2, 'melhor': 1, 'espetacular': 2,
            'impressionante': 2, 'fenomenal': 2, 'genial': 2, 'brilhante': 2,
            'excepcional': 2, 'surpreendente': 2, 'formidável': 2
        }
        
        self.palavras_negativas = {
            'odeio': 3, 'detesto': 3, 'horrível': 2, 'terrível': 2, 'péssimo': 2,
            'ruim': 1, 'lixo': 3, 'porcaria': 2, 'horroroso': 2, 'decepcionante': 2,
            'furada': 2, 'assustadora': 2, 'travando': 1, 'superestimado': 1,
            'nojo': 3, 'vergonha': 2, 'frustrado': 1, 'incompetente': 2,
            'catástrofe': 3, 'desastre': 2, 'pessimo': 2, 'horrivel': 2,
            'medíocre': 2, 'lamentável': 2, 'ridículo': 2, 'insuportável': 2
        }

    def _gerar_tweets_tecnologia(self):
        return [
            "ChatGPT está revolucionando tudo! Incrível demais! 🤖",
            "Meu novo MacBook é fantástico, performance absurda! 💻",
            "Python é sensacional para data science! 🐍",
            "Odeio quando o Windows atualiza sozinho! 😠",
            "Inteligência Artificial está impressionante!",
            "Fone Bluetooth novo com qualidade horrível!",
            "GitHub Copilot mudou minha vida! Recomendo!",
            "Smartphone Android travando toda hora!",
            "Metaverso é uma furada completa!",
            "Linux é perfeito para desenvolvimento! 🐧"
        ]

    def _gerar_tweets_entretenimento(self):
        return [
            "Filme novo é simplesmente espetacular! 🎬",
            "Que decepção com a nova série!",
            "Atuações fenomenais no último filme! 👏",
            "Efeitos especiais uma catástrofe!",
            "Documentário incrível, mind blowing!",
            "Streaming caro e catálogo meia boca!",
            "Final de série foi perfeito!",
            "Roteiro horrível, atuações péssimas!",
            "Diretor fez trabalho brilhante!",
            "Pior filme que já vi na vida!"
        ]

    def _gerar_tweets_politica(self):
        return [
            "Governo acertou na nova medida! 👍",
            "Políticos só sabem mentir, que nojo!",
            "Reforma importante para o país!",
            "Corrupção nunca acaba, desanimador!",
            "Projeto excelente para educação!",
            "Situação do país está terrível!",
            "Líder fez discurso inspirador!",
            "Que vergonha do congresso!",
            "Medida vai ajudar milhões!",
            "Estou furioso com as notícias!"
        ]

    def _gerar_tweets_esportes(self):
        return [
            "Jogo incrível, time jogou demais! ⚽",
            "Arbitragem horrível, roubaram o jogo!",
            "Jogador foi fenomenal, hat-trick!",
            "Derrota dolorosa, time desistiu!",
            "Contratação excelente para o elenco!",
            "Que time ruim, não acerta nada!",
            "Torcida maravilhosa, apoiou até o final!",
            "Técnico incompetente, tem que sair!",
            "Gol mais bonito que já vi! 🥅",
            "Precisamos de reforços urgentemente!"
        ]

    def _gerar_tweets_compras(self):
        return [
            "Produto excelente, superou expectativas! 📦",
            "Que decepção com a qualidade!",
            "Entrega super rápida, adorei! 🚚",
            "Atendimento horrível, nunca mais!",
            "Site fácil de usar, experiência ótima!",
            "Produto veio com defeito, que raiva!",
            "Recomendo muito essa loja!",
            "Péssimo custo-benefício!",
            "Embalagem perfeita, muito cuidado!",
            "Golpe completo, produto fake!"
        ]

    def _gerar_tweets_alimentacao(self):
        return [
            "Restaurante novo é fantástico! 🍝",
            "Comida horrível, nunca mais volto!",
            "Hambúrguer mais incrível que já comi! 🍔",
            "Serviço péssimo, demorou horas!",
            "Sobremesa divina, perfeita! 🍰",
            "Preços abusivos, não vale a pena!",
            "Atendimento impecável! 👏",
            "Comida veio fria, que decepção!",
            "Ambiente agradável, música ótima!",
            "Lugar sujo, comida ruim!"
        ]

    def _gerar_tweets_automoveis(self):
        return [
            "Carro novo é espetacular! 🚗",
            "Manutenção cara demais, arrependimento!",
            "Desempenho fantástico na estrada!",
            "Consumo de combustível horrível!",
            "Conforto incrível, amo dirigir!",
            "Problemas constantes, só dor de cabeça!",
            "Design lindo, todo mundo elogia!",
            "Revenda difícil, preço cai muito!",
            "Tecnologia de ponta, sensacional!",
            "Carro beberrão, gasto fortuna!"
        ]

    def _gerar_tweets_games(self):
        return [
            "Jogo novo é viciante! 🎮",
            "Grágicos horríveis, decepcionante!",
            "Gameplay fluida e divertida!",
            "Servidores lagados, impossível jogar!",
            "História emocionante, masterpiece!",
            "Preço abusivo pelo que oferece!",
            "Multiplayer incrível com amigos!",
            "Cheio de bugs, inacabado!",
            "Grágicos lindos, imersivo!",
            "Suporte técnico inexistente!"
        ]

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
            return "😍 MUITO POSITIVO", score, palavras_detectadas, "#00b894", "🟢"
        elif score >= 1:
            return "😊 POSITIVO", score, palavras_detectadas, "#00cec9", "🟢"
        elif score <= -3:
            return "🤬 MUITO NEGATIVO", score, palavras_detectadas, "#d63031", "🔴"
        elif score <= -1:
            return "😠 NEGATIVO", score, palavras_detectadas, "#e17055", "🔴"
        else:
            return "😐 NEUTRO", score, palavras_detectadas, "#fdcb6e", "🟡"

    def buscar_tweets_simulados(self, topico, quantidade=12):
        if topico in self.topicos_populares:
            base = self.topicos_populares[topico]
        else:
            base = list(self.topicos_populares.values())[0]
        
        tweets = random.sample(base, min(quantidade, len(base)))
        
        tweets_com_dados = []
        for texto in tweets:
            sentimento, score, palavras, cor, emoji = self.analisar_sentimento(texto)
            tweets_com_dados.append({
                'texto': texto,
                'sentimento': sentimento,
                'score': score,
                'palavras_chave': palavras[:3],
                'cor': cor,
                'emoji': emoji,
                'usuario': f'user_{random.randint(1000, 9999)}',
                'likes': random.randint(0, 500),
                'retweets': random.randint(0, 100),
                'data': (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime("%d/%m %H:%M")
            })
        
        return tweets_com_dados

def main():
    sistema = SistemaAnaliseCompleto()
    
    # Header premium
    st.markdown('<h1 class="main-header">🤖 SISTEMA COMPLETO DE ANÁLISE</h1>', unsafe_allow_html=True)
    st.markdown("### 🚀 Análise de Sentimentos com Histórico e Banco de Dados")
    st.markdown("---")
    
    # Sidebar avançada
    with st.sidebar:
        st.header("🎯 Controle Principal")
        
        # Abas na sidebar
        aba_principal, aba_historico, aba_estatisticas = st.tabs(["🔍 Análise", "📊 Histórico", "📈 Stats"])
        
        with aba_principal:
            topico = st.selectbox(
                "Selecione o tópico:",
                list(sistema.topicos_populares.keys())
            )
            
            quantidade = st.slider("Tweets para analisar:", 8, 20, 12)
            
            if st.button("🚀 Executar Análise", type="primary", use_container_width=True):
                st.session_state.analisar = True
                st.session_state.topico = topico
                st.session_state.quantidade = quantidade
        
        with aba_historico:
            st.subheader("📜 Últimas Análises")
            historico = sistema.db.obter_historico(5)
            
            if historico:
                for analise in historico:
                    emoji = "😊" if analise['sentimento_geral'] == "POSITIVO" else "😠" if analise['sentimento_geral'] == "NEGATIVO" else "😐"
                    st.write(f"{emoji} **{analise['topico']}**")
                    st.caption(f"📅 {analise['data'][:16]} | 🐦 {analise['total_tweets']} tweets")
            else:
                st.info("Nenhuma análise no histórico")
        
        with aba_estatisticas:
            st.subheader("📊 Estatísticas Gerais")
            stats = sistema.db.obter_estatisticas()
            
            st.metric("Total de Análises", stats['total_analises'])
            st.metric("Tópicos Únicos", stats['topicos_unicos'])
            st.metric("Tweets Analisados", stats['total_tweets'])
    
    # Conteúdo principal
    if st.session_state.get('analisar', False):
        topico = st.session_state.topico
        quantidade = st.session_state.quantidade
        
        with st.spinner("🔍 Analisando sentimentos..."):
            tweets = sistema.buscar_tweets_simulados(topico, quantidade)
            
            # Salvar no banco de dados
            sistema.db.salvar_analise(topico, tweets, {})
            
            # Métricas premium
            st.subheader(f"📊 Análise: {topico}")
            
            total_positivo = sum(1 for t in tweets if "POSITIVO" in t['sentimento'])
            total_negativo = sum(1 for t in tweets if "NEGATIVO" in t['sentimento'])
            total_neutro = sum(1 for t in tweets if "NEUTRO" in t['sentimento'])
            
            # Grid de métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="premium-card positive-card">
                    <h3>😊 Positivos</h3>
                    <h2 style="color: #00b894;">{total_positivo}</h2>
                    <p>{total_positivo/len(tweets)*100:.1f}% do total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="premium-card negative-card">
                    <h3>😠 Negativos</h3>
                    <h2 style="color: #e17055;">{total_negativo}</h2>
                    <p>{total_negativo/len(tweets)*100:.1f}% do total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="premium-card neutral-card">
                    <h3>😐 Neutros</h3>
                    <h2 style="color: #fdcb6e;">{total_neutro}</h2>
                    <p>{total_neutro/len(tweets)*100:.1f}% do total</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                sentimento_geral = "😊 Positivo" if total_positivo > total_negativo else "😠 Negativo" if total_negativo > total_positivo else "😐 Neutro"
                cor_geral = "#00b894" if total_positivo > total_negativo else "#e17055" if total_negativo > total_positivo else "#fdcb6e"
                st.markdown(f"""
                <div class="premium-card" style="border-left-color: {cor_geral}">
                    <h3>🎭 Sentimento Geral</h3>
                    <h2 style="color: {cor_geral};">{sentimento_geral}</h2>
                    <p>Baseado em {len(tweets)} análises</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Visualizações
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Distribuição de Sentimentos")
                
                df = pd.DataFrame({
                    'Categoria': ['Muito Positivo', 'Positivo', 'Neutro', 'Negativo', 'Muito Negativo'],
                    'Quantidade': [
                        sum(1 for t in tweets if "MUITO POSITIVO" in t['sentimento']),
                        sum(1 for t in tweets if t['sentimento'] == "😊 POSITIVO"),
                        sum(1 for t in tweets if t['sentimento'] == "😐 NEUTRO"),
                        sum(1 for t in tweets if t['sentimento'] == "😠 NEGATIVO"),
                        sum(1 for t in tweets if "MUITO NEGATIVO" in t['sentimento'])
                    ]
                })
                
                fig = px.bar(df, x='Categoria', y='Quantidade', 
                           color='Categoria',
                           color_discrete_map={
                               'Muito Positivo': '#00b894',
                               'Positivo': '#00cec9', 
                               'Neutro': '#fdcb6e',
                               'Negativo': '#e17055',
                               'Muito Negativo': '#d63031'
                           })
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🎯 Análise Detalhada")
                
                fig_pizza = px.pie(
                    names=['Positivos', 'Negativos', 'Neutros'],
                    values=[total_positivo, total_negativo, total_neutro],
                    color=['Positivos', 'Negativos', 'Neutros'],
                    color_discrete_map={
                        'Positivos': '#00b894',
                        'Negativos': '#e17055',
                        'Neutros': '#fdcb6e'
                    }
                )
                fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pizza, use_container_width=True)
            
            # Tweets individuais
            st.markdown("---")
            st.subheader(f"🐦 Análise Individual dos Tweets")
            
            for i, tweet in enumerate(tweets, 1):
                st.markdown(f"""
                <div class="tweet-card" style="border-left-color: {tweet['cor']}">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0; color: #2d3436;">{tweet['texto']}</h4>
                            <div style="margin-top: 8px;">
                                <small>👤 @{tweet['usuario']} | 📅 {tweet['data']}</small>
                                <br>
                                <small>❤️ {tweet['likes']} likes | 🔄 {tweet['retweets']} retweets</small>
                                {f'<br><small>🔍 <strong>Palavras-chave:</strong> {", ".join(tweet["palavras_chave"])}</small>' if tweet['palavras_chave'] else ''}
                            </div>
                        </div>
                        <div style="text-align: right; min-width: 120px;">
                            <div style="background: {tweet['cor']}15; padding: 10px; border-radius: 8px; border: 2px solid {tweet['cor']}30;">
                                <strong style="color: {tweet['cor']};">{tweet['emoji']} {tweet['sentimento']}</strong>
                                <br>
                                <small>Score: {tweet['score']}</small>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # Tela inicial premium
        st.success("🎉 Bem-vindo ao Sistema Completo de Análise de Sentimentos!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Recursos do Sistema:")
            st.write("""
            - **🤖 Análise com Machine Learning**
            - **💾 Banco de Dados SQLite integrado**
            - **📊 Histórico completo de análises**
            - **🎯 8 categorias diferentes**
            - **📈 Estatísticas em tempo real**
            - **💫 Interface premium**
            - **🔒 100% local e privado**
            """)
        
        with col2:
            st.subheader("📈 Como Usar:")
            st.write("""
            1. **Selecione um tópico** no menu lateral
            2. **Ajuste a quantidade** de tweets
            3. **Clique em Executar Análise**
            4. **Explore os resultados** completos
            5. **Acesse o histórico** quando quiser
            """)
            
            st.info("""
            **💡 Dica:** Todas as análises são salvas 
            automaticamente no banco de dados local.
            """)
        
        st.markdown("---")
        st.subheader("🎯 Categorias Disponíveis:")
        
        # Grid de categorias
        cols = st.columns(4)
        topicos = list(sistema.topicos_populares.keys())
        
        for i, (col, topico) in enumerate(zip(cols * 2, topicos)):
            with col:
                emoji, nome = topico.split(" ", 1)
                st.info(f"**{emoji} {nome}**")

if __name__ == "__main__":
    if 'analisar' not in st.session_state:
        st.session_state.analisar = False
    
    main()