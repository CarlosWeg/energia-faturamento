"""
Singleton Pattern - Gerenciador de Tabela Tarifária

Este módulo implementa o padrão Singleton para garantir uma única
instância da tabela tarifária em toda a aplicação.

Pattern: Singleton
Garante que uma classe tenha apenas uma instância e fornece um ponto
global de acesso a ela.
"""

import threading
from typing import Dict, Optional
from datetime import datetime


class TabelaTarifariaManager:
    """
    Singleton - Gerenciador único de tabelas tarifárias
    
    Garante que apenas uma instância da tabela tarifária exista,
    mantendo consistência dos valores em toda a aplicação.
    
    Thread-safe: Usa Lock para garantir segurança em ambientes multithreaded.
    """
    
    # Atributos de classe para o Singleton
    _instance: Optional['TabelaTarifariaManager'] = None
    _lock: threading.Lock = threading.Lock()
    
    def __new__(cls):
        """
        Sobrescreve __new__ para controlar a criação da instância
        
        Este é o ponto chave do padrão Singleton: apenas uma instância
        pode ser criada.
        """
        if cls._instance is None:
            with cls._lock:
                # Double-check locking para thread-safety
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Inicializa a tabela tarifária apenas na primeira vez
        
        Usa flag para evitar reinicialização em chamadas subsequentes.
        """
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._tarifas: Dict[str, float] = self._carregar_tarifas_padrao()
            self._bandeiras: Dict[str, float] = self._carregar_bandeiras_padrao()
            self._mes_referencia = datetime.now().strftime("%m/%Y")
            self._data_atualizacao = datetime.now()
    
    @staticmethod
    def _carregar_tarifas_padrao() -> Dict[str, float]:
        """Carrega tarifas padrão do sistema"""
        return {
            'residencial_faixa1': 0.50,  # 0-100 kWh
            'residencial_faixa2': 0.65,  # 101-300 kWh
            'residencial_faixa3': 0.85,  # >300 kWh
            'comercial_base': 0.75,
            'industrial_base': 0.60,
            'industrial_demanda': 25.00
        }
    
    @staticmethod
    def _carregar_bandeiras_padrao() -> Dict[str, float]:
        """Carrega valores padrão das bandeiras tarifárias"""
        return {
            'verde': 0.00,
            'amarela': 1.50,
            'vermelha1': 4.50,
            'vermelha2': 7.00
        }
    
    @classmethod
    def get_instance(cls) -> 'TabelaTarifariaManager':
        """
        Método estático para obter a instância única
        
        Esta é a forma recomendada de acessar o Singleton.
        """
        if cls._instance is None:
            cls()
        return cls._instance
    
    def get_tarifa(self, tipo: str) -> float:
        """
        Obtém valor da tarifa por tipo
        
        Args:
            tipo: Chave da tarifa (ex: 'residencial_faixa1')
            
        Returns:
            Valor da tarifa em R$/kWh
            
        Raises:
            KeyError: Se o tipo de tarifa não existir
        """
        if tipo not in self._tarifas:
            raise KeyError(f"Tarifa '{tipo}' não encontrada")
        return self._tarifas[tipo]
    
    def get_todas_tarifas(self) -> Dict[str, float]:
        """Retorna cópia de todas as tarifas"""
        return self._tarifas.copy()
    
    def atualizar_tarifa(self, tipo: str, valor: float) -> None:
        """
        Atualiza valor de uma tarifa
        
        Args:
            tipo: Chave da tarifa
            valor: Novo valor em R$/kWh
            
        Raises:
            ValueError: Se valor for negativo
        """
        if valor < 0:
            raise ValueError("Valor da tarifa não pode ser negativo")
        
        with self._lock:
            self._tarifas[tipo] = valor
            self._data_atualizacao = datetime.now()
    
    def get_bandeira(self, tipo: str) -> float:
        """
        Obtém valor da bandeira tarifária
        
        Args:
            tipo: Tipo de bandeira ('verde', 'amarela', etc)
            
        Returns:
            Valor da bandeira por 100 kWh
        """
        if tipo not in self._bandeiras:
            raise KeyError(f"Bandeira '{tipo}' não encontrada")
        return self._bandeiras[tipo]
    
    def get_todas_bandeiras(self) -> Dict[str, float]:
        """Retorna cópia de todas as bandeiras"""
        return self._bandeiras.copy()
    
    def atualizar_bandeira(self, tipo: str, valor: float) -> None:
        """
        Atualiza valor de uma bandeira
        
        Args:
            tipo: Tipo de bandeira
            valor: Novo valor por 100 kWh
        """
        if valor < 0:
            raise ValueError("Valor da bandeira não pode ser negativo")
        
        with self._lock:
            self._bandeiras[tipo] = valor
            self._data_atualizacao = datetime.now()
    
    def get_mes_referencia(self) -> str:
        """Retorna o mês de referência da tabela"""
        return self._mes_referencia
    
    def set_mes_referencia(self, mes: str) -> None:
        """Define o mês de referência da tabela"""
        with self._lock:
            self._mes_referencia = mes
            self._data_atualizacao = datetime.now()
    
    def get_data_atualizacao(self) -> datetime:
        """Retorna data da última atualização"""
        return self._data_atualizacao
    
    def resetar_tarifas_padrao(self) -> None:
        """Reseta todas as tarifas para valores padrão"""
        with self._lock:
            self._tarifas = self._carregar_tarifas_padrao()
            self._bandeiras = self._carregar_bandeiras_padrao()
            self._data_atualizacao = datetime.now()
    
    def exportar_configuracao(self) -> Dict:
        """
        Exporta configuração completa da tabela
        
        Returns:
            Dicionário com toda a configuração
        """
        return {
            'mes_referencia': self._mes_referencia,
            'data_atualizacao': self._data_atualizacao.isoformat(),
            'tarifas': self._tarifas.copy(),
            'bandeiras': self._bandeiras.copy()
        }
    
    def importar_configuracao(self, config: Dict) -> None:
        """
        Importa configuração da tabela
        
        Args:
            config: Dicionário com configuração exportada
        """
        with self._lock:
            if 'mes_referencia' in config:
                self._mes_referencia = config['mes_referencia']
            if 'tarifas' in config:
                self._tarifas = config['tarifas'].copy()
            if 'bandeiras' in config:
                self._bandeiras = config['bandeiras'].copy()
            self._data_atualizacao = datetime.now()
    
    @classmethod
    def reset_instance(cls) -> None:
        """
        Reseta a instância do Singleton
        
        ATENÇÃO: Usar apenas em testes! Este método quebra o padrão
        Singleton e só deve ser usado para limpar estado entre testes.
        """
        with cls._lock:
            cls._instance = None
    
    def __repr__(self) -> str:
        """Representação do objeto"""
        return (
            f"TabelaTarifariaManager("
            f"mes={self._mes_referencia}, "
            f"tarifas={len(self._tarifas)}, "
            f"bandeiras={len(self._bandeiras)})"
        )


# Função auxiliar para acesso rápido
def obter_tabela_tarifaria() -> TabelaTarifariaManager:
    """
    Função auxiliar para obter instância do Singleton
    
    Fornece uma forma mais simples de acessar a tabela tarifária.
    """
    return TabelaTarifariaManager.get_instance()