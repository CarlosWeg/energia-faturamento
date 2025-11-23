"""
Testes para Decorator Pattern

Testa comportamentos-chave do padrão:
1. Composição de múltiplos decoradores
2. Ordem de aplicação dos decoradores
3. Cálculo correto em cascata
4. Interface mantida entre componentes
"""

import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decorators.conta_decorators import (
    ContaBase,
    BandeiraDecorator,
    ImpostoDecorator,
    TaxaIluminacaoDecorator,
    ContribuicaoMunicipalDecorator,
    criar_conta_completa
)


class TestContaBase:
    """Testes do componente base"""
    
    def test_criacao_conta_base(self):
        """Testa criação de conta base"""
        conta = ContaBase(100.00)
        
        assert conta.get_valor() == 100.00
        assert "Consumo de Energia" in conta.get_descricao()
        
        detalhes = conta.get_detalhamento()
        assert len(detalhes) == 1
        assert detalhes["Consumo de Energia"] == 100.00
    
    def test_valor_negativo(self):
        """Testa validação de valor negativo"""
        with pytest.raises(ValueError):
            ContaBase(-100.00)


class TestBandeiraDecorator:
    """Testes do decorador de bandeira"""
    
    def test_bandeira_verde(self):
        """Testa bandeira verde (sem custo adicional)"""
        conta = ContaBase(100.00)
        conta_com_bandeira = BandeiraDecorator(conta, 'verde', 300)
        
        # Bandeira verde não adiciona custo
        assert conta_com_bandeira.get_valor() == 100.00
    
    def test_bandeira_amarela(self):
        """Testa bandeira amarela (R$ 1,50 por 100 kWh)"""
        conta = ContaBase(100.00)
        conta_com_bandeira = BandeiraDecorator(conta, 'amarela', 200)
        
        # 200 kWh / 100 * R$ 1,50 = R$ 3,00
        custo_esperado = 100.00 + (200 / 100 * 1.50)
        assert conta_com_bandeira.get_valor() == pytest.approx(custo_esperado)
    
    def test_bandeira_vermelha1(self):
        """Testa bandeira vermelha patamar 1"""
        conta = ContaBase(100.00)
        conta_com_bandeira = BandeiraDecorator(conta, 'vermelha1', 300)
        
        # 300 kWh / 100 * R$ 4,50 = R$ 13,50
        custo_esperado = 100.00 + (300 / 100 * 4.50)
        assert conta_com_bandeira.get_valor() == pytest.approx(custo_esperado)
    
    def test_bandeira_vermelha2(self):
        """Testa bandeira vermelha patamar 2"""
        conta = ContaBase(100.00)
        conta_com_bandeira = BandeiraDecorator(conta, 'vermelha2', 400)
        
        # 400 kWh / 100 * R$ 7,00 = R$ 28,00
        custo_esperado = 100.00 + (400 / 100 * 7.00)
        assert conta_com_bandeira.get_valor() == pytest.approx(custo_esperado)
    
    def test_bandeira_invalida(self):
        """Testa erro ao usar bandeira inválida"""
        conta = ContaBase(100.00)
        
        with pytest.raises(ValueError):
            BandeiraDecorator(conta, 'azul', 300)
    
    def test_descricao_incluida(self):
        """Testa que descrição da bandeira é incluída"""
        conta = ContaBase(100.00)
        conta_com_bandeira = BandeiraDecorator(conta, 'amarela', 200)
        
        descricao = conta_com_bandeira.get_descricao()
        assert "Bandeira Amarela" in descricao


class TestImpostoDecorator:
    """Testes do decorador de imposto"""
    
    def test_icms(self):
        """Testa aplicação de ICMS (18%)"""
        conta = ContaBase(100.00)
        conta_com_icms = ImpostoDecorator(conta, 'icms')
        
        # 100.00 + 18% = 118.00
        assert conta_com_icms.get_valor() == pytest.approx(118.00)
    
    def test_pis_cofins(self):
        """Testa aplicação de PIS/COFINS (9,25%)"""
        conta = ContaBase(100.00)
        conta_com_pis_cofins = ImpostoDecorator(conta, 'pis_cofins')
        
        # 100.00 + 9.25% = 109.25
        assert conta_com_pis_cofins.get_valor() == pytest.approx(109.25)
    
    def test_imposto_invalido(self):
        """Testa erro ao usar imposto inválido"""
        conta = ContaBase(100.00)
        
        with pytest.raises(ValueError):
            ImpostoDecorator(conta, 'imposto_inexistente')
    
    def test_imposto_em_cascata(self):
        """
        TESTE CRÍTICO: Imposto calculado sobre valor acumulado
        
        Demonstra que decoradores calculam sobre o valor já decorado.
        """
        conta = ContaBase(100.00)
        
        # Adiciona primeiro imposto
        conta = ImpostoDecorator(conta, 'pis_cofins')  # +9.25% = 109.25
        valor_intermediario = conta.get_valor()
        
        # Adiciona segundo imposto (calcula sobre o novo valor)
        conta = ImpostoDecorator(conta, 'icms')  # +18% de 109.25
        valor_final = conta.get_valor()
        
        # Valor calculado manualmente em cascata: 100 * 1.0925 * 1.18 = 128.915
        valor_esperado_cascata = 100.00 * 1.0925 * 1.18
        
        # O teste falhava porque usava > (maior) em vez de == (igual)
        # Agora verificamos se o valor final é igual ao cálculo composto esperado
        assert valor_final == pytest.approx(valor_esperado_cascata)
        
        # Se quisermos provar que é maior que a soma simples (100 + 9.25 + 18 = 127.25):
        valor_soma_simples = 100.00 + (100.00 * 0.0925) + (100.00 * 0.18)
        assert valor_final > valor_soma_simples

class TestTaxaIluminacaoDecorator:
    """Testes do decorador de taxa de iluminação"""
    
    def test_taxa_padrao(self):
        """Testa taxa padrão (R$ 15,00)"""
        conta = ContaBase(100.00)
        conta_com_taxa = TaxaIluminacaoDecorator(conta)
        
        assert conta_com_taxa.get_valor() == pytest.approx(115.00)
    
    def test_taxa_customizada(self):
        """Testa taxa customizada"""
        conta = ContaBase(100.00)
        conta_com_taxa = TaxaIluminacaoDecorator(conta, valor_taxa=20.00)
        
        assert conta_com_taxa.get_valor() == pytest.approx(120.00)
    
    def test_taxa_negativa(self):
        """Testa validação de taxa negativa"""
        conta = ContaBase(100.00)
        
        with pytest.raises(ValueError):
            TaxaIluminacaoDecorator(conta, valor_taxa=-10.00)


class TestComposicaoDecoradores:
    """
    TESTES CRÍTICOS: Composição de múltiplos decoradores
    
    Estes testes demonstram o poder do padrão Decorator:
    empilhamento flexível de comportamentos.
    """
    
    def test_composicao_completa(self):
        """Testa composição de todos os decoradores"""
        valor_base = 100.00
        kwh = 300
        
        # Cria conta base
        conta = ContaBase(valor_base)
        
        # Adiciona bandeira
        conta = BandeiraDecorator(conta, 'amarela', kwh)
        
        # Adiciona impostos
        conta = ImpostoDecorator(conta, 'pis_cofins')
        conta = ImpostoDecorator(conta, 'icms')
        
        # Adiciona taxa
        conta = TaxaIluminacaoDecorator(conta)
        
        # Valor final deve ser maior que o base
        assert conta.get_valor() > valor_base
        
        # Detalhamento deve ter todos os itens
        detalhes = conta.get_detalhamento()
        assert len(detalhes) >= 4  # Base + bandeira + impostos + taxa
    
    def test_ordem_decoradores_importa(self):
        """
        TESTE CRÍTICO: Ordem dos decoradores afeta resultado
        
        Demonstra que a ordem de aplicação dos decoradores importa.
        """
        valor_base = 100.00
        
        # Ordem 1: Imposto antes da taxa
        conta1 = ContaBase(valor_base)
        conta1 = ImpostoDecorator(conta1, 'icms')  # +18%
        conta1 = TaxaIluminacaoDecorator(conta1)  # +15
        valor1 = conta1.get_valor()
        
        # Ordem 2: Taxa antes do imposto
        conta2 = ContaBase(valor_base)
        conta2 = TaxaIluminacaoDecorator(conta2)  # +15
        conta2 = ImpostoDecorator(conta2, 'icms')  # +18% (sobre 115)
        valor2 = conta2.get_valor()
        
        # Valores devem ser diferentes
        assert valor1 != valor2
        
        # Ordem 2 deve resultar em valor maior (ICMS sobre taxa)
        assert valor2 > valor1
    
    def test_empilhamento_multiplo_mesmo_tipo(self):
        """Testa empilhamento de decoradores do mesmo tipo"""
        conta = ContaBase(100.00)
        
        # Adiciona múltiplos impostos
        conta = ImpostoDecorator(conta, 'pis')
        conta = ImpostoDecorator(conta, 'cofins')
        conta = ImpostoDecorator(conta, 'icms')
        
        # Todos devem aparecer no detalhamento
        detalhes = conta.get_detalhamento()
        assert len(detalhes) == 4  # Base + 3 impostos
    
    def test_interface_mantida(self):
        """
        TESTE CRÍTICO: Interface mantida após decoração
        
        Demonstra que decoradores mantêm a interface original.
        """
        conta_simples = ContaBase(100.00)
        conta_decorada = ImpostoDecorator(conta_simples, 'icms')
        
        # Ambas devem ter os mesmos métodos
        assert hasattr(conta_decorada, 'get_valor')
        assert hasattr(conta_decorada, 'get_descricao')
        assert hasattr(conta_decorada, 'get_detalhamento')
        
        # E devem ser chamáveis
        assert callable(conta_decorada.get_valor)
        assert callable(conta_decorada.get_descricao)
        assert callable(conta_decorada.get_detalhamento)


class TestDetalhamento:
    """Testes do detalhamento de valores"""
    
    def test_detalhamento_base(self):
        """Testa detalhamento da conta base"""
        conta = ContaBase(100.00, "Teste Base")
        detalhes = conta.get_detalhamento()
        
        assert "Teste Base" in detalhes
        assert detalhes["Teste Base"] == 100.00
    
    def test_detalhamento_completo(self):
        """Testa detalhamento com múltiplos decoradores"""
        conta = ContaBase(100.00)
        conta = BandeiraDecorator(conta, 'amarela', 200)
        conta = ImpostoDecorator(conta, 'icms')
        conta = TaxaIluminacaoDecorator(conta)
        
        detalhes = conta.get_detalhamento()
        
        # Deve ter base + bandeira + imposto + taxa
        # Correção: Usamos 'any' para buscar substring nas chaves, pois a chave real é 'ICMS (18%)'
        assert "Consumo de Energia" in detalhes
        assert "Bandeira Amarela" in detalhes
        assert any("ICMS" in k for k in detalhes.keys()) 
        assert any("Taxa de Iluminação" in k for k in detalhes.keys())
    
    def test_soma_detalhamento_igual_total(self):
        """Testa que soma do detalhamento = valor total"""
        conta = ContaBase(100.00)
        conta = BandeiraDecorator(conta, 'vermelha1', 300)
        conta = ImpostoDecorator(conta, 'pis_cofins')
        conta = TaxaIluminacaoDecorator(conta)
        
        detalhes = conta.get_detalhamento()
        soma_detalhes = sum(detalhes.values())
        
        assert soma_detalhes == pytest.approx(conta.get_valor())


class TestFactoryContaCompleta:
    """Testes da factory de conta completa"""
    
    def test_criar_conta_completa_padrao(self):
        """Testa criação de conta com configuração padrão"""
        conta = criar_conta_completa(
            valor_base=100.00,
            kwh=300
        )
        
        # Deve ter todos os componentes
        detalhes = conta.get_detalhamento()
        assert len(detalhes) >= 4
        
        # Valor deve ser maior que base
        assert conta.get_valor() > 100.00
    
    def test_criar_conta_sem_impostos(self):
        """Testa criação sem impostos"""
        conta = criar_conta_completa(
            valor_base=100.00,
            kwh=300,
            incluir_impostos=False
        )
        
        detalhes = conta.get_detalhamento()
        
        # Não deve ter ICMS nem PIS/COFINS
        assert not any('ICMS' in k for k in detalhes.keys())
        assert not any('PIS' in k for k in detalhes.keys())
    
    def test_criar_conta_sem_taxa(self):
        """Testa criação sem taxa de iluminação"""
        conta = criar_conta_completa(
            valor_base=100.00,
            kwh=300,
            incluir_taxa_iluminacao=False
        )
        
        detalhes = conta.get_detalhamento()
        
        # Não deve ter taxa de iluminação
        assert not any('Iluminação' in k for k in detalhes.keys())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])