"""
Decorator Pattern - Decoradores para Custos Adicionais

Este módulo implementa decoradores que adicionam custos adicionais
(bandeiras tarifárias, impostos, taxas) sobre o valor base da conta.

Pattern: Decorator
Permite adicionar responsabilidades dinamicamente aos objetos,
mantendo a interface original.
"""

from abc import ABC, abstractmethod
from typing import Dict


class ContaComponent(ABC):
    """
    Component - Interface para componentes de conta
    
    Define a interface comum para objetos que podem ser decorados.
    """
    
    @abstractmethod
    def get_valor(self) -> float:
        """Retorna o valor total da conta"""
        pass
    
    @abstractmethod
    def get_descricao(self) -> str:
        """Retorna descrição dos componentes"""
        pass
    
    @abstractmethod
    def get_detalhamento(self) -> Dict[str, float]:
        """Retorna detalhamento de todos os valores"""
        pass


class ContaBase(ContaComponent):
    """
    Concrete Component - Implementação básica do componente
    
    Representa o valor base da conta sem custos adicionais.
    """
    
    def __init__(self, valor_base: float, descricao_base: str = "Consumo de Energia"):
        if valor_base < 0:
            raise ValueError("Valor base não pode ser negativo")
        self._valor_base = valor_base
        self._descricao_base = descricao_base
    
    def get_valor(self) -> float:
        return self._valor_base
    
    def get_descricao(self) -> str:
        return self._descricao_base
    
    def get_detalhamento(self) -> Dict[str, float]:
        return {self._descricao_base: self._valor_base}


class ContaDecorator(ContaComponent):
    """
    Decorator Base - Classe abstrata para todos os decoradores
    
    Mantém referência ao componente decorado e delega chamadas.
    """
    
    def __init__(self, componente: ContaComponent):
        self._componente = componente
    
    def get_valor(self) -> float:
        """Delega para o componente decorado"""
        return self._componente.get_valor()
    
    def get_descricao(self) -> str:
        """Delega para o componente decorado"""
        return self._componente.get_descricao()
    
    def get_detalhamento(self) -> Dict[str, float]:
        """Delega para o componente decorado"""
        return self._componente.get_detalhamento()


class BandeiraDecorator(ContaDecorator):
    """
    Concrete Decorator - Adiciona custo de bandeira tarifária
    
    Bandeiras representam custos extras de geração de energia:
    - Verde: R$ 0,00 (sem custo adicional)
    - Amarela: R$ 1,50 por 100 kWh
    - Vermelha Patamar 1: R$ 4,50 por 100 kWh
    - Vermelha Patamar 2: R$ 7,00 por 100 kWh
    """
    
    BANDEIRAS = {
        'verde': (0.00, "Bandeira Verde"),
        'amarela': (1.50, "Bandeira Amarela"),
        'vermelha1': (4.50, "Bandeira Vermelha - Patamar 1"),
        'vermelha2': (7.00, "Bandeira Vermelha - Patamar 2")
    }
    
    def __init__(self, componente: ContaComponent, tipo_bandeira: str, kwh: float):
        super().__init__(componente)
        
        if tipo_bandeira not in self.BANDEIRAS:
            raise ValueError(
                f"Bandeira inválida. Use: {', '.join(self.BANDEIRAS.keys())}"
            )
        
        self._tipo_bandeira = tipo_bandeira
        self._kwh = kwh
        self._valor_adicional, self._nome_bandeira = self.BANDEIRAS[tipo_bandeira]
    
    def _calcular_custo_bandeira(self) -> float:
        """Calcula custo proporcional da bandeira"""
        # Custo por 100 kWh, então divide por 100
        return (self._kwh / 100.0) * self._valor_adicional
    
    def get_valor(self) -> float:
        """Adiciona custo da bandeira ao valor base"""
        return self._componente.get_valor() + self._calcular_custo_bandeira()
    
    def get_descricao(self) -> str:
        """Adiciona descrição da bandeira"""
        return f"{self._componente.get_descricao()} + {self._nome_bandeira}"
    
    def get_detalhamento(self) -> Dict[str, float]:
        """Adiciona detalhamento da bandeira"""
        detalhes = self._componente.get_detalhamento()
        custo_bandeira = self._calcular_custo_bandeira()
        if custo_bandeira > 0:
            detalhes[self._nome_bandeira] = custo_bandeira
        return detalhes


class ImpostoDecorator(ContaDecorator):
    """
    Concrete Decorator - Adiciona impostos sobre o valor
    
    Calcula impostos como percentual do valor acumulado até então.
    Comum para ICMS, PIS, COFINS.
    """
    
    IMPOSTOS_DISPONIVEIS = {
        'icms': (18.0, "ICMS (18%)"),
        'pis': (1.65, "PIS (1,65%)"),
        'cofins': (7.6, "COFINS (7,6%)"),
        'pis_cofins': (9.25, "PIS/COFINS (9,25%)")
    }
    
    def __init__(self, componente: ContaComponent, tipo_imposto: str):
        super().__init__(componente)
        
        if tipo_imposto not in self.IMPOSTOS_DISPONIVEIS:
            raise ValueError(
                f"Imposto inválido. Use: {', '.join(self.IMPOSTOS_DISPONIVEIS.keys())}"
            )
        
        self._tipo_imposto = tipo_imposto
        percentual, nome = self.IMPOSTOS_DISPONIVEIS[tipo_imposto]
        self._percentual = percentual / 100.0  # Converte para decimal
        self._nome_imposto = nome
    
    def _calcular_imposto(self) -> float:
        """Calcula imposto sobre o valor acumulado"""
        return self._componente.get_valor() * self._percentual
    
    def get_valor(self) -> float:
        """Adiciona imposto ao valor base"""
        return self._componente.get_valor() + self._calcular_imposto()
    
    def get_descricao(self) -> str:
        """Adiciona descrição do imposto"""
        return f"{self._componente.get_descricao()} + {self._nome_imposto}"
    
    def get_detalhamento(self) -> Dict[str, float]:
        """Adiciona detalhamento do imposto"""
        detalhes = self._componente.get_detalhamento()
        detalhes[self._nome_imposto] = self._calcular_imposto()
        return detalhes


class TaxaIluminacaoDecorator(ContaDecorator):
    """
    Concrete Decorator - Adiciona taxa de iluminação pública
    
    Valor fixo cobrado mensalmente para manutenção da iluminação pública.
    """
    
    def __init__(self, componente: ContaComponent, valor_taxa: float = 15.00):
        super().__init__(componente)
        if valor_taxa < 0:
            raise ValueError("Taxa não pode ser negativa")
        self._valor_taxa = valor_taxa
    
    def get_valor(self) -> float:
        """Adiciona taxa de iluminação"""
        return self._componente.get_valor() + self._valor_taxa
    
    def get_descricao(self) -> str:
        """Adiciona descrição da taxa"""
        return f"{self._componente.get_descricao()} + Taxa de Iluminação"
    
    def get_detalhamento(self) -> Dict[str, float]:
        """Adiciona detalhamento da taxa"""
        detalhes = self._componente.get_detalhamento()
        detalhes["Taxa de Iluminação Pública"] = self._valor_taxa
        return detalhes


class ContribuicaoMunicipalDecorator(ContaDecorator):
    """
    Concrete Decorator - Adiciona contribuição municipal
    
    Percentual variável cobrado pelos municípios.
    """
    
    def __init__(self, componente: ContaComponent, percentual: float = 3.0):
        super().__init__(componente)
        if percentual < 0 or percentual > 100:
            raise ValueError("Percentual deve estar entre 0 e 100")
        self._percentual = percentual / 100.0
    
    def _calcular_contribuicao(self) -> float:
        """Calcula contribuição sobre valor base (sem outros impostos)"""
        # Pega apenas o valor base original, não o acumulado
        return list(self._componente.get_detalhamento().values())[0] * self._percentual
    
    def get_valor(self) -> float:
        """Adiciona contribuição municipal"""
        return self._componente.get_valor() + self._calcular_contribuicao()
    
    def get_descricao(self) -> str:
        """Adiciona descrição da contribuição"""
        return f"{self._componente.get_descricao()} + Contrib. Municipal"
    
    def get_detalhamento(self) -> Dict[str, float]:
        """Adiciona detalhamento da contribuição"""
        detalhes = self._componente.get_detalhamento()
        detalhes[f"Contribuição Municipal ({self._percentual*100:.1f}%)"] = self._calcular_contribuicao()
        return detalhes


# Função auxiliar para criar conta completa com todos os decoradores
def criar_conta_completa(
    valor_base: float,
    kwh: float,
    tipo_bandeira: str = 'verde',
    incluir_impostos: bool = True,
    incluir_taxa_iluminacao: bool = True
) -> ContaComponent:
    """
    Factory para criar conta com decoradores comuns
    
    Demonstra a composição de múltiplos decoradores.
    """
    conta = ContaBase(valor_base)
    
    # Adiciona bandeira
    conta = BandeiraDecorator(conta, tipo_bandeira, kwh)
    
    # Adiciona impostos
    if incluir_impostos:
        conta = ImpostoDecorator(conta, 'pis_cofins')
        conta = ImpostoDecorator(conta, 'icms')
    
    # Adiciona taxa de iluminação
    if incluir_taxa_iluminacao:
        conta = TaxaIluminacaoDecorator(conta)
    
    return conta