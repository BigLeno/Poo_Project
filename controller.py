import tkinter as tk
from model import Model
from view import View

class Controller(Model, View):
    def __init__(self) -> None:
        """Construtor da classe Controller"""
        Model.__init__(self)
        View.__init__(self)
        print("Iniciando o módulo Controller")
        self.nome_lojas = []
        self.razao_produtos = []
        self.carrega_bd()
        print("\nAplicativo iniciado com sucesso!")

    def carrega_bd(self) -> None:
        """Método que carrega os itens de acordo com o pedido"""
        self.lista_geral_mercados = self.lista_mercados()
        self.lista_geral_produtos = self.lista_produtos()

    def acessa_dados_mercados(self) -> None:
        """Método que separa o nome da localização do mercado"""
        for mercado in self.lista_geral_mercados:
            self.nome_lojas.append(mercado.nome)

    def acessa_dados_produtos(self) -> None:
        """Método que separa o nome do produto"""
        for produto in self.lista_geral_produtos:
            self.razao_produtos.append((produto.descricao))

    def inicializa_app(self) -> None:
        """Método que inicializa o App"""
        self.carrega_bd()
        self.acessa_dados_mercados()
        self.acessa_dados_produtos()
        self.inicializar(self.nome_lojas, self.razao_produtos, self.lista_geral_mercados)
        self.inicializa_tabela()
        self.root.mainloop()
    
    def inicializa_tabela(self) -> None:
        """Inicia o widget tabela"""
        for item in self.lista_geral_produtos:
            listTest = [item.descricao, item.mercado, item.unit_value]
            self.frame_inferior.adiciona_dado(listTest)

    def filtro_marcadores(self, item_produtos) -> None:
        """Método que filtra os marcadores"""
        for produto in self.lista_geral_produtos:
            if produto.descricao == item_produtos:
                for mercado in self.lista_geral_mercados:
                    if produto.mercado == mercado.nome:
                        self.criar_marcador(mercado.localizacao(), mercado.nome)  

    def filtrar_items(self) -> None:
        """Método que gere as ações do filtro"""
        item_produtos = self.combobox_produtos.get()
        item_lojas = self.combobox_mercados.get()

        if item_produtos != "Selecione um produto":
            self.inicializa_tabela()
            self.frame_inferior.remover_linhas(item_produtos, "Produto")
            if item_lojas == "Selecione uma loja":
                self.mapview.delete_all_marker()
                self.filtro_marcadores(item_produtos)
                self.filtro_combobox(item_produtos) 

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
	Control = Controller()
	Control.inicializa_app()

if __name__ == '__main__':
	main()