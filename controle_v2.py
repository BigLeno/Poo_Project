import tkinter as tk
from model_v2 import Model
from Testeview_v2 import app_view, Produtos_dados, Mercado_local

class Controle:
    def __init__(self):
        self.model = Model()
        self.root = tk.Tk()
        self.root.title("View em App")
        self.root.geometry("600x480+100+100")
        self.lista_lojas = self.pegar_lista_lojas()
        self.lista_produtos = self.pegar_lista_produtos()
        self.lista_dados = self.pegar_todos_produtos_dados()
        self.lista_localizacoes = self.pegar_lista_lojas_coord()
        self.view = app_view(self.root, self.lista_lojas, self.lista_produtos, self.lista_dados, self.lista_localizacoes)

    def inicializa_app(self):
        self.view.inicializar()
        self.botao_filtro()
        self.root.mainloop()

    def pegar_lista_lojas(self):
        lista_lojas = self.model.lista_mercados()
        return lista_lojas

    def pegar_lista_produtos(self):
        lista_produtos = self.model.lista_produtos()
        return lista_produtos

    def encontrar_produtos_iguais(self, produto):
        produtos_encontrados = self.model.encontra_produto(produto)
        lista_dados = []
        for produto in produtos_encontrados:
            dados_produto = Produtos_dados(produto.descricao, produto.mercado, produto.unit_value)
            lista_dados.append(dados_produto)
        return lista_dados

    def pegar_todos_produtos_dados(self):
        lista_produtos = self.pegar_lista_produtos()
        todos_produtos_dados = []
        for produto in lista_produtos:
            dados = self.encontrar_produtos_iguais(produto)
            for produto_dados in dados:
                produto_lis = Produtos_dados(produto_dados.descricao, produto_dados.mercado, produto_dados.unit_value)
                todos_produtos_dados.append(produto_lis)
        return todos_produtos_dados

    def encontrar_mercado_e_localizacao(self, mercado):
        mercado_encontrado = self.model.encontra_mercado(mercado)
        coordenadas = mercado_encontrado.localizacao()
        return coordenadas

    def pegar_lista_lojas_coord(self):
        lista_lojas = self.pegar_lista_lojas()
        lista_coord = []

        for mercado in lista_lojas:
            mercado_encontrado = Mercado_local(mercado,self.encontrar_mercado_e_localizacao(mercado))
            lista_coord.append(mercado_encontrado)
            
        return lista_coord

    def botao_filtro(self):
         if self.view.filtrar_items() != "normal":
            nova_list_produtos = []
            dados = self.encontrar_produtos_iguais(self.view.filtrar_items())
            for produto_dados in dados:
                produto_new_lis = Produtos_dados(produto_dados.descricao,produto_dados.mercado,produto_dados.unit_value)
                nova_list_produtos.append(produto_new_lis)
            self.view.atualiza_tabela(nova_list_produtos)
def main():
	testcontrole = Controle()
	testcontrole.inicializa_app()

if __name__ == '__main__':
	main()
