"""
Strategy Pattern - Estratégias de cálculo de tarifa

Este módulo implementa o padrão Strategy para permitir diferentes
algoritmos de cálculo de tarifa baseados no tipo de consumidor.
"""

from .calculo_tarifa import (
    CalculoTarifaStrategy,
    CalculoResidencial,
    CalculoComercial,
    CalculoIndustrial,
    CalculadoraConta,
    criar_estrategia
)

__all__ = [
    'CalculoTarifaStrategy',
    'CalculoResidencial',
    'CalculoComercial',
    'CalculoIndustrial',
    'CalculadoraConta',
    'criar_estrategia'
]