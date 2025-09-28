#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🐦 ANALISADOR DE TWEETS REAIS - API TWITTER")
print("=" * 60)
print("🇧🇷 Buscando tweets em português em tempo real!")
print()

# Importar configurações
try:
    from config import TWITTER_KEYS
    print("✅ Chaves da API carregadas com sucesso!")
except ImportError:
    print("❌ Arquivo config.py não encontrado")
    exit()

import tweepy
import re
from datetime import datetime

class TwitterManager:
    def __init__(self):
        self.api = None
        self.conectar()
    
    def conectar(self):
        """Conecta à API do Twitter"""
        try:
            print("🔗 Conectando à API do Twitter...")
            
            # Autenticação
            auth = tweepy.OAuthHandler(
                TWITTER_KEYS["API_KEY"], 
                TWITTER_KEYS["API_SECRET_KEY"]
            )
            auth.set_access_token(
                TWITTER_KEYS["ACCESS_TOKEN"],
                TWITTER_KEYS["ACCESS_TOKEN_SECRET"]
            )
            
            # Criar API
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # Verificar conexão
            user = self.api.verify_credentials()
            print(f"✅ Conectado como: @{user.screen_name}")
            print(f"👤 Nome: {user.name}")
            print(f"📊 Seguidores: {user.followers_count}")
            print("🎯 API Twitter configurada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            print("💡 Verifique se todas as chaves estão corretas")
            return False
    
    def buscar_tweets_ptbr(self, query, quantidade=10):
        """Busca tweets em português"""
        try:
            print(f"🔍 Buscando {quantidade} tweets sobre: '{query}'")
            
            # Buscar tweets em português, excluir retweets
            tweets = self.api.search_tweets(
                q=f"{query} -filter:retweets lang:pt",
                count=quantidade,
                tweet_mode='extended'
            )
            
            tweets_data = []
            for tweet in tweets:
                # Limpar texto do tweet
                texto_limpo = re.sub(r'http\S+', '', tweet.full_text)
                texto_limpo = re.sub(r'@\w+', '', texto_limpo)
                texto_limpo = re.sub(r'#\w+', '', texto_limpo)
                texto_limpo = texto_limpo.strip()
                
                if texto_limpo and len(texto_limpo) > 10:  # Só tweets com conteúdo
                    tweets_data.append({
                        'texto': texto_limpo,
                        'usuario': tweet.user.screen_name,
                        'nome': tweet.user.name,
                        'seguidores': tweet.user.followers_count,
                        'data': tweet.created_at,
                        'likes': tweet.favorite_count,
                        'retweets': tweet.retweet_count,
                        'localizacao': tweet.user.location or "Não informada"
                    })
            
            print(f"✅ {len(tweets_data)} tweets relevantes encontrados")
            return tweets_data
            
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            return []

class AnalisadorPortugues:
    def __init__(self):
        # Dicionário completo para português brasileiro
        self.positivas = {
            'amo': 3, 'adoro': 3, 'incrível': 2, 'fantástico': 2, 'sensacional': 2,
            'maravilhoso': 2, 'perfeito': 2, 'excelente': 2, 'ótimo': 1, 'bom': 1,
            'top': 2, 'show': 2, 'maneiro': 1, 'curti': 1, 'gostei': 1, 'amei': 2,
            'recomendo': 1, 'nota10': 2, 'feliz': 1, 'alegre': 1, 'content': 1,
            'sucesso': 1, 'vitória': 1, 'ganhou': 1, 'venceu': 1, 'love': 2,
            'incrivel': 2, 'maravilhosa': 2, 'perfeita': 2, 'boa': 1
        }
        
        self.negativas = {
            'odeio': 3, 'detesto': 3, 'horrível': 2, 'terrível': 2, 'péssimo': 2,
            'ruim': 1, 'lixo': 3, 'porcaria': 2, 'horroroso': 2, 'decepcionante': 2,
            'furada': 2, 'golpe': 2, 'arrependimento': 2, 'triste': 1, 'chateado': 1,
            'raiva': 2, 'ódio': 2, 'revolta': 1, 'indignado': 1, 'fracasso': 1,
            'horrivel': 2, 'terrivel': 2, 'pessimo': 2, 'decepcionado': 1
        }

    def analisar(self, texto):
        """Analisa sentimento do texto"""
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
    print("🎯 INICIANDO ANALISADOR DE TWEETS REAIS...")
    print("=" * 50)
    
    # Inicializar
    twitter = TwitterManager()
    analisador = AnalisadorPortugues()
    
    if not twitter.api:
        print("❌ Não foi possível conectar à API")
        return
    
    print("\n💡 TÓPICOS SUGERIDOS:")
    print("   futebol, política, netflix, filme, música, python, eleições")
    print("   covid, bitcoin, séries, games, tecnologia, carnaval")
    
    while True:
        try:
            query = input("\n🔍 Sobre o que buscar tweets? (ou 'sair'): ")
            
            if query.lower() == 'sair':
                print("👋 Até mais! Obrigado por usar o analisador!")
                break
            
            if not query.strip():
                print("⚠️  Digite um tópico válido")
                continue
            
            # Buscar tweets
            print(f"\n📡 Conectando ao Twitter...")
            tweets = twitter.buscar_tweets_ptbr(query, 8)
            
            if not tweets:
                print("❌ Nenhum tweet encontrado. Tente outro termo.")
                continue
            
            print(f"\n📊 ANALISANDO {len(tweets)} TWEETS REAIS:")
            print("=" * 50)
            
            resultados = []
            for i, tweet in enumerate(tweets, 1):
                sentimento, score, palavras = analisador.analisar(tweet['texto'])
                
                print(f"\n🐦 TWEET {i}:")
                print(f"   👤 @{tweet['usuario']} ({tweet['nome']})")
                print(f"   📍 {tweet['localizacao']}")
                print(f"   📝 {tweet['texto'][:80]}...")
                print(f"   📅 {tweet['data'].strftime('%d/%m %H:%M')}")
                print(f"   ❤️  {tweet['likes']} likes | 🔄 {tweet['retweets']} RTs")
                print(f"   🎯 {sentimento} (score: {score})")
                
                if palavras:
                    print(f"   🔍 Palavras: {', '.join(palavras[:3])}")
                
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
            print(f"📊 Total: {total} tweets")
            
            # Barra visual
            barra_positivo = "😊" * total_positivo
            barra_negativo = "😠" * total_negativo
            barra_neutro = "😐" * neutro
            
            print(f"📈 [{barra_positivo}{barra_negativo}{barra_neutro}]")
            
            # Sentimento geral
            if total_positivo > total_negativo and total_positivo > neutro:
                geral = "😊 MAIORIA POSITIVA"
            elif total_negativo > total_positivo and total_negativo > neutro:
                geral = "😠 MAIORIA NEGATIVA" 
            else:
                geral = "😐 MAIORIA NEUTRA"
            
            print(f"🎭 SENTIMENTO GERAL: {geral}")
            
            print("\n" + "✨" * 40)
            print("Pronto para analisar outro tópico!")
            print("✨" * 40)
            
        except KeyboardInterrupt:
            print("\n\n👋 Programa encerrado pelo usuário!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue

if __name__ == "__main__":
    main()