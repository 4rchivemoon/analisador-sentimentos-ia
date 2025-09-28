#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("📊 DASHBOARD DE ANÁLISE DE SENTIMENTOS")
print("=" * 50)
print("🎯 Visualização profissional dos resultados")
print()

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import random

# Configurar matplotlib para português
plt.rcParams['font.family'] = 'DejaVu Sans'

class DashboardSentimentos:
    def __init__(self):
        self.historico = []
    
    def adicionar_analise(self, topico, resultados):
        """Adiciona análise ao histórico"""
        analise = {
            'topico': topico,
            'data': datetime.now(),
            'total_tweets': len(resultados),
            'positivos': sum(1 for r in resultados if "POSITIVO" in r),
            'negativos': sum(1 for r in resultados if "NEGATIVO" in r),
            'neutros': sum(1 for r in resultados if "NEUTRO" in r)
        }
        self.historico.append(analise)
        return analise
    
    def criar_grafico_pizza(self, analise):
        """Cria gráfico de pizza"""
        labels = ['Positivos 😊', 'Negativos 😠', 'Neutros 😐']
        sizes = [analise['positivos'], analise['negativos'], analise['neutros']]
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title(f'📊 Sentimentos sobre: {analise["topico"].upper()}\n'
                 f'📅 {analise["data"].strftime("%d/%m/%Y %H:%M")} | '
                 f'🐦 {analise["total_tweets"]} tweets analisados')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
    
    def criar_grafico_barras(self, analise):
        """Cria gráfico de barras"""
        categorias = ['Muito Positivo', 'Positivo', 'Neutro', 'Negativo', 'Muito Negativo']
        valores = [
            sum(1 for r in resultados if "MUITO POSITIVO" in r),
            sum(1 for r in resultados if "POSITIVO" in r and "MUITO" not in r),
            sum(1 for r in resultados if "NEUTRO" in r),
            sum(1 for r in resultados if "NEGATIVO" in r and "MUITO" not in r),
            sum(1 for r in resultados if "MUITO NEGATIVO" in r)
        ]
        cores = ['#27ae60', '#2ecc71', '#f39c12', '#e67e22', '#c0392b']
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(categorias, valores, color=cores, edgecolor='black', alpha=0.8)
        
        # Adicionar valores nas barras
        for bar, valor in zip(bars, valores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(valor), ha='center', va='bottom', fontweight='bold')
        
        plt.title(f'📈 Análise Detalhada: {analise["topico"].upper()}', fontsize=14, fontweight='bold')
        plt.xlabel('Categorias de Sentimento')
        plt.ylabel('Quantidade de Tweets')
        plt.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def criar_grafico_evolucao(self):
        """Mostra evolução temporal dos sentimentos"""
        if len(self.historico) < 2:
            print("📈 Colete mais dados para ver a evolução temporal")
            return
        
        datas = [a['data'] for a in self.historico]
        topicos = [a['topico'] for a in self.historico]
        positivos = [a['positivos'] for a in self.historico]
        negativos = [a['negativos'] for a in self.historico]
        
        plt.figure(figsize=(12, 6))
        plt.plot(datas, positivos, marker='o', linewidth=2, label='Positivos 😊', color='#2ecc71')
        plt.plot(datas, negativos, marker='s', linewidth=2, label='Negativos 😠', color='#e74c3c')
        
        plt.title('📈 Evolução Temporal dos Sentimentos', fontsize=14, fontweight='bold')
        plt.xlabel('Data e Hora')
        plt.ylabel('Quantidade de Tweets')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def mostrar_resumo_executivo(self, analise):
        """Mostra relatório executivo"""
        total = analise['total_tweets']
        perc_positivo = (analise['positivos'] / total) * 100
        perc_negativo = (analise['negativos'] / total) * 100
        perc_neutro = (analise['neutros'] / total) * 100
        
        print("\n" + "📋" * 20)
        print("📊 RELATÓRIO EXECUTIVO")
        print("📋" * 20)
        print(f"🎯 Tópico: {analise['topico'].upper()}")
        print(f"📅 Período: {analise['data'].strftime('%d/%m/%Y %H:%M')}")
        print(f"📈 Amostra: {total} tweets analisados")
        print("\n📊 DISTRIBUIÇÃO:")
        print(f"   😊 Positivos: {analise['positivos']} tweets ({perc_positivo:.1f}%)")
        print(f"   😠 Negativos: {analise['negativos']} tweets ({perc_negativo:.1f}%)")
        print(f"   😐 Neutros: {analise['neutros']} tweets ({perc_neutro:.1f}%)")
        
        # Recomendações baseadas na análise
        print("\n💡 RECOMENDAÇÕES:")
        if perc_positivo > 60:
            print("   ✅ Sentimento muito positivo! Ótima aceitação do público.")
        elif perc_negativo > 60:
            print("   ⚠️  Sentimento negativo. Recomenda-se análise das críticas.")
        elif perc_neutro > 50:
            print("   🔄 Opiniões divididas. Público ainda está formando opinião.")
        else:
            print("   📊 Perfil misto. Análise detalhada recomendada.")
        
        print("📋" * 20)

# Dados de exemplo (substitua pelos resultados reais do seu analisador)
resultados_tecnologia = [
    "😍 MUITO POSITIVO", "😊 POSITIVO", "😊 POSITIVO", "😐 NEUTRO",
    "😠 NEGATIVO", "😊 POSITIVO", "🤬 MUITO NEGATIVO", "😊 POSITIVO"
]

resultados_python = [
    "😍 MUITO POSITIVO", "😍 MUITO POSITIVO", "😊 POSITIVO", "😊 POSITIVO",
    "😊 POSITIVO", "😐 NEUTRO", "😊 POSITIVO", "😍 MUITO POSITIVO"
]

def main():
    print("🚀 INICIANDO DASHBOARD PROFISSIONAL...")
    
    dashboard = DashboardSentimentos()
    
    # Adicionar análises de exemplo
    print("\n📥 ADICIONANDO ANÁLISES AO DASHBOARD...")
    
    analise_tech = dashboard.adicionar_analise("tecnologia", resultados_tecnologia)
    analise_python = dashboard.adicionar_analise("python", resultados_python)
    
    while True:
        print("\n📊 MENU DO DASHBOARD:")
        print("1. 📈 Gráfico de Pizza (Tecnologia)")
        print("2. 📊 Gráfico de Barras (Tecnologia)")
        print("3. 🐍 Gráfico de Pizza (Python)")
        print("4. 📈 Gráfico de Barras (Python)")
        print("5. ⏰ Evolução Temporal")
        print("6. 📋 Relatório Executivo")
        print("7. 🚪 Sair")
        
        escolha = input("\n🎯 Escolha uma opção: ")
        
        if escolha == '1':
            print("\n📊 Gerando gráfico de pizza...")
            dashboard.criar_grafico_pizza(analise_tech)
        
        elif escolha == '2':
            print("\n📈 Gerando gráfico de barras...")
            dashboard.criar_grafico_barras(analise_tech)
        
        elif escolha == '3':
            print("\n🐍 Gerando gráfico de pizza (Python)...")
            dashboard.criar_grafico_pizza(analise_python)
        
        elif escolha == '4':
            print("\n📊 Gerando gráfico de barras (Python)...")
            dashboard.criar_grafico_barras(analise_python)
        
        elif escolha == '5':
            print("\n⏰ Gerando gráfico de evolução...")
            dashboard.criar_grafico_evolucao()
        
        elif escolha == '6':
            print("\n📋 Gerando relatório executivo...")
            dashboard.mostrar_resumo_executivo(analise_tech)
        
        elif escolha == '7':
            print("👋 Saindo do dashboard...")
            break
        
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()