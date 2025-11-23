"""
Strategy Pattern - Estratégias de Cálculo de Tarifa

Este módulo implementa diferentes estratégias de cálculo baseadas no tipo
de consumidor (residencial, comercial, industrial).

Pattern: Strategy
Permite trocar dinamicamente o algoritmo de cálculo sem modificar o código cliente.
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple


class CalculoTarifaStrategy(ABC):
    """
    Interface Strategy - Define o contrato para cálculo de tarifa
    
    Todas as estratégias concretas devem implementar esta interface.
    """
    
    @abstractmethod
    def calcular(self, kwh: float) -> Tuple[float, Dict[str, float]]:
        """
        Calcula o valor da tarifa baseado no consumo
        
        Args:
            kwh: Consumo em quilowatt-hora
            
        Returns:
            Tupla contendo (valor_total, detalhes_calculo)
        """
        pass
    
    @abstractmethod
    def get_descricao(self) -> str:
        """Retorna descrição da estratégia"""
        pass


class CalculoResidencial(CalculoTarifaStrategy):
    """
    Estratégia Concreta - Cálculo para consumo residencial
    
    Utiliza tarifação progressiva por faixas:
    - Até 100 kWh: R$ 0,50/kWh
    - 101 a 300 kWh: R$ 0,65/kWh
    - Acima de 300 kWh: R$ 0,85/kWh
    """
    
    def __init__(self):
        self.faixas = [
            (100, 0.50, "Faixa 1 (0-100 kWh)"),
            (300, 0.65, "Faixa 2 (101-300 kWh)"),
            (float('inf'), 0.85, "Faixa 3 (>300 kWh)")
        ]
    
    def calcular(self, kwh: float) -> Tuple[float, Dict[str, float]]:
        """Calcula tarifa progressiva por faixas"""
        valor_total = 0.0
        detalhes = {}
        kwh_restante = kwh
        kwh_anterior = 0
        
        for limite, tarifa, descricao in self.faixas:
            if kwh_restante <= 0:
                break
            
            # Calcula quanto consumir nesta faixa
            kwh_faixa = min(kwh_restante, limite - kwh_anterior)
            valor_faixa = kwh_faixa * tarifa
            
            if kwh_faixa > 0:
                detalhes[f"{descricao}"] = valor_faixa
                valor_total += valor_faixa
            
            kwh_restante -= kwh_faixa
            kwh_anterior = limite
        
        return valor_total, detalhes
    
    def get_descricao(self) -> str:
        return "Residencial - Tarifação Progressiva"


class CalculoComercial(CalculoTarifaStrategy):
    """
    Estratégia Concreta - Cálculo para consumo comercial
    
    Tarifa fixa com descontos por volume:
    - Base: R$ 0,75/kWh
    - Desconto de 5% acima de 500 kWh
    - Desconto de 10% acima de 1000 kWh
    """
    
    def __init__(self):
        self.tarifa_base = 0.75
    
    def calcular(self, kwh: float) -> Tuple[float, Dict[str, float]]:
        """Calcula tarifa com desconto progressivo"""
        valor_base = kwh * self.tarifa_base
        detalhes = {"Consumo Base": valor_base}
        
        # Aplica descontos por volume
        desconto = 0.0
        if kwh > 1000:
            desconto = valor_base * 0.10
            detalhes["Desconto (>1000 kWh)"] = -desconto
        elif kwh > 500:
            desconto = valor_base * 0.05
            detalhes["Desconto (>500 kWh)"] = -desconto
        
        valor_total = valor_base - desconto
        
        return valor_total, detalhes
    
    def get_descricao(self) -> str:
        return "Comercial - Tarifa Fixa com Desconto por Volume"


class CalculoIndustrial(CalculoTarifaStrategy):
    """
    Estratégia Concreta - Cálculo para consumo industrial
    
    Tarifa especial com descontos significativos:
    - Base: R$ 0,60/kWh
    - Desconto de 12% acima de 2000 kWh
    - Desconto de 18% acima de 5000 kWh
    - Tarifa de demanda contratada
    """
    
    def __init__(self):
        self.tarifa_base = 0.60
        self.tarifa_demanda = 25.00  # Valor fixo mensal
    
    def calcular(self, kwh: float) -> Tuple[float, Dict[str, float]]:
        """Calcula tarifa industrial com descontos e demanda"""
        valor_consumo = kwh * self.tarifa_base
        detalhes = {
            "Consumo Base": valor_consumo,
            "Tarifa de Demanda": self.tarifa_demanda
        }
        
        # Aplica descontos por volume industrial
        desconto = 0.0
        if kwh > 5000:
            desconto = valor_consumo * 0.18
            detalhes["Desconto Industrial (>5000 kWh)"] = -desconto
        elif kwh > 2000:
            desconto = valor_consumo * 0.12
            detalhes["Desconto Industrial (>2000 kWh)"] = -desconto
        
        valor_total = valor_consumo - desconto + self.tarifa_demanda
        
        return valor_total, detalhes
    
    def get_descricao(self) -> str:
        return "Industrial - Tarifa Especial com Demanda"


class CalculadoraConta:
    """
    Context - Classe que usa a estratégia
    
    Permite trocar a estratégia de cálculo dinamicamente.
    """
    
    def __init__(self, estrategia: CalculoTarifaStrategy):
        self._estrategia = estrategia
    
    def set_estrategia(self, estrategia: CalculoTarifaStrategy) -> None:
        """
        Troca a estratégia de cálculo em tempo de execução
        
        Este é o ponto forte do padrão Strategy: permite mudança
        dinâmica do comportamento.
        """
        self._estrategia = estrategia
    
    def calcular_conta(self, kwh: float) -> Tuple[float, Dict[str, float], str]:
        """
        Calcula a conta usando a estratégia atual
        
        Returns:
            Tupla contendo (valor, detalhes, descricao_estrategia)
        """
        if kwh < 0:
            raise ValueError("Consumo não pode ser negativo")
        
        valor, detalhes = self._estrategia.calcular(kwh)
        descricao = self._estrategia.get_descricao()
        
        return valor, detalhes, descricao


# Factory simples para criar estratégias (facilita os testes)
def criar_estrategia(tipo: str) -> CalculoTarifaStrategy:
    """
    Factory Method simples para criar estratégias
    
    Args:
        tipo: 'residencial', 'comercial' ou 'industrial'
        
    Returns:
        Instância da estratégia apropriada
    """
    estrategias = {
        'residencial': CalculoResidencial,
        'comercial': CalculoComercial,
        'industrial': CalculoIndustrial
    }
    
    if tipo not in estrategias:
        raise ValueError(
            f"Tipo inválido. Use: {', '.join(estrategias.keys())}"
        )
    
    return estrategias[tipo]()