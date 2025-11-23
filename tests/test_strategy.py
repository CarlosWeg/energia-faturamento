"""
Testes para Strategy Pattern

Testa comportamentos-chave do padrão:
1. Troca dinâmica de estratégias
2. Cálculo correto por faixas
3. Múltiplas instâncias com estratégias diferentes
"""

import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.calculo_tarifa import (
    CalculoResidencial,
    CalculoComercial,
    CalculoIndustrial,
    CalculadoraConta,
    criar_estrategia
)


class TestCalculoResidencial:
    """Testes da estratégia residencial"""
    
    def test_calculo_faixa1(self):
        """Testa cálculo na primeira faixa (0-100 kWh)"""
        estrategia = CalculoResidencial()
        valor, detalhes = estrategia.calcular(50)
        
        # 50 kWh * R$ 0.50 = R$ 25.00
        assert valor == pytest.approx(25.00)
        assert "Faixa 1" in str(detalhes)
    
    def test_calculo_faixa2(self):
        """Testa cálculo na segunda faixa (101-300 kWh)"""
        estrategia = CalculoResidencial()
        valor, detalhes = estrategia.calcular(200)
        
        # 100 kWh * R$ 0.50 + 100 kWh * R$ 0.65 = R$ 115.00
        esperado = (100 * 0.50) + (100 * 0.65)
        assert valor == pytest.approx(esperado)
        assert len(detalhes) == 2  # Duas faixas
    
    def test_calculo_faixa3(self):
        """Testa cálculo na terceira faixa (>300 kWh)"""
        estrategia = CalculoResidencial()
        valor, detalhes = estrategia.calcular(400)
        
        # 100*0.50 + 200*0.65 + 100*0.85
        esperado = (100 * 0.50) + (200 * 0.65) + (100 * 0.85)
        assert valor == pytest.approx(esperado)
        assert len(detalhes) == 3  # Três faixas
    
    def test_descricao(self):
        """Testa descrição da estratégia"""
        estrategia = CalculoResidencial()
        assert "Residencial" in estrategia.get_descricao()


class TestCalculoComercial:
    """Testes da estratégia comercial"""
    
    def test_calculo_sem_desconto(self):
        """Testa cálculo comercial sem desconto (<500 kWh)"""
        estrategia = CalculoComercial()
        valor, detalhes = estrategia.calcular(300)
        
        # 300 kWh * R$ 0.75 = R$ 225.00
        assert valor == pytest.approx(225.00)
        assert len(detalhes) == 1  # Sem desconto
    
    def test_calculo_desconto_5(self):
        """Testa desconto de 5% (>500 kWh)"""
        estrategia = CalculoComercial()
        valor, detalhes = estrategia.calcular(600)
        
        valor_base = 600 * 0.75
        desconto = valor_base * 0.05
        esperado = valor_base - desconto
        
        assert valor == pytest.approx(esperado)
        assert "Desconto" in str(detalhes)
    
    def test_calculo_desconto_10(self):
        """Testa desconto de 10% (>1000 kWh)"""
        estrategia = CalculoComercial()
        valor, detalhes = estrategia.calcular(1500)
        
        valor_base = 1500 * 0.75
        desconto = valor_base * 0.10
        esperado = valor_base - desconto
        
        assert valor == pytest.approx(esperado)


class TestCalculoIndustrial:
    """Testes da estratégia industrial"""
    
    def test_calculo_com_demanda(self):
        """Testa inclusão da tarifa de demanda"""
        estrategia = CalculoIndustrial()
        valor, detalhes = estrategia.calcular(1000)
        
        # Deve incluir tarifa de demanda
        assert "Tarifa de Demanda" in detalhes
        assert detalhes["Tarifa de Demanda"] == 25.00
    
    def test_desconto_industrial(self):
        """Testa descontos industriais"""
        estrategia = CalculoIndustrial()
        
        # >2000 kWh: desconto de 12%
        valor1, detalhes1 = estrategia.calcular(3000)
        assert "Desconto Industrial" in str(detalhes1)
        
        # >5000 kWh: desconto de 18%
        valor2, detalhes2 = estrategia.calcular(6000)
        assert "Desconto Industrial" in str(detalhes2)
        
        # Maior consumo deve ter maior desconto percentual
        assert valor2 / 6000 < valor1 / 3000


class TestCalculadoraConta:
    """Testes do Context (troca dinâmica de estratégias)"""
    
    def test_troca_dinamica_estrategia(self):
        """
        TESTE CRÍTICO: Troca dinâmica de estratégias
        
        Este é o comportamento-chave do padrão Strategy.
        """
        kwh = 300
        
        # Inicia com estratégia residencial
        calculadora = CalculadoraConta(CalculoResidencial())
        valor1, _, desc1 = calculadora.calcular_conta(kwh)
        
        # Troca para estratégia comercial
        calculadora.set_estrategia(CalculoComercial())
        valor2, _, desc2 = calculadora.calcular_conta(kwh)
        
        # Troca para estratégia industrial
        calculadora.set_estrategia(CalculoIndustrial())
        valor3, _, desc3 = calculadora.calcular_conta(kwh)
        
        # Valores devem ser diferentes
        assert valor1 != valor2
        assert valor2 != valor3
        assert valor1 != valor3
        
        # Descrições devem corresponder às estratégias
        assert "Residencial" in desc1
        assert "Comercial" in desc2
        assert "Industrial" in desc3
    
    def test_multiplas_instancias_estrategias_diferentes(self):
        """
        Testa múltiplas calculadoras com estratégias diferentes
        
        Demonstra que o padrão Strategy permite que diferentes
        objetos tenham comportamentos distintos.
        """
        kwh = 500
        
        calc_residencial = CalculadoraConta(CalculoResidencial())
        calc_comercial = CalculadoraConta(CalculoComercial())
        calc_industrial = CalculadoraConta(CalculoIndustrial())
        
        valor_res, _, _ = calc_residencial.calcular_conta(kwh)
        valor_com, _, _ = calc_comercial.calcular_conta(kwh)
        valor_ind, _, _ = calc_industrial.calcular_conta(kwh)
        
        # Todos devem ter valores diferentes
        assert valor_res != valor_com
        assert valor_com != valor_ind
        assert valor_res != valor_ind
    
    def test_validacao_consumo_negativo(self):
        """Testa validação de consumo negativo"""
        calculadora = CalculadoraConta(CalculoResidencial())
        
        with pytest.raises(ValueError):
            calculadora.calcular_conta(-100)


class TestFactoryEstrategia:
    """Testa factory method para criar estratégias"""
    
    def test_criar_residencial(self):
        """Testa criação de estratégia residencial"""
        estrategia = criar_estrategia('residencial')
        assert isinstance(estrategia, CalculoResidencial)
    
    def test_criar_comercial(self):
        """Testa criação de estratégia comercial"""
        estrategia = criar_estrategia('comercial')
        assert isinstance(estrategia, CalculoComercial)
    
    def test_criar_industrial(self):
        """Testa criação de estratégia industrial"""
        estrategia = criar_estrategia('industrial')
        assert isinstance(estrategia, CalculoIndustrial)
    
    def test_tipo_invalido(self):
        """Testa erro ao criar estratégia de tipo inválido"""
        with pytest.raises(ValueError):
            criar_estrategia('inexistente')


class TestComparacaoEstrategias:
    """Testes comparativos entre estratégias"""
    
    def test_residencial_vs_comercial(self):
        """Compara cálculo residencial vs comercial"""
        kwh = 200
        
        res = CalculoResidencial()
        com = CalculoComercial()
        
        valor_res, _ = res.calcular(kwh)
        valor_com, _ = com.calcular(kwh)
        
        # Comercial tem tarifa fixa mais alta, então deve ser maior
        assert valor_com > valor_res
    
    def test_progressao_valores_residencial(self):
        """Testa que valores crescem com consumo"""
        estrategia = CalculoResidencial()
        
        valor_100, _ = estrategia.calcular(100)
        valor_200, _ = estrategia.calcular(200)
        valor_400, _ = estrategia.calcular(400)
        
        assert valor_100 < valor_200 < valor_400


if __name__ == "__main__":
    pytest.main([__file__, "-v"])