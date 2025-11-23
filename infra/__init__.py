"""
Infraestrutura - Serviços do sistema

Este módulo contém serviços de infraestrutura como o Singleton
da tabela tarifária.
"""

from .tabela_tarifaria import (
    TabelaTarifariaManager,
    obter_tabela_tarifaria
)

__all__ = [
    'TabelaTarifariaManager',
    'obter_tabela_tarifaria'
]