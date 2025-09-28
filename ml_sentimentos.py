#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🤖 MACHINE LEARNING - ANÁLISE DE SENTIMENTOS")
print("=" * 55)

# Importar bibliotecas de ML
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

print("✅ Bibliotecas de ML carregadas!")

# Dados de treinamento (exemplos rotulados)
print("\n📚 PREPARANDO DADOS DE TREINAMENTO...")

textos_treinamento = [
    # Positivos
    "adoro esse produto é incrível",
    "excelente qualidade muito bom", 
    "recomendo muito é ótimo",
    "serviço fantástico adorei",
    "produto maravilhoso perfeito",
    "atendimento excelente muito bom",
    "qualidade superior recomendo",
    "experiência positiva gostei",
    
    # Negativos
    "que produto horrível detestei",
    "péssima qualidade não gostei",
    "não recomendo é ruim",
    "atenção horrível péssimo", 
    "serviço terrível muito ruim",
    "qualidade inferior decepcionante",
    "produto defeituoso horrível",
    "experiência negativa odeio"
]

# Rótulos (0 = negativo, 1 = positivo)
rotulos_treinamento = [1, 1, 1, 1, 1, 1, 1, 1,  # positivos
                       0, 0, 0, 0, 0, 0, 0, 0]  # negativos

print(f"📊 Total de exemplos: {len(textos_treinamento)}")
print(f"😊 Positivos: {rotulos_treinamento.count(1)}")
print(f"😠 Negativos: {rotulos_treinamento.count(0)}")

# Criar o modelo de Machine Learning
print("\n🧠 CRIANDO MODELO DE MACHINE LEARNING...")

modelo = make_pipeline(
    CountVectorizer(),      # Converte texto em números
    MultinomialNB()         # Algoritmo que aprende padrões
)

# Treinar o modelo
print("📚 TREINANDO O MODELO...")
modelo.fit(textos_treinamento, rotulos_treinamento)
print("✅ Modelo treinado com sucesso!")

# Testar o modelo
print("\n🧪 TESTANDO O MODELO...")
print("-" * 40)

frases_teste = [
    "gostei muito do produto excelente",
    "que serviço ruim horrível",
    "produto mais ou menos",
    "python é fantástico para IA",
    "odeio quando o código tem bugs",
    "VS Code é bom para programar",
    "péssima experiência não gostei",
    "recomendo é muito bom"
]

for frase in frases_teste:
    # Fazer previsão
    predicao = modelo.predict([frase])[0]
    probabilidade = modelo.predict_proba([frase])[0]
    
    # Converter para resultado legível
    sentimento = "😊 POSITIVO" if predicao == 1 else "😠 NEGATIVO"
    confianca = probabilidade[predicao] * 100
    
    print(f"📝 '{frase}'")
    print(f"   → {sentimento} (confiança: {confianca:.1f}%)")
    print()

# Mostrar estatísticas do modelo
print("\n📈 ESTATÍSTICAS DO MODELO:")
acuracia = modelo.score(textos_treinamento, rotulos_treinamento)
print(f"✅ Acurácia no treinamento: {acuracia * 100:.1f}%")

# Teste interativo
print("\n🔍 TESTE INTERATIVO (digite 'sair' para encerrar)")
print("-" * 50)

while True:
    user_input = input("\nDigite uma frase para analisar: ")
    
    if user_input.lower() == 'sair':
        print("👋 Até a próxima!")
        break
    
    if user_input.strip():
        predicao = modelo.predict([user_input])[0]
        probabilidade = modelo.predict_proba([user_input])[0]
        confianca = probabilidade[predicao] * 100
        
        sentimento = "😊 POSITIVO" if predicao == 1 else "😠 NEGATIVO"
        
        print(f"   🎯 {sentimento} (confiança: {confianca:.1f}%)")
        
        # Mostrar palavras importantes
        if hasattr(modelo, 'named_steps'):
            vectorizer = modelo.named_steps['countvectorizer']
            classifier = modelo.named_steps['multinomialnb']
            
            palavras = vectorizer.get_feature_names_out()
            coefs = classifier.feature_log_prob_[predicao]
            
            # Encontrar palavras mais importantes
            palavras_importantes = sorted(zip(palavras, coefs), 
                                        key=lambda x: x[1], reverse=True)[:3]
            
            print(f"   🔍 Palavras-chave: {[p[0] for p in palavras_importantes]}")