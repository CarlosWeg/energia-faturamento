"""
Testes para Singleton Pattern

Testa comportamentos-chave do padrão:
1. Unicidade da instância
2. Thread-safety
3. Persistência de dados entre chamadas
4. Atualização global de valores
"""

import pytest
import threading
import time
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infra.tabela_tarifaria import (
    TabelaTarifariaManager,
    obter_tabela_tarifaria
)


class TestUnicidadeInstancia:
    """
    TESTES CRÍTICOS: Unicidade da instância Singleton
    
    Estes testes demonstram o comportamento fundamental do Singleton:
    apenas uma instância existe.
    """
    
    def setup_method(self):
        """Reseta singleton antes de cada teste"""
        TabelaTarifariaManager.reset_instance()
    
    def test_mesma_instancia_construtor(self):
        """Testa que múltiplas chamadas ao construtor retornam mesma instância"""
        instancia1 = TabelaTarifariaManager()
        instancia2 = TabelaTarifariaManager()
        instancia3 = TabelaTarifariaManager()
        
        # Todas devem ser a mesma instância
        assert instancia1 is instancia2
        assert instancia2 is instancia3
        assert id(instancia1) == id(instancia2) == id(instancia3)
    
    def test_mesma_instancia_get_instance(self):
        """Testa método get_instance()"""
        instancia1 = TabelaTarifariaManager.get_instance()
        instancia2 = TabelaTarifariaManager.get_instance()
        
        assert instancia1 is instancia2
        assert id(instancia1) == id(instancia2)
    
    def test_mesma_instancia_funcao_auxiliar(self):
        """Testa função auxiliar obter_tabela_tarifaria()"""
        instancia1 = obter_tabela_tarifaria()
        instancia2 = obter_tabela_tarifaria()
        instancia3 = TabelaTarifariaManager.get_instance()
        
        # Todas as formas de acesso retornam a mesma instância
        assert instancia1 is instancia2 is instancia3
    
    def test_construtor_e_get_instance_mesma_instancia(self):
        """Testa que construtor e get_instance retornam mesma instância"""
        instancia1 = TabelaTarifariaManager()
        instancia2 = TabelaTarifariaManager.get_instance()
        
        assert instancia1 is instancia2


class TestPersistenciaDados:
    """
    TESTES CRÍTICOS: Persistência de dados
    
    Demonstra que mudanças em uma referência afetam todas as outras,
    pois todas apontam para a mesma instância.
    """
    
    def setup_method(self):
        """Reseta singleton antes de cada teste"""
        TabelaTarifariaManager.reset_instance()
    
    def test_mudanca_visivel_em_todas_referencias(self):
        """
        Testa que mudança em uma referência é visível em todas
        
        Este é o comportamento-chave do Singleton.
        """
        tabela1 = TabelaTarifariaManager()
        tabela2 = TabelaTarifariaManager()
        
        # Modifica através da primeira referência
        tabela1.atualizar_tarifa('residencial_faixa1', 0.99)
        
        # Mudança deve ser visível na segunda referência
        assert tabela2.get_tarifa('residencial_faixa1') == 0.99
        
        # Modifica através da segunda referência
        tabela2.atualizar_tarifa('comercial_base', 0.88)
        
        # Mudança deve ser visível na primeira referência
        assert tabela1.get_tarifa('comercial_base') == 0.88
    
    def test_persistencia_entre_chamadas(self):
        """Testa que dados persistem entre chamadas"""
        # Primeira chamada: define valor
        tabela1 = TabelaTarifariaManager()
        tabela1.atualizar_tarifa('residencial_faixa1', 0.55)
        
        # Segunda chamada: verifica valor
        tabela2 = TabelaTarifariaManager()
        assert tabela2.get_tarifa('residencial_faixa1') == 0.55
        
        # Terceira chamada: também deve ver o valor
        tabela3 = obter_tabela_tarifaria()
        assert tabela3.get_tarifa('residencial_faixa1') == 0.55
    
    def test_mes_referencia_compartilhado(self):
        """Testa que mês de referência é compartilhado"""
        tabela1 = TabelaTarifariaManager()
        tabela2 = TabelaTarifariaManager()
        
        # Define mês na primeira instância
        tabela1.set_mes_referencia("12/2024")
        
        # Deve ser visível na segunda
        assert tabela2.get_mes_referencia() == "12/2024"


class TestThreadSafety:
    """
    TESTES CRÍTICOS: Thread-safety
    
    Demonstra que o Singleton funciona corretamente em ambiente
    multithreaded.
    """
    
    def setup_method(self):
        """Reseta singleton antes de cada teste"""
        TabelaTarifariaManager.reset_instance()
    
    def test_criacao_concorrente_mesma_instancia(self):
        """
        Testa que criação concorrente resulta em mesma instância
        
        Este teste verifica o double-check locking.
        """
        instancias = []
        
        def criar_instancia():
            instancia = TabelaTarifariaManager()
            instancias.append(id(instancia))
        
        # Cria múltiplas threads tentando criar instâncias
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=criar_instancia)
            threads.append(thread)
            thread.start()
        
        # Aguarda todas as threads
        for thread in threads:
            thread.join()
        
        # Todas devem ter o mesmo ID (mesma instância)
        assert len(set(instancias)) == 1
    
    def test_atualizacao_concorrente_thread_safe(self):
        """
        Testa que atualizações concorrentes são thread-safe
        
        Verifica que o Lock protege contra race conditions.
        """
        tabela = TabelaTarifariaManager()
        contador = {'valor': 0}
        
        def atualizar_tarifa(valor):
            tabela.atualizar_tarifa('residencial_faixa1', valor)
            time.sleep(0.001)  # Simula operação demorada
            contador['valor'] += 1
        
        # Cria threads que atualizam concorrentemente
        threads = []
        valores = [0.50 + i * 0.01 for i in range(20)]
        
        for valor in valores:
            thread = threading.Thread(target=atualizar_tarifa, args=(valor,))
            threads.append(thread)
            thread.start()
        
        # Aguarda todas as threads
        for thread in threads:
            thread.join()
        
        # Todas as atualizações devem ter ocorrido
        assert contador['valor'] == 20
        
        # Valor final deve ser um dos valores definidos
        valor_final = tabela.get_tarifa('residencial_faixa1')
        assert valor_final in valores


class TestOperacoesTarifa:
    """Testes das operações de tarifa"""
    
    def setup_method(self):
        """Reseta singleton e obtém instância limpa"""
        TabelaTarifariaManager.reset_instance()
        self.tabela = TabelaTarifariaManager()
    
    def test_get_tarifa_existente(self):
        """Testa obter tarifa existente"""
        valor = self.tabela.get_tarifa('residencial_faixa1')
        assert valor > 0
    
    def test_get_tarifa_inexistente(self):
        """Testa erro ao obter tarifa inexistente"""
        with pytest.raises(KeyError):
            self.tabela.get_tarifa('tarifa_inexistente')
    
    def test_atualizar_tarifa(self):
        """Testa atualização de tarifa"""
        self.tabela.atualizar_tarifa('residencial_faixa1', 0.60)
        assert self.tabela.get_tarifa('residencial_faixa1') == 0.60
    
    def test_atualizar_tarifa_valor_negativo(self):
        """Testa validação de valor negativo"""
        with pytest.raises(ValueError):
            self.tabela.atualizar_tarifa('residencial_faixa1', -0.50)
    
    def test_get_todas_tarifas(self):
        """Testa obter todas as tarifas"""
        tarifas = self.tabela.get_todas_tarifas()
        
        assert isinstance(tarifas, dict)
        assert len(tarifas) > 0
        assert 'residencial_faixa1' in tarifas
    
    def test_get_todas_tarifas_retorna_copia(self):
        """Testa que get_todas_tarifas retorna cópia"""
        tarifas1 = self.tabela.get_todas_tarifas()
        tarifas2 = self.tabela.get_todas_tarifas()
        
        # Devem ser objetos diferentes (cópias)
        assert tarifas1 is not tarifas2
        
        # Mas com mesmo conteúdo
        assert tarifas1 == tarifas2


class TestOperacoesBandeira:
    """Testes das operações de bandeira"""
    
    def setup_method(self):
        """Reseta singleton e obtém instância limpa"""
        TabelaTarifariaManager.reset_instance()
        self.tabela = TabelaTarifariaManager()
    
    def test_get_bandeira_existente(self):
        """Testa obter bandeira existente"""
        valor = self.tabela.get_bandeira('verde')
        assert valor >= 0
    
    def test_get_bandeira_inexistente(self):
        """Testa erro ao obter bandeira inexistente"""
        with pytest.raises(KeyError):
            self.tabela.get_bandeira('bandeira_inexistente')
    
    def test_atualizar_bandeira(self):
        """Testa atualização de bandeira"""
        self.tabela.atualizar_bandeira('amarela', 2.00)
        assert self.tabela.get_bandeira('amarela') == 2.00
    
    def test_atualizar_bandeira_valor_negativo(self):
        """Testa validação de valor negativo"""
        with pytest.raises(ValueError):
            self.tabela.atualizar_bandeira('verde', -1.00)
    
    def test_get_todas_bandeiras(self):
        """Testa obter todas as bandeiras"""
        bandeiras = self.tabela.get_todas_bandeiras()
        
        assert isinstance(bandeiras, dict)
        assert len(bandeiras) > 0
        assert 'verde' in bandeiras
        assert 'amarela' in bandeiras


class TestResetTarifasPadrao:
    """Testes da funcionalidade de reset"""
    
    def setup_method(self):
        """Reseta singleton e obtém instância limpa"""
        TabelaTarifariaManager.reset_instance()
        self.tabela = TabelaTarifariaManager()
    
    def test_reset_restaura_valores_padrao(self):
        """Testa que reset restaura valores padrão"""
        # Modifica valores
        self.tabela.atualizar_tarifa('residencial_faixa1', 0.99)
        self.tabela.atualizar_bandeira('amarela', 9.99)
        
        # Reseta
        self.tabela.resetar_tarifas_padrao()
        
        # Valores devem voltar ao padrão
        assert self.tabela.get_tarifa('residencial_faixa1') == 0.50
        assert self.tabela.get_bandeira('amarela') == 1.50


class TestExportarImportar:
    """Testes de exportação e importação de configuração"""
    
    def setup_method(self):
        """Reseta singleton e obtém instância limpa"""
        TabelaTarifariaManager.reset_instance()
        self.tabela = TabelaTarifariaManager()
    
    def test_exportar_configuracao(self):
        """Testa exportação de configuração"""
        config = self.tabela.exportar_configuracao()
        
        assert 'mes_referencia' in config
        assert 'tarifas' in config
        assert 'bandeiras' in config
        assert 'data_atualizacao' in config
    
    def test_importar_configuracao(self):
        """Testa importação de configuração"""
        # Exporta configuração atual
        config_original = self.tabela.exportar_configuracao()
        
        # Modifica valores
        self.tabela.atualizar_tarifa('residencial_faixa1', 0.99)
        
        # Importa configuração original
        self.tabela.importar_configuracao(config_original)
        
        # Valor deve voltar ao original
        assert self.tabela.get_tarifa('residencial_faixa1') == config_original['tarifas']['residencial_faixa1']
    
    def test_exportar_importar_ciclo_completo(self):
        """Testa ciclo completo de exportação e importação"""
        # Define valores customizados
        self.tabela.atualizar_tarifa('residencial_faixa1', 0.77)
        self.tabela.atualizar_bandeira('verde', 0.50)
        self.tabela.set_mes_referencia("01/2025")
        
        # Exporta
        config = self.tabela.exportar_configuracao()
        
        # Reseta
        self.tabela.resetar_tarifas_padrao()
        
        # Importa
        self.tabela.importar_configuracao(config)
        
        # Valores devem estar de volta
        assert self.tabela.get_tarifa('residencial_faixa1') == 0.77
        assert self.tabela.get_bandeira('verde') == 0.50
        assert self.tabela.get_mes_referencia() == "01/2025"


class TestDataAtualizacao:
    """Testes de data de atualização"""
    
    def setup_method(self):
        """Reseta singleton e obtém instância limpa"""
        TabelaTarifariaManager.reset_instance()
        self.tabela = TabelaTarifariaManager()
    
    def test_data_atualizacao_existe(self):
        """Testa que data de atualização existe"""
        data = self.tabela.get_data_atualizacao()
        assert data is not None
    
    def test_data_atualizacao_muda_em_updates(self):
        """Testa que data muda quando há atualizações"""
        data_inicial = self.tabela.get_data_atualizacao()
        
        time.sleep(0.01)  # Pequeno delay
        self.tabela.atualizar_tarifa('residencial_faixa1', 0.51)
        
        data_final = self.tabela.get_data_atualizacao()
        
        assert data_final > data_inicial


if __name__ == "__main__":
    pytest.main([__file__, "-v"])