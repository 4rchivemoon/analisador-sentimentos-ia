#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🎉 Testando instalação no macOS...")

# Testar imports
try:
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import CountVectorizer
    import nltk
    import matplotlib.pyplot as plt
    
    print("✅ Todas as bibliotecas importadas com sucesso!")
    print(f"📊 Pandas version: {pd.__version__}")
    print(f"🔢 NumPy version: {np.__version__}")
    
except ImportError as e:
    print(f"❌ Erro: {e}")
    print("Execute: pip3 install pandas numpy scikit-learn nltk matplotlib")

# Teste simples de análise de sentimentos
print("\n🧠 Testando análise de sentimentos básica...")

frases = [
    "adoro macos é muito bom",
    "odeio quando trava", 
    "que sistema incrível",
    "péssima experiência"
]

def analisar_sentimento_mac(texto):
    texto = texto.lower()
    positivas = ["adoro", "bom", "incrível", "ótimo", "excelente"]
    negativas = ["odeio", "péssima", "horrível", "trava", "ruim"]
    
    score = 0
    for palavra in texto.split():
        if palavra in positivas:
            score += 1
        elif palavra in negativas:
            score -= 1
    
    if score > 0:
        return "😊 POSITIVO"
    elif score < 0:
        return "😠 NEGATIVO"
    else:
        return "😐 NEUTRO"

# Testar
for frase in frases:
    resultado = analisar_sentimento_mac(frase)
    print(f"'{frase}' → {resultado}")

print("\n🎉 Setup completo! Se chegou até aqui, está pronto!")