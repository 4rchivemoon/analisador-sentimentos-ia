#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🐦 ANALISADOR DE TWEETS - VERSÃO ALTERNATIVA")
print("=" * 55)
print("💡 Usando dados simulados baseados em tendências reais")
print()

from config import TWITTER_KEYS
import tweepy
import random
from datetime import datetime, timedelta

class TwitterSimulacaoRealista:
    def __init__(self):
        # Dados baseados em tendências reais do Twitter
        self.tweets_tecnologia = [
            "ChatGPT está revolucionando a forma como trabalhamos! Incrível demais! 🤖",
            "Meu novo MacBook é fantástico, performance absurda! 💻",
            "Python continua sendo a melhor linguagem para data science! 🐍",
            "Odeio quando o Windows atualiza sozinho e trava tudo! 😠",
            "Inteligência Artificial está assustadora, mas incrível ao mesmo tempo!",
            "Comprei um fone Bluetooth novo e a qualidade é horrível, que decepção!",
            "GitHub Copilot mudou minha vida de programador! Recomendo demais!",
            "Smartphone Android travando toda hora, que produto ruim!",
            "Metaverso é uma furada completa, ninguém aguenta mais!",
            "Linux é sensacional para desenvolvimento, sistema perfeito! 🐧",
            "5G chegando no Brasil e a velocidade é maravilhosa! 🚀",
            "Bateria do meu iPhone não dura nada, produto superestimado!",
            "Home office com setup gamer é a melhor coisa do mundo! 🎮",
            "Serviço de streaming caro e catálogo meia boca, não vale a pena!",
            "Realidade Virtual é uma experiência fantástica, mind blowing! 🕶️"
        ]
        
        self.tweets_ciencia = [
            "James Webb Telescope revelando segredos do universo! Espetacular! 🔭",
            "Vacinas mRNA são a maior conquista científica do século! 💉",
            "Mudanças climáticas são assustadoras, precisamos agir agora! 🌍",
            "CRISPR vai curar doenças genéticas, tecnologia incrível! 🧬",
            "Negacionismo científico é o câncer da nossa sociedade! 😠",
            "Chegar em Marte será realidade em breve, emocionante! 🚀",
            "Artigos científicos atrás de paywall são uma injustiça!",
            "Mulheres na ciência fazendo descobertas incríveis! 👩🔬",
            "Cortes na educação científica são um crime contra o futuro!",
            "Bioquímica é fascinante, amo estudar sobre DNA! 🧪"
        ]

    def buscar_tweets_simulados(self, topico, quantidade=8):
        """Simula busca por tweets com dados realistas"""
        print(f"🔍 Simulando busca por tweets sobre: '{topico}'")
        
        topico = topico.lower()
        
        # Selecionar base de tweets baseada no tópico
        if topico in ['tecnologia', 'tech', 'python', 'programação']:
            base_tweets = self.tweets_tecnologia
        elif topico in ['ciencia', 'ciência', 'pesquisa']:
            base_tweets = self.tweets_ciencia
        else:
            # Combinar para tópicos genéricos
            base_tweets = self.tweets_tecnologia + self.tweets_ciencia
        
        # Selecionar tweets aleatórios
        tweets_selecionados = random.sample(base_tweets, min(quantidade, len(base_tweets)))
        
        # Adicionar dados realistas
        tweets_com_dados = []
        for texto in tweets_selecionados:
            tweets_com_dados.append({
                'texto': texto,
                'usuario': f'user_{random.randint(1000, 9999)}',
                'nome': f'Usuário {random.randint(1, 100)}',
                'seguidores': random.randint(100, 50000),
                'data': datetime.now() - timedelta(hours=random.randint(1, 24)),
                'likes': random.randint(0, 250),
                'retweets': random.randint(0, 50),
                'localizacao': random.choice(['São Paulo', 'Rio de Janeiro', 'Brasília', 'Portugal', 'Não informada'])
            })
        
        print(f"✅ {len(tweets_com_dados)} tweets simulados gerados")
        return tweets_com_dados

class AnalisadorPortugues:
    def __init__(self):
        self.positivas = {
            'amo': 3, 'adoro': 3, 'incrível': 2, 'fantástico': 2, 'sensacional': 2,
            'maravilhoso': 2, 'perfeito': 2, 'excelente': 2, 'ótimo': 1, 'bom': 1,
            'top': 2, 'show': 2, 'maneiro': 1, 'curti': 1, 'gostei': 1, 'amei': 2,
            'recomendo': 1, 'nota10': 2, 'feliz': 1, 'alegre': 1, 'emocionante': 2,
            'revolucionando': 2, 'absurda': 2, 'melhor': 1, 'fantastico': 2
        }
        
        self.negativas = {
            'odeio': 3, 'detesto': 3, 'horrível': 2, 'terrível': 2, 'péssimo': 2,
            'ruim': 1, 'lixo': 3, 'porcaria': 2, 'horroroso': 2, 'decepcionante': 2,
            'furada': 2, 'assustadora': 2, 'travando': 1, 'superestimado': 1,
            'meia boca': 2, 'câncer': 3, 'crime': 2, 'injustiça': 1
        }

    def analisar(self, texto):
        texto = texto.lower()
        score = 0
        palavras_detectadas = []
        
        for palavra in texto.split():
            if palavra in self.positivas:
                score += self.positivas[palavra]
                palavras_detectadas.append(f"➕{palavra}")
            elif palavra in self.negativas:
                score += self.negativas[palavra]
                palavras_detectadas.append(f"➖{palavra}")
        
        if score >= 3:
            return "😍 MUITO POSITIVO", score, palavras_detectadas
        elif score >= 1:
            return "😊 POSITIVO", score, palavras_detectadas
        elif score <= -3:
            return "🤬 MUITO NEGATIVO", score, palavras_detectadas
        elif score <= -1:
            return "😠 NEGATIVO", score, palavras_detectadas
        else:
            return "😐 NEUTRO", score, palavras_detectadas

def main():
    print("🎯 ANALISADOR DE SENTIMENTOS - DADOS REALISTAS")
    print("=" * 50)
    
    simulador = TwitterSimulacaoRealista()
    analisador = AnalisadorPortugues()
    
    print("\n💡 TÓPICOS DISPONÍVEIS: tecnologia, ciencia, python, programação")
    
    while True:
        try:
            query = input("\n🔍 Sobre o que analisar tweets? (ou 'sair'): ")
            
            if query.lower() == 'sair':
                print("👋 Até mais! Obrigado por usar o analisador!")
                break
            
            if not query.strip():
                continue
            
            # Buscar tweets simulados
            tweets = simulador.buscar_tweets_simulados(query, 8)
            
            print(f"\n📊 ANALISANDO SENTIMENTOS SOBRE '{query.upper()}':")
            print("=" * 50)
            
            resultados = []
            for i, tweet in enumerate(tweets, 1):
                sentimento, score, palavras = analisador.analisar(tweet['texto'])
                
                print(f"\n🐦 TWEET {i}:")
                print(f"   👤 @{tweet['usuario']} ({tweet['nome']})")
                print(f"   📍 {tweet['localizacao']}")
                print(f"   📝 {tweet['texto']}")
                print(f"   📅 {tweet['data'].strftime('%d/%m %H:%M')}")
                print(f"   ❤️  {tweet['likes']} likes | 🔄 {tweet['retweets']} RTs")
                print(f"   🎯 {sentimento} (score: {score})")
                
                if palavras:
                    print(f"   🔍 {', '.join(palavras[:3])}")
                
                resultados.append(sentimento)
            
            # Estatísticas
            print(f"\n📈 RESUMO: SENTIMENTOS SOBRE '{query.upper()}'")
            print("-" * 40)
            
            total = len(resultados)
            muito_positivo = resultados.count("😍 MUITO POSITIVO")
            positivo = resultados.count("😊 POSITIVO") 
            muito_negativo = resultados.count("🤬 MUITO NEGATIVO")
            negativo = resultados.count("😠 NEGATIVO")
            neutro = resultados.count("😐 NEUTRO")
            
            total_positivo = muito_positivo + positivo
            total_negativo = muito_negativo + negativo
            
            print(f"😍 Muito positivo: {muito_positivo}")
            print(f"😊 Positivo: {positivo}")
            print(f"😐 Neutro: {neutro}") 
            print(f"😠 Negativo: {negativo}")
            print(f"🤬 Muito negativo: {muito_negativo}")
            
            # Percentuais
            print(f"\n📊 PORCENTAGENS:")
            print(f"   😊 Positivos: {total_positivo/total*100:.1f}%")
            print(f"   😠 Negativos: {total_negativo/total*100:.1f}%")
            print(f"   😐 Neutros: {neutro/total*100:.1f}%")
            
            # Barra visual
            print(f"\n📊 GRÁFICO:")
            barra = "😊" * total_positivo + "😠" * total_negativo + "😐" * neutro
            print(f"   [{barra}]")
            
            # Sentimento geral
            if total_positivo > total_negativo and total_positivo > neutro:
                geral = "😊 MAIORIA POSITIVA"
            elif total_negativo > total_positivo and total_negativo > neutro:
                geral = "😠 MAIORIA NEGATIVA" 
            else:
                geral = "😐 MAIORIA NEUTRA"
            
            print(f"\n🎭 SENTIMENTO GERAL: {geral}")
            
            print("\n" + "✨" * 40)
            
        except KeyboardInterrupt:
            print("\n\n👋 Programa encerrado!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue

if __name__ == "__main__":
    main()