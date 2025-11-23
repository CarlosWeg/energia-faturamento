"""
Decorator Pattern - Decoradores para custos adicionais

Este módulo implementa o padrão Decorator para adicionar custos
adicionais (bandeiras, impostos, taxas) de forma flexível.
"""

from .conta_decorators import (
    ContaComponent,
    ContaBase,
    ContaDecorator,
    BandeiraDecorator,
    ImpostoDecorator,
    TaxaIluminacaoDecorator,
    ContribuicaoMunicipalDecorator,
    criar_conta_completa
)

__all__ = [
    'ContaComponent',
    'ContaBase',
    'ContaDecorator',
    'BandeiraDecorator',
    'ImpostoDecorator',
    'TaxaIluminacaoDecorator',
    'ContribuicaoMunicipalDecorator',
    'criar_conta_completa'
]