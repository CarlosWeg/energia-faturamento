"""
Módulo de entidades do domínio - Conta de Energia

Este módulo contém as entidades principais do sistema de faturamento.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class Cliente:
    """Representa um cliente consumidor de energia"""
    
    codigo: str
    nome: str
    tipo_consumidor: str  # 'residencial', 'comercial', 'industrial'
    endereco: str
    
    def __post_init__(self):
        """Valida os dados do cliente"""
        tipos_validos = ['residencial', 'comercial', 'industrial']
        if self.tipo_consumidor not in tipos_validos:
            raise ValueError(
                f"Tipo de consumidor inválido. Use: {', '.join(tipos_validos)}"
            )


@dataclass
class Consumo:
    """Representa o consumo de energia em um período"""
    
    kwh: float
    mes_referencia: str
    data_leitura: datetime
    leitura_anterior: float
    leitura_atual: float
    
    def __post_init__(self):
        """Valida o consumo"""
        if self.kwh < 0:
            raise ValueError("Consumo não pode ser negativo")
        
        if self.leitura_atual < self.leitura_anterior:
            raise ValueError(
                "Leitura atual não pode ser menor que leitura anterior"
            )


class ContaEnergia:
    """
    Representa uma conta de energia completa com todos os detalhes
    
    Esta é a entidade principal do domínio que agrega todas as informações
    de uma conta de energia.
    """
    
    def __init__(
        self,
        cliente: Cliente,
        consumo: Consumo,
        valor_total: float,
        detalhes: Dict[str, float]
    ):
        self.cliente = cliente
        self.consumo = consumo
        self.valor_total = valor_total
        self.detalhes = detalhes
        self.data_emissao = datetime.now()
        self.data_vencimento = self._calcular_vencimento()
    
    def _calcular_vencimento(self) -> datetime:
        """Calcula data de vencimento (10 dias após emissão)"""
        from datetime import timedelta
        return self.data_emissao + timedelta(days=10)
    
    def get_resumo(self) -> str:
        """Retorna um resumo formatado da conta"""
        resumo = f"""
╔══════════════════════════════════════════════════════╗
          CONTA DE ENERGIA ELÉTRICA                   
╠══════════════════════════════════════════════════════╣
 Cliente: {self.cliente.nome:<40}                     
 Código: {self.cliente.codigo:<41}                    
 Tipo: {self.cliente.tipo_consumidor.title():<44}     
 Endereço: {self.cliente.endereco:<40}                
╠══════════════════════════════════════════════════════╣
 Mês Referência: {self.consumo.mes_referencia:<34}    
 Consumo: {self.consumo.kwh:.2f} kWh{' ' * (38 - len(f"{self.consumo.kwh:.2f} kWh"))}                                   
 Leitura Anterior: {self.consumo.leitura_anterior:.0f} kWh{' ' * (28 - len(f"{self.consumo.leitura_anterior:.0f} kWh"))}
 Leitura Atual: {self.consumo.leitura_atual:.0f} kWh{' ' * (31 - len(f"{self.consumo.leitura_atual:.0f} kWh"))}         
╠══════════════════════════════════════════════════════╣
 DETALHAMENTO:                                                                                                          
"""
        
        for descricao, valor in self.detalhes.items():
            linha = f" {descricao:<40} R$ {valor:>8.2f} "
            resumo += linha + "\n"
        
        resumo += f"""╠══════════════════════════════════════════════════════╣
 VALOR TOTAL:{' ' * 30}R$ {self.valor_total:>8.2f} 
╠══════════════════════════════════════════════════════╣
 Emissão: {self.data_emissao.strftime('%d/%m/%Y')}{' ' * 38}
 Vencimento: {self.data_vencimento.strftime('%d/%m/%Y')}{' ' * 35}
╚══════════════════════════════════════════════════════╝
"""
        return resumo
    
    def __str__(self) -> str:
        """Representação em string da conta"""
        return self.get_resumo()