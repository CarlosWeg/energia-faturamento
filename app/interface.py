"""
Interface Tkinter - Sistema de Faturamento de Energia

Interface gráfica para interação com o sistema de cálculo de contas.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from typing import Optional

# Importações dos padrões
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.conta import Cliente, Consumo, ContaEnergia
from strategies.calculo_tarifa import (
    CalculadoraConta, criar_estrategia
)
from decorators.conta_decorators import (
    ContaBase, BandeiraDecorator, ImpostoDecorator,
    TaxaIluminacaoDecorator
)
from infra.tabela_tarifaria import obter_tabela_tarifaria


class SistemaFaturamentoGUI:
    """Interface gráfica principal do sistema"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistema de Faturamento de Energia Elétrica")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configuração de cores
        self.cor_primaria = "#1e3a8a"
        self.cor_secundaria = "#3b82f6"
        self.cor_destaque = "#22c55e"
        self.cor_fundo = "#f8fafc"
        
        self.root.configure(bg=self.cor_fundo)
        
        # Obtém instância única da tabela tarifária (Singleton)
        self.tabela_tarifaria = obter_tabela_tarifaria()
        
        # Variáveis
        self.conta_atual: Optional[ContaEnergia] = None
        
        # Cria interface
        self._criar_widgets()
        
    def _criar_widgets(self):
        """Cria todos os widgets da interface"""
        
        # Frame principal com scrollbar
        main_container = tk.Frame(self.root, bg=self.cor_fundo)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        titulo_frame = tk.Frame(main_container, bg=self.cor_primaria)
        titulo_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            titulo_frame,
            text="⚡ Sistema de Faturamento de Energia",
            font=("Arial", 18, "bold"),
            bg=self.cor_primaria,
            fg="white",
            pady=10
        ).pack()
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba 1: Cálculo de Conta
        self.aba_calculo = tk.Frame(self.notebook, bg=self.cor_fundo)
        self.notebook.add(self.aba_calculo, text="📊 Calcular Conta")
        self._criar_aba_calculo()
        
        # Aba 2: Configurações
        self.aba_config = tk.Frame(self.notebook, bg=self.cor_fundo)
        self.notebook.add(self.aba_config, text="⚙️ Configurações")
        self._criar_aba_configuracoes()
        
        # Rodapé
        rodape = tk.Frame(self.root, bg=self.cor_primaria, height=40)
        rodape.pack(side=tk.BOTTOM, fill=tk.X)
        
        tk.Label(
            rodape,
            text="Desenvolvido por: Carlos Weege",
            font=("Arial", 10),
            bg=self.cor_primaria,
            fg="white"
        ).pack(pady=10)
    
    def _criar_aba_calculo(self):
        """Cria aba de cálculo de conta"""
        
        # Frame de entrada
        entrada_frame = tk.LabelFrame(
            self.aba_calculo,
            text="Dados do Cliente e Consumo",
            font=("Arial", 11, "bold"),
            bg=self.cor_fundo,
            padx=15,
            pady=15
        )
        entrada_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Grid de inputs
        row = 0
        
        # Nome do Cliente
        tk.Label(
            entrada_frame, text="Nome do Cliente:", bg=self.cor_fundo
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.entry_nome = tk.Entry(entrada_frame, width=40)
        self.entry_nome.grid(row=row, column=1, pady=5, padx=5)
        self.entry_nome.insert(0, "Cliente Exemplo")
        
        row += 1
        
        # Código do Cliente
        tk.Label(
            entrada_frame, text="Código:", bg=self.cor_fundo
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.entry_codigo = tk.Entry(entrada_frame, width=20)
        self.entry_codigo.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        self.entry_codigo.insert(0, "CLI-001")
        
        row += 1
        
        # Tipo de Consumidor (Strategy Pattern)
        tk.Label(
            entrada_frame, text="Tipo de Consumidor:", bg=self.cor_fundo
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.combo_tipo = ttk.Combobox(
            entrada_frame,
            values=['residencial', 'comercial', 'industrial'],
            state='readonly',
            width=18
        )
        self.combo_tipo.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        self.combo_tipo.current(0)
        
        row += 1
        
        # Consumo em kWh
        tk.Label(
            entrada_frame, text="Consumo (kWh):", bg=self.cor_fundo
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.entry_kwh = tk.Entry(entrada_frame, width=20)
        self.entry_kwh.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        self.entry_kwh.insert(0, "250")
        
        row += 1
        
        # Tipo de Bandeira (Decorator Pattern)
        tk.Label(
            entrada_frame, text="Bandeira Tarifária:", bg=self.cor_fundo
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        self.combo_bandeira = ttk.Combobox(
            entrada_frame,
            values=['verde', 'amarela', 'vermelha1', 'vermelha2'],
            state='readonly',
            width=18
        )
        self.combo_bandeira.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        self.combo_bandeira.current(0)
        
        row += 1
        
        # Checkboxes para custos adicionais (Decorator Pattern)
        self.var_impostos = tk.BooleanVar(value=True)
        self.var_taxa_ilum = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            entrada_frame,
            text="Incluir Impostos (ICMS, PIS/COFINS)",
            variable=self.var_impostos,
            bg=self.cor_fundo
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        row += 1
        
        tk.Checkbutton(
            entrada_frame,
            text="Incluir Taxa de Iluminação Pública",
            variable=self.var_taxa_ilum,
            bg=self.cor_fundo
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Botão de calcular
        btn_calcular = tk.Button(
            entrada_frame,
            text="💰 Calcular Conta",
            command=self._calcular_conta,
            bg=self.cor_destaque,
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn_calcular.grid(row=row+1, column=0, columnspan=2, pady=15)
        
        # Frame de resultado
        resultado_frame = tk.LabelFrame(
            self.aba_calculo,
            text="Resultado da Conta",
            font=("Arial", 11, "bold"),
            bg=self.cor_fundo,
            padx=10,
            pady=10
        )
        resultado_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de texto com scroll para resultado
        self.text_resultado = scrolledtext.ScrolledText(
            resultado_frame,
            width=80,
            height=20,
            font=("Courier", 9),
            wrap=tk.WORD
        )
        self.text_resultado.pack(fill=tk.BOTH, expand=True)
    
    def _criar_aba_configuracoes(self):
        """Cria aba de configurações (Singleton Pattern)"""
        
        # Info do Singleton
        info_frame = tk.LabelFrame(
            self.aba_config,
            text="Tabela Tarifária (Singleton)",
            font=("Arial", 11, "bold"),
            bg=self.cor_fundo,
            padx=15,
            pady=15
        )
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Mostra informações da tabela
        mes_ref = self.tabela_tarifaria.get_mes_referencia()
        data_atual = self.tabela_tarifaria.get_data_atualizacao()
        
        tk.Label(
            info_frame,
            text=f"Mês de Referência: {mes_ref}",
            bg=self.cor_fundo,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=2)
        
        tk.Label(
            info_frame,
            text=f"Última Atualização: {data_atual.strftime('%d/%m/%Y %H:%M')}",
            bg=self.cor_fundo,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=2)
        
        tk.Label(
            info_frame,
            text=f"Instância Singleton: {id(self.tabela_tarifaria)}",
            bg=self.cor_fundo,
            font=("Arial", 9),
            fg="gray"
        ).pack(anchor=tk.W, pady=2)
        
        # Tarifas
        tarifas_frame = tk.LabelFrame(
            self.aba_config,
            text="Tarifas Vigentes",
            font=("Arial", 11, "bold"),
            bg=self.cor_fundo,
            padx=15,
            pady=15
        )
        tarifas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cria treeview para tarifas
        columns = ('tipo', 'valor')
        self.tree_tarifas = ttk.Treeview(
            tarifas_frame,
            columns=columns,
            show='headings',
            height=8
        )
        
        self.tree_tarifas.heading('tipo', text='Tipo de Tarifa')
        self.tree_tarifas.heading('valor', text='Valor (R$/kWh)')
        
        self.tree_tarifas.column('tipo', width=300)
        self.tree_tarifas.column('valor', width=150)
        
        self.tree_tarifas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Carrega tarifas
        self._atualizar_tree_tarifas()
        
        # Botão de reset
        tk.Button(
            tarifas_frame,
            text="🔄 Restaurar Tarifas Padrão",
            command=self._restaurar_tarifas,
            bg=self.cor_secundaria,
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=8
        ).pack(pady=10)
    
    def _atualizar_tree_tarifas(self):
        """Atualiza treeview com tarifas do Singleton"""
        # Limpa items existentes
        for item in self.tree_tarifas.get_children():
            self.tree_tarifas.delete(item)
        
        # Adiciona tarifas
        tarifas = self.tabela_tarifaria.get_todas_tarifas()
        for tipo, valor in tarifas.items():
            nome_formatado = tipo.replace('_', ' ').title()
            self.tree_tarifas.insert('', tk.END, values=(nome_formatado, f"R$ {valor:.2f}"))
        
        # Adiciona bandeiras
        bandeiras = self.tabela_tarifaria.get_todas_bandeiras()
        for tipo, valor in bandeiras.items():
            nome_formatado = f"Bandeira {tipo.title()}"
            valor_str = f"R$ {valor:.2f}/100kWh" if valor > 0 else "Sem custo"
            self.tree_tarifas.insert('', tk.END, values=(nome_formatado, valor_str))
    
    def _calcular_conta(self):
        """Calcula conta usando os padrões implementados"""
        try:
            # Valida e obtém dados
            nome = self.entry_nome.get().strip()
            codigo = self.entry_codigo.get().strip()
            tipo_consumidor = self.combo_tipo.get()
            kwh = float(self.entry_kwh.get())
            tipo_bandeira = self.combo_bandeira.get()
            
            if not nome or not codigo:
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return
            
            if kwh <= 0:
                messagebox.showerror("Erro", "Consumo deve ser maior que zero!")
                return
            
            # Cria cliente
            cliente = Cliente(
                codigo=codigo,
                nome=nome,
                tipo_consumidor=tipo_consumidor,
                endereco="Rua Exemplo, 123"
            )
            
            # STRATEGY PATTERN: Cria estratégia baseada no tipo
            estrategia = criar_estrategia(tipo_consumidor)
            calculadora = CalculadoraConta(estrategia)
            
            # Calcula valor base usando Strategy
            valor_base, detalhes_base, desc_estrategia = calculadora.calcular_conta(kwh)
            
            # DECORATOR PATTERN: Aplica decoradores em camadas
            conta_component = ContaBase(valor_base, "Consumo de Energia")
            
            # Adiciona bandeira
            conta_component = BandeiraDecorator(
                conta_component, tipo_bandeira, kwh
            )
            
            # Adiciona impostos se selecionado
            if self.var_impostos.get():
                conta_component = ImpostoDecorator(conta_component, 'pis_cofins')
                conta_component = ImpostoDecorator(conta_component, 'icms')
            
            # Adiciona taxa de iluminação se selecionado
            if self.var_taxa_ilum.get():
                conta_component = TaxaIluminacaoDecorator(conta_component)
            
            # Obtém valor final e detalhamento
            valor_final = conta_component.get_valor()
            detalhes_completos = conta_component.get_detalhamento()
            
            # Cria objeto Consumo
            consumo = Consumo(
                kwh=kwh,
                mes_referencia=self.tabela_tarifaria.get_mes_referencia(),
                data_leitura=datetime.now(),
                leitura_anterior=1000,
                leitura_atual=1000 + kwh
            )
            
            # Cria conta final
            self.conta_atual = ContaEnergia(
                cliente=cliente,
                consumo=consumo,
                valor_total=valor_final,
                detalhes=detalhes_completos
            )
            
            # Exibe resultado
            self._exibir_resultado(desc_estrategia, conta_component.get_descricao())
            
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular: {str(e)}")
    
    def _exibir_resultado(self, estrategia: str, decoradores: str):
        """Exibe resultado no text widget"""
        self.text_resultado.delete(1.0, tk.END)
        
        if not self.conta_atual:
            return
        
        # Cabeçalho com padrões utilizados
        resultado = f"""
{'='*70}
DEMONSTRAÇÃO DOS PADRÕES DE PROJETO
{'='*70}

STRATEGY PATTERN:
  Estratégia utilizada: {estrategia}

DECORATOR PATTERN:
  Composição aplicada: {decoradores}

SINGLETON PATTERN:
  Tabela Tarifária (ID: {id(self.tabela_tarifaria)})
  Mês: {self.tabela_tarifaria.get_mes_referencia()}

{'='*70}
"""
        
        # Adiciona resumo da conta
        resultado += self.conta_atual.get_resumo()
        
        self.text_resultado.insert(1.0, resultado)
        
        messagebox.showinfo(
            "Sucesso",
            f"Conta calculada com sucesso!\n\nValor Total: R$ {self.conta_atual.valor_total:.2f}"
        )
    
    def _restaurar_tarifas(self):
        """Restaura tarifas padrão usando Singleton"""
        resposta = messagebox.askyesno(
            "Confirmar",
            "Deseja restaurar todas as tarifas para os valores padrão?"
        )
        
        if resposta:
            self.tabela_tarifaria.resetar_tarifas_padrao()
            self._atualizar_tree_tarifas()
            messagebox.showinfo("Sucesso", "Tarifas restauradas com sucesso!")


def iniciar_interface():
    """Função para iniciar a interface gráfica"""
    root = tk.Tk()
    app = SistemaFaturamentoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_interface()