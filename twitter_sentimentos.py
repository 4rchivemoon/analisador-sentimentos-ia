#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🐦 ANALISADOR DE TWEETS BRASILEIROS EM TEMPO REAL")
print("=" * 65)

import tweepy
import pandas as pd
import re
from datetime import datetime
import time

# Configurações (Vamos usar uma forma alternativa sem API keys primeiro)
print("🔧 Iniciando analisador de tweets...")

# Nosso analisador de sentimentos em português
class AnalisadorPortugues:
    def __init__(self):
        # Palavras-chave em português com pesos
        self.palavras_positivas = {
            'amo': 3, 'adoro': 3, 'incrível': 2, 'fantástico': 2, 'sensacional': 2,
            'maravilhoso': 2, 'perfeito': 2, 'excelente': 2, 'ótimo': 1, 'bom': 1,
            'top': 2, 'show': 2, 'maneiro': 1, 'curti': 1, 'gostei': 1, 'amei': 2,
            'recomendo': 1, 'nota10': 2, 'showdebola': 2, 'topdemais': 2,
            'feliz': 1, 'alegre': 1, 'content': 1, 'sortudo': 1, 'grato': 1,
            'sucesso': 1, 'vitória': 1, 'ganhou': 1, 'venceu': 1
        }
        
        self.palavras_negativas = {
            'odeio': 3, 'detesto': 3, 'horrível': 2, 'terrível': 2, 'péssimo': 2,
            'ruim': 1, 'lixo': 3, 'porcaria': 2, 'horroroso': 2, 'decepcionante': 2,
            'furada': 2, 'golpe': 2, 'arrependimento': 2, 'perdadetempo': 2,
            'triste': 1, 'chateado': 1, 'decepcionado': 1, 'frustrado': 1,
            'raiva': 2, 'ódio': 2, 'revolta': 1, 'indignado': 1,
            'derrota': 1, 'perdeu': 1, 'fracasso': 1, 'problema': 1
        }
        
        # Expressões compostas típicas do Brasil
        self.expressoes_positivas = [
            'show de bola', 'top demais', 'custo benefício', 'nota dez',
            'vale a pena', 'muito bom', 'superou expectativas'
        ]
        
        self.expressoes_negativas = [
            'dinheiro jogado fora', 'não comprem', 'não recomendo',
            'péssima experiência', 'que bagunça', 'que droga'
        ]

    def limpar_texto(self, texto):
        """Limpa o texto do tweet"""
        if not texto:
            return ""
        
        # Remove URLs, menções e hashtags
        texto = re.sub(r'http\S+', '', texto)
        texto = re.sub(r'@\w+', '', texto)
        texto = re.sub(r'#\w+', '', texto)
        texto = re.sub(r'\n', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        
        return texto.lower()

    def analisar_tweet(self, texto):
        """Analisa o sentimento de um tweet"""
        texto_limpo = self.limpar_texto(texto)
        
        if not texto_limpo:
            return "NEUTRO", 0, []
        
        score = 0
        palavras_detectadas = []
        
        # Verificar expressões compostas primeiro
        for expressao in self.expressoes_positivas:
            if expressao in texto_limpo:
                score += 2
                palavras_detectadas.append(f"➕ '{expressao}'")
        
        for expressao in self.expressoes_negativas:
            if expressao in texto_limpo:
                score -= 2
                palavras_detectadas.append(f"➖ '{expressao}'")
        
        # Verificar palavras individuais
        palavras = texto_limpo.split()
        for palavra in palavras:
            if palavra in self.palavras_positivas:
                score += self.palavras_positivas[palavra]
                palavras_detectadas.append(f"➕ '{palavra}'")
            elif palavra in self.palavras_negativas:
                score += self.palavras_negativas[palavra]
                palavras_detectadas.append(f"➖ '{palavra}'")
        
        # Classificar baseado no score
        if score >= 3:
            return "😊 MUITO POSITIVO", score, palavras_detectadas
        elif score >= 1:
            return "😊 POSITIVO", score, palavras_detectadas
        elif score <= -3:
            return "😠 MUITO NEGATIVO", score, palavras_detectadas
        elif score <= -1:
            return "😠 NEGATIVO", score, palavras_detectadas
        else:
            return "😐 NEUTRO", score, palavras_detectadas

# Simulador de tweets brasileiros (enquanto não temos API)
class SimuladorTweets:
    def __init__(self):
        self.tweets_exemplo = [
            # Tweets sobre futebol
            "Que jogo incrível do Flamengo! Jogaram demais! 🔥",
            "Odeio quando meu time perde de time pequeno, que raiva!",
            "Gol mais lindo que já vi na minha vida! Sensacional!",
            
            # Tweets sobre política
            "Governo fazendo merda de novo, que situação horrível",
            "Amo as novas medidas econômicas, finalmente algo bom!",
            "Que decepção com nossos políticos, só enganação",
            
            # Tweets sobre tecnologia
            "Python é sensacional para análise de dados! Adorei aprender",
            "Meu código tá cheio de bugs, que ódio disso",
            "ChatGPT é incrível, mudou minha forma de trabalhar",
            
            # Tweets do dia a dia
            "Cafézinho de manhã é tudo de bom! ☕",
            "Trânsito tá um lixo hoje, que stress",
            "Amo final de semana! Hora de descansar!",
            "Chefe sendo chato de novo, que saco",
            "Almoço maravilhoso hoje, comida top!",
            
            # Tweets sobre entretenimento
            "Filme brasileiro incrível, emocionante do começo ao fim",
            "Série nova é uma porcaria, perdendo tempo",
            "Show fantástico ontem, experiência única!",
            
            # Tweets neutros
            "Hoje o dia está normal",
            "Vou ao mercado mais tarde",
            "Assistindo TV em casa"
        ]

    def buscar_tweets_por_topico(self, topico, quantidade=10):
        """Simula busca por tweets sobre um tópico"""
        print(f"🔍 Buscando tweets sobre: '{topico}'")
        
        # Filtrar tweets que contenham palavras do tópico
        tweets_filtrados = []
        palavras_topico = topico.lower().split()
        
        for tweet in self.tweets_exemplo:
            if any(palavra in tweet.lower() for palavra in palavras_topico):
                tweets_filtrados.append(tweet)
        
        # Se não encontrou suficientes, adiciona alguns genéricos
        while len(tweets_filtrados) < quantidade:
            tweets_filtrados.extend(self.tweets_exemplo[:quantidade - len(tweets_filtrados)])
            break
        
        return tweets_filtrados[:quantidade]

# Função principal
def main():
    analisador = AnalisadorPortugues()
    simulador = SimuladorTweets()
    
    print("\n🎯 TÓPICOS DISPONÍVEIS:")
    print("   futebol, política, tecnologia, café, filme, trânsito, trabalho")
    
    while True:
        try:
            topico = input("\n📝 Sobre qual tópico buscar tweets? (ou 'sair'): ")
            
            if topico.lower() == 'sair':
                print("👋 Até mais! Obrigado por usar o analisador!")
                break
            
            if not topico.strip():
                print("⚠️  Por favor, digite um tópico válido")
                continue
            
            print(f"\n🔍 BUSCANDO TWEETS SOBRE: {topico.upper()}")
            print("=" * 50)
            
            # Buscar tweets
            tweets = simulador.buscar_tweets_por_topico(topico, 8)
            
            if not tweets:
                print("❌ Nenhum tweet encontrado para este tópico")
                continue
            
            # Analisar cada tweet
            resultados = []
            for i, tweet in enumerate(tweets, 1):
                sentimento, score, palavras = analisador.analisar_tweet(tweet)
                
                print(f"\n🐦 TWEET {i}:")
                print(f"   📝 '{tweet}'")
                print(f"   🎯 {sentimento} (score: {score})")
                
                if palavras:
                    print(f"   🔍 {', '.join(palavras[:3])}")  # Mostra até 3 palavras
                
                resultados.append(sentimento)
            
            # Estatísticas
            print(f"\n📊 ESTATÍSTICAS DO TÓPICO '{topico.upper()}':")
            total = len(resultados)
            positivos = resultados.count("😊 POSITIVO") + resultados.count("😊 MUITO POSITIVO")
            negativos = resultados.count("😠 NEGATIVO") + resultados.count("😠 MUITO NEGATIVO")
            neutros = resultados.count("😐 NEUTRO")
            
            print(f"   😊 Positivos: {positivos}/{total} ({positivos/total*100:.1f}%)")
            print(f"   😠 Negativos: {negativos}/{total} ({negativos/total*100:.1f}%)")
            print(f"   😐 Neutros: {neutros}/{total} ({neutros/total*100:.1f}%)")
            
            # Sentimento geral
            if positivos > negativos and positivos > neutros:
                sentimento_geral = "😊 MAIORIA POSITIVA"
            elif negativos > positivos and negativos > neutros:
                sentimento_geral = "😠 MAIORIA NEGATIVA"
            else:
                sentimento_geral = "😐 MAIORIA NEUTRA"
            
            print(f"   🎭 SENTIMENTO GERAL: {sentimento_geral}")
            
            print("\n" + "✨" * 30)
            print("Pronto para analisar outro tópico!")
            print("✨" * 30)
            
        except KeyboardInterrupt:
            print("\n\n👋 Programa encerrado!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue

if __name__ == "__main__":
    main()