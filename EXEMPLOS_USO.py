"""
Exemplos de Uso dos Padrões de Projeto
Sistema de Faturamento de Energia

Este arquivo demonstra como usar cada padrão implementado.
Execute: python EXEMPLOS_USO.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from strategies.calculo_tarifa import (
    CalculoResidencial, CalculoComercial, CalculoIndustrial,
    CalculadoraConta, criar_estrategia
)
from decorators.conta_decorators import (
    ContaBase, BandeiraDecorator, ImpostoDecorator,
    TaxaIluminacaoDecorator, criar_conta_completa
)
from infra.tabela_tarifaria import obter_tabela_tarifaria


def separador(titulo):
    """Imprime separador visual"""
    print("\n" + "=" * 80)
    print(f"  {titulo}")
    print("=" * 80 + "\n")


def exemplo_strategy_pattern():
    """Demonstra uso do Strategy Pattern"""
    separador("EXEMPLO 1: STRATEGY PATTERN - Troca Dinâmica de Estratégias")
    
    kwh = 350
    print(f"Consumo: {kwh} kWh\n")
    
    # Cria calculadora com estratégia residencial
    calculadora = CalculadoraConta(CalculoResidencial())
    valor, detalhes, desc = calculadora.calcular_conta(kwh)
    
    print(f"1. {desc}")
    print(f"   Valor: R$ {valor:.2f}")
    for item, val in detalhes.items():
        print(f"   - {item}: R$ {val:.2f}")
    
    print("\n   >>> Trocando para estratégia COMERCIAL...\n")
    
    # TROCA DINÂMICA de estratégia
    calculadora.set_estrategia(CalculoComercial())
    valor, detalhes, desc = calculadora.calcular_conta(kwh)
    
    print(f"2. {desc}")
    print(f"   Valor: R$ {valor:.2f}")
    for item, val in detalhes.items():
        print(f"   - {item}: R$ {val:.2f}")
    
    print("\n   >>> Trocando para estratégia INDUSTRIAL...\n")
    
    # TROCA DINÂMICA novamente
    calculadora.set_estrategia(CalculoIndustrial())
    valor, detalhes, desc = calculadora.calcular_conta(kwh)
    
    print(f"3. {desc}")
    print(f"   Valor: R$ {valor:.2f}")
    for item, val in detalhes.items():
        print(f"   - {item}: R$ {val:.2f}")
    
    print("\n✓ Demonstração: Mesmo objeto (calculadora) com comportamentos diferentes!")


def exemplo_strategy_factory():
    """Demonstra uso da factory de estratégias"""
    separador("EXEMPLO 2: STRATEGY PATTERN - Factory Method")
    
    kwh = 250
    tipos = ['residencial', 'comercial', 'industrial']
    
    print(f"Consumo: {kwh} kWh\n")
    print("Criando estratégias via Factory Method:\n")
    
    for tipo in tipos:
        # Factory cria a estratégia apropriada
        estrategia = criar_estrategia(tipo)
        calculadora = CalculadoraConta(estrategia)
        valor, _, desc = calculadora.calcular_conta(kwh)
        
        print(f"Tipo: {tipo.upper()}")
        print(f"Estratégia: {desc}")
        print(f"Valor: R$ {valor:.2f}\n")
    
    print("✓ Factory Method facilita criação de estratégias!")


def exemplo_decorator_pattern():
    """Demonstra uso do Decorator Pattern"""
    separador("EXEMPLO 3: DECORATOR PATTERN - Composição de Decoradores")
    
    valor_base = 150.00
    kwh = 300
    
    print(f"Valor Base: R$ {valor_base:.2f}")
    print(f"Consumo: {kwh} kWh\n")
    
    # Inicia com conta base
    conta = ContaBase(valor_base)
    print(f"1. Conta Base")
    print(f"   Valor: R$ {conta.get_valor():.2f}\n")
    
    # DECORA com bandeira
    conta = BandeiraDecorator(conta, 'amarela', kwh)
    print(f"2. + Bandeira Amarela")
    print(f"   Valor: R$ {conta.get_valor():.2f}")
    print(f"   Descrição: {conta.get_descricao()}\n")
    
    # DECORA com PIS/COFINS
    conta = ImpostoDecorator(conta, 'pis_cofins')
    print(f"3. + PIS/COFINS")
    print(f"   Valor: R$ {conta.get_valor():.2f}")
    print(f"   Descrição: {conta.get_descricao()}\n")
    
    # DECORA com ICMS
    conta = ImpostoDecorator(conta, 'icms')
    print(f"4. + ICMS")
    print(f"   Valor: R$ {conta.get_valor():.2f}")
    print(f"   Descrição: {conta.get_descricao()}\n")
    
    # DECORA com taxa
    conta = TaxaIluminacaoDecorator(conta)
    print(f"5. + Taxa de Iluminação")
    print(f"   Valor: R$ {conta.get_valor():.2f}")
    print(f"   Descrição: {conta.get_descricao()}\n")
    
    print("Detalhamento Final:")
    for item, valor in conta.get_detalhamento().items():
        print(f"   - {item}: R$ {valor:.2f}")
    
    print(f"\n✓ Demonstração: Decoradores empilhados em camadas!")


def exemplo_decorator_ordem():
    """Demonstra que ordem dos decoradores importa"""
    separador("EXEMPLO 4: DECORATOR PATTERN - Ordem de Aplicação")
    
    valor_base = 100.00
    
    print("Comparando diferentes ordens de decoradores:\n")
    
    # Ordem 1: Imposto depois da taxa
    conta1 = ContaBase(valor_base, "Ordem 1")
    conta1 = TaxaIluminacaoDecorator(conta1, 15.00)  # +15
    conta1 = ImpostoDecorator(conta1, 'icms')         # +18% de 115
    
    print(f"Ordem 1: Taxa → Imposto")
    print(f"   Base: R$ 100.00")
    print(f"   + Taxa R$ 15.00 = R$ 115.00")
    print(f"   + ICMS 18% de R$ 115.00 = R$ {conta1.get_valor():.2f}")
    
    # Ordem 2: Imposto antes da taxa
    conta2 = ContaBase(valor_base, "Ordem 2")
    conta2 = ImpostoDecorator(conta2, 'icms')         # +18% de 100
    conta2 = TaxaIluminacaoDecorator(conta2, 15.00)  # +15
    
    print(f"\nOrdem 2: Imposto → Taxa")
    print(f"   Base: R$ 100.00")
    print(f"   + ICMS 18% de R$ 100.00 = R$ 118.00")
    print(f"   + Taxa R$ 15.00 = R$ {conta2.get_valor():.2f}")
    
    diferenca = abs(conta1.get_valor() - conta2.get_valor())
    print(f"\n✓ Diferença: R$ {diferenca:.2f} - A ordem importa!")


def exemplo_singleton_pattern():
    """Demonstra uso do Singleton Pattern"""
    separador("EXEMPLO 5: SINGLETON PATTERN - Instância Única")
    
    print("Obtendo múltiplas referências da Tabela Tarifária:\n")
    
    # Três formas diferentes de obter a instância
    tabela1 = obter_tabela_tarifaria()
    from infra.tabela_tarifaria import TabelaTarifariaManager
    tabela2 = TabelaTarifariaManager()
    tabela3 = TabelaTarifariaManager.get_instance()
    
    print(f"Tabela 1 ID: {id(tabela1)}")
    print(f"Tabela 2 ID: {id(tabela2)}")
    print(f"Tabela 3 ID: {id(tabela3)}")
    
    if id(tabela1) == id(tabela2) == id(tabela3):
        print("\n✓ Todas são a MESMA instância! (Singleton)")
    
    print(f"\nMês de referência: {tabela1.get_mes_referencia()}")
    
    # Modifica através de uma referência
    print("\nModificando tarifa através da tabela1...")
    tarifa_original = tabela1.get_tarifa('residencial_faixa1')
    print(f"Tarifa original: R$ {tarifa_original:.2f}")
    
    tabela1.atualizar_tarifa('residencial_faixa1', 0.99)
    print(f"Nova tarifa (via tabela1): R$ 0.99")
    
    # Verifica em outra referência
    print(f"\nVerificando na tabela2: R$ {tabela2.get_tarifa('residencial_faixa1'):.2f}")
    print(f"Verificando na tabela3: R$ {tabela3.get_tarifa('residencial_faixa1'):.2f}")
    
    print("\n✓ Mudança visível em todas as referências!")
    
    # Restaura valor original
    tabela1.atualizar_tarifa('residencial_faixa1', tarifa_original)


def exemplo_integracao_completa():
    """Demonstra integração de todos os padrões"""
    separador("EXEMPLO 6: INTEGRAÇÃO COMPLETA - Todos os Padrões Juntos")
    
    print("Calculando conta com todos os padrões integrados:\n")
    
    kwh = 280
    tipo_consumidor = 'residencial'
    tipo_bandeira = 'vermelha1'
    
    print(f"Consumo: {kwh} kWh")
    print(f"Tipo: {tipo_consumidor.title()}")
    print(f"Bandeira: {tipo_bandeira.title()}\n")
    
    # SINGLETON: Obtém tabela única
    tabela = obter_tabela_tarifaria()
    print(f"1. SINGLETON: Tabela Tarifária (ID: {id(tabela)})")
    print(f"   Mês: {tabela.get_mes_referencia()}\n")
    
    # STRATEGY: Calcula valor base
    estrategia = criar_estrategia(tipo_consumidor)
    calculadora = CalculadoraConta(estrategia)
    valor_base, detalhes_base, desc = calculadora.calcular_conta(kwh)
    
    print(f"2. STRATEGY: {desc}")
    print(f"   Valor base: R$ {valor_base:.2f}")
    for item, val in detalhes_base.items():
        print(f"   - {item}: R$ {val:.2f}")
    
    # DECORATOR: Aplica custos adicionais
    print(f"\n3. DECORATOR: Aplicando custos adicionais em camadas...")
    
    conta = ContaBase(valor_base)
    conta = BandeiraDecorator(conta, tipo_bandeira, kwh)
    conta = ImpostoDecorator(conta, 'pis_cofins')
    conta = ImpostoDecorator(conta, 'icms')
    conta = TaxaIluminacaoDecorator(conta)
    
    print(f"\n   Valor final: R$ {conta.get_valor():.2f}")
    print(f"\n   Composição: {conta.get_descricao()}")
    
    print("\n   Detalhamento completo:")
    for item, valor in conta.get_detalhamento().items():
        print(f"   - {item}: R$ {valor:.2f}")
    
    print("\n✓ Todos os 3 padrões trabalhando juntos!")


def exemplo_casos_uso_reais():
    """Demonstra casos de uso práticos"""
    separador("EXEMPLO 7: CASOS DE USO REAIS")
    
    print("Comparando custos entre diferentes perfis de consumo:\n")
    
    cenarios = [
        ("Apartamento Pequeno", 'residencial', 120, 'verde'),
        ("Casa Grande", 'residencial', 450, 'vermelha1'),
        ("Loja", 'comercial', 800, 'amarela'),
        ("Fábrica", 'industrial', 5500, 'vermelha2')
    ]
    
    for nome, tipo, kwh, bandeira in cenarios:
        # Strategy para cálculo base
        estrategia = criar_estrategia(tipo)
        calculadora = CalculadoraConta(estrategia)
        valor_base, _, _ = calculadora.calcular_conta(kwh)
        
        # Decorator para custos totais
        conta = criar_conta_completa(
            valor_base=valor_base,
            kwh=kwh,
            tipo_bandeira=bandeira,
            incluir_impostos=True,
            incluir_taxa_iluminacao=True
        )
        
        print(f"{nome} ({tipo.title()})")
        print(f"   Consumo: {kwh} kWh")
        print(f"   Bandeira: {bandeira.title()}")
        print(f"   Valor base: R$ {valor_base:.2f}")
        print(f"   Valor total: R$ {conta.get_valor():.2f}")
        print(f"   Custo/kWh: R$ {conta.get_valor()/kwh:.2f}\n")
    
    print("✓ Padrões facilitam diferentes cenários de negócio!")


def menu_principal():
    """Menu interativo de exemplos"""
    while True:
        print("\n" + "=" * 80)
        print("  EXEMPLOS DE USO - Sistema de Faturamento de Energia")
        print("=" * 80)
        print("\n1. Strategy Pattern - Troca Dinâmica de Estratégias")
        print("2. Strategy Pattern - Factory Method")
        print("3. Decorator Pattern - Composição de Decoradores")
        print("4. Decorator Pattern - Ordem de Aplicação")
        print("5. Singleton Pattern - Instância Única")
        print("6. Integração Completa - Todos os Padrões")
        print("7. Casos de Uso Reais")
        print("8. Executar TODOS os exemplos")
        print("0. Sair")
        
        try:
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '0':
                print("\nEncerrando exemplos. Até logo!")
                break
            elif opcao == '1':
                exemplo_strategy_pattern()
            elif opcao == '2':
                exemplo_strategy_factory()
            elif opcao == '3':
                exemplo_decorator_pattern()
            elif opcao == '4':
                exemplo_decorator_ordem()
            elif opcao == '5':
                exemplo_singleton_pattern()
            elif opcao == '6':
                exemplo_integracao_completa()
            elif opcao == '7':
                exemplo_casos_uso_reais()
            elif opcao == '8':
                exemplo_strategy_pattern()
                input("\nPressione ENTER para continuar...")
                exemplo_strategy_factory()
                input("\nPressione ENTER para continuar...")
                exemplo_decorator_pattern()
                input("\nPressione ENTER para continuar...")
                exemplo_decorator_ordem()
                input("\nPressione ENTER para continuar...")
                exemplo_singleton_pattern()
                input("\nPressione ENTER para continuar...")
                exemplo_integracao_completa()
                input("\nPressione ENTER para continuar...")
                exemplo_casos_uso_reais()
            else:
                print("\n❌ Opção inválida!")
            
            if opcao != '0' and opcao != '8':
                input("\nPressione ENTER para voltar ao menu...")
                
        except KeyboardInterrupt:
            print("\n\nEncerrando exemplos. Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              Sistema de Faturamento de Energia Elétrica                      ║
║                       EXEMPLOS DE USO DOS PADRÕES                            ║
║                                                                              ║
║  Desenvolvido por: Carlos Henrique Andrade Weege                             ║
║  Padrões: Strategy, Decorator, Singleton                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    menu_principal()