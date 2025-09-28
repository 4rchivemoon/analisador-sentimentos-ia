#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🇧🇷 ANALISADOR DE SENTIMENTOS - PORTUGUÊS BRASILEIRO")
print("=" * 60)

import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

print("✅ Iniciando analisador para português...")

# Dados ESPECÍFICOS para português brasileiro
print("\n📚 CARREGANDO DATASET EM PORTUGUÊS...")

textos_treinamento = [
    # 😊 POSITIVOS - Expressões típicas do Brasil
    "achei muito bom top demais",
    "gostei bastante curti muito", 
    "maneiro demais show de bola",
    "excelente produto recomendo",
    "muito bom mesmo adorei",
    "qualidade top nota dez",
    "superou expectativas incrível",
    "maravilhoso fantástico sensacional",
    "barato e bom custo benefício",
    "atendimento perfeito impecável",
    "produto chegou rápido",
    "funciona perfeitamente zero defeitos",
    "prático e eficiente amei",
    "vale cada centavo compraria de novo",
    "melhor compra do ano",
    "surpreendeu positivamente",
    
    # 😠 NEGATIVOS - Expressões típicas do Brasil
    "que porcaria lixo completo",
    "péssimo produto não comprem",
    "dinheiro jogado fora",
    "arrependimento total furada",
    "horrível terrível decepcionante", 
    "veio com defeito quebra fácil",
    "atendimento horroroso péssimo",
    "não funciona direito problema",
    "qualidade inferior ruim",
    "golpe enganação mentira",
    "perda de tempo dinheiro",
    "pessimo atendimento demorado",
    "produto veio errado errado",
    "não recomendo pra ninguém",
    "péssima experiência nunca mais",
    "estragou rápido quebrou"
]

rotulos_treinamento = [1] * 16 + [0] * 16  # 16 positivos, 16 negativos

print(f"📊 Dataset carregado: {len(textos_treinamento)} frases em português")

# Pré-processamento específico para português
def preprocessar_ptbr(texto):
    texto = texto.lower()
    
    # Remover caracteres especiais mas manter acentos
    texto = re.sub(r'[^\w\sáàâãéèêíïóôõöúçñ]', '', texto)
    
    # Expressões comuns no Brasil (manter como uma única "palavra")
    expressoes = {
        'show de bola': 'showdebola',
        'top demais': 'topdemais', 
        'dinheiro jogado fora': 'dinheirojogadofora',
        'nota dez': 'notadez',
        'custo benefício': 'custobeneficio',
        'zero defeitos': 'zerodefeitos'
    }
    
    for exp, substituicao in expressoes.items():
        texto = texto.replace(exp, substituicao)
    
    return texto

print("🔧 Aplicando pré-processamento para português...")
textos_processados = [preprocessar_ptbr(texto) for texto in textos_treinamento]

# Criar modelo otimizado para português
modelo_ptbr = make_pipeline(
    CountVectorizer(
        ngram_range=(1, 2),  # Captura palavras simples e combinações
        max_features=100     # Foca nas palavras mais importantes
    ),
    MultinomialNB()
)

print("🧠 TREINANDO MODELO PARA PORTUGUÊS...")
modelo_ptbr.fit(textos_processados, rotulos_treinamento)
print("✅ Modelo treinado com sucesso!")

# Função de análise com detalhes em português
def analisar_detalhado_ptbr(frase):
    frase_processada = preprocessar_ptbr(frase)
    predicao = modelo_ptbr.predict([frase_processada])[0]
    probabilidades = modelo_ptbr.predict_proba([frase_processada])[0]
    
    sentimento = "😊 POSITIVO" if predicao == 1 else "😠 NEGATIVO"
    confianca = probabilidades[predicao] * 100
    
    # Analisar palavras específicas do português
    palavras_positivas_br = ['top', 'show', 'maneiro', 'curti', 'gostei', 'amei', 'adorei', 'incrível']
    palavras_negativas_br = ['porcaria', 'péssimo', 'horroroso', 'furada', 'arrependimento', 'golpe']
    
    palavras_detectadas = []
    for palavra in frase.lower().split():
        if palavra in palavras_positivas_br:
            palavras_detectadas.append(f"➕'{palavra}'")
        elif palavra in palavras_negativas_br:
            palavras_detectadas.append(f"➖'{palavra}'")
    
    return sentimento, confianca, palavras_detectadas

# Testar com expressões brasileiras
print("\n🧪 TESTANDO COM EXPRESSÕES BRASILEIRAS:")
print("-" * 50)

testes_brasileiros = [
    "achei top demais show de bola",
    "que porcaria dinheiro jogado fora", 
    "produto maneiro curti muito",
    "golpe completo furada",
    "custo benefício excelente",
    "atendimento horroroso péssimo",
    "nota dez recomendo",
    "arrependimento total não comprem"
]

for frase in testes_brasileiros:
    sentimento, confianca, palavras = analisar_detalhado_ptbr(frase)
    
    print(f"📝 '{frase}'")
    print(f"   → {sentimento} ({confianca:.1f}% de confiança)")
    if palavras:
        print(f"   🔍 {', '.join(palavras)}")
    print()

# Estatísticas em português
acuracia_ptbr = modelo_ptbr.score(textos_processados, rotulos_treinamento)
print(f"📈 Acurácia para português: {acuracia_ptbr * 100:.1f}%")

# Teste interativo BR
print("\n🔄 MODO INTERATIVO BR (digite 'sair' para parar)")
print("-" * 50)

while True:
    try:
        user_input = input("\n😊 Digite uma frase em português: ")
        
        if user_input.lower() == 'sair':
            print("👋 Valeu! Até mais!")
            break
        
        if user_input.strip():
            sentimento, confianca, palavras = analisar_detalhado_ptbr(user_input)
            print(f"   🎯 {sentimento} ({confianca:.1f}% de confiança)")
            
            if confianca < 70:
                print("   ⚠️  Confiança baixa - talvez seja neutro?")
            
    except KeyboardInterrupt:
        print("\n\n👋 Programa encerrado pelo usuário!")
        break

print("\n✨ Analisador de sentimentos em português brasileiro - PRONTO! 🎊")