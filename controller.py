import tkinter as tk
from model import Model
from view import View

class Controle(Model, View):
    def __init__(self):
        Model.__init__(self)
        View.__init__(self)
        self.nome_lojas = []
        self.razao_produtos = []
        self.carrega_bd()
        
    def carrega_bd(self):
        """Método que carrega os itens de acordo com o pedido"""
        self.lista_geral_mercados = self.lista_mercados()
        self.lista_geral_produtos = self.lista_produtos()

    def acessa_dados_mercados(self):
        """Método que separa o nome da localização do mercado"""
        for mercado in self.lista_geral_mercados:
            self.nome_lojas.append(mercado.nome)

    def acessa_dados_produtos(self):
        """Método que separa o nome do produto"""
        for produto in self.lista_geral_produtos:
            self.razao_produtos.append((produto.descricao))

    def inicializa_app(self):
        self.carrega_bd()
        self.acessa_dados_mercados()
        self.acessa_dados_produtos()
        self.inicializar(self.nome_lojas, self.razao_produtos, self.lista_geral_mercados)
        self.inicializa_tabela()
        self.root.mainloop()
    
    def inicializa_tabela(self):
        """Inicia o widget tabela"""
        for item in self.lista_geral_produtos:
            listTest = [item.descricao, item.mercado, item.unit_value]
            self.frame_inferior.adiciona_dado(listTest)

    def filtrar_items(self):
        """Método que gere as ações do filtro"""
        item_produtos = self.combobox_produtos.get()
        item_lojas = self.combobox_mercados.get()
        if item_produtos != "Selecione um produto":
            self.inicializa_tabela()
            self.frame_inferior.remover_linhas(item_produtos, "Produto")
            if item_lojas == "Selecione uma loja":
                self.mapview.delete_all_marker()
                for produto in self.lista_geral_produtos:
                    if produto.descricao == item_produtos:
                        for teste in self.lista_geral_mercados:
                            if produto.mercado == teste.nome:
                                self.criar_marcador(teste.localizacao(), teste.nome)              
        elif item_lojas != "Selecione uma loja":
            self.mapview.delete_all_marker()
            for mercado in self.lista_geral_mercados:
                if mercado.nome == item_lojas:
                    self.criar_marcador(mercado.localizacao(),mercado.nome)
            self.frame_inferior.remover_linhas(item_lojas, "Mercado")
        
        else:
            self.inicializa_marcadores()
            self.inicializa_tabela()

def main():
	Control = Controle()
        

	Control.inicializa_app()

if __name__ == '__main__':
	main()
