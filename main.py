"""
Sistema de Faturamento de Energia Elétrica
Trabalho 04 - Design Patterns

Desenvolvido por: Carlos Henrique Andrade Weege
GitHub: https://github.com/CarlosWeg

Este sistema implementa três padrões de projeto:
1. Strategy Pattern - Para diferentes estratégias de cálculo de tarifa
2. Decorator Pattern - Para aplicar custos adicionais em camadas
3. Singleton Pattern - Para gerenciar tabela tarifária única

Execução:
    python main.py
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.interface import iniciar_interface


def main():
    """Função principal do sistema"""
    print("="*70)
    print("Sistema de Faturamento de Energia Elétrica")
    print("Desenvolvido por: Carlos Henrique Andrade Weege")
    print("="*70)
    print("\nIniciando interface gráfica...")
    print("\nPadrões implementados:")
    print("  ✓ Strategy Pattern - Cálculo dinâmico por tipo de consumidor")
    print("  ✓ Decorator Pattern - Custos adicionais em camadas")
    print("  ✓ Singleton Pattern - Tabela tarifária única")
    print("="*70)
    print()
    
    try:
        iniciar_interface()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário.")
    except Exception as e:
        print(f"\n\nErro ao iniciar sistema: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()