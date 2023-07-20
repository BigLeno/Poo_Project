from model import Model
from view import View

class Controller(Model, View):
    """Uma classe que representa o Controller"""
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
        """Método que separa o nome do produto sem repetição por supermercado"""
        produtos_por_nome_mercado = {}
        for produto in self.lista_geral_produtos:
            chave_produto = produto.descricao
            chave_mercado = produto.mercado
            if chave_produto not in produtos_por_nome_mercado:
                produtos_por_nome_mercado[chave_produto] = chave_mercado
                self.razao_produtos.append(chave_produto)
            else:
                mercado_existente = produtos_por_nome_mercado[chave_produto]
                if mercado_existente != chave_mercado:
                    produtos_por_nome_mercado[chave_produto] = chave_mercado
                    self.razao_produtos.append(chave_produto)


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
        dados_adicionados = set()  # Conjunto para armazenar informações únicas de produto, mercado e preço

        for item in self.lista_geral_produtos:
            tupla_info = (item.descricao, item.mercado, item.unit_value)

            # Verifica se a tupla já existe no conjunto de dados adicionados
            if tupla_info not in dados_adicionados:
                listTest = [item.descricao, item.mercado, item.unit_value]
                self.frame_inferior.adiciona_dado(listTest)

                # Adiciona a tupla ao conjunto para evitar duplicatas
                dados_adicionados.add(tupla_info)


    def filtro_marcadores(self, item_produtos) -> None:
        """Método que filtra os marcadores"""
        produtos_por_descricao = {produto.descricao: produto for produto in self.lista_geral_produtos}
        produtos_relevantes = [produtos_por_descricao[item_produtos]]
        marcadores_adicionados = set()
        for produto in produtos_relevantes:
            for mercado in self.lista_geral_mercados:
                if produto.mercado == mercado.nome and mercado.nome not in marcadores_adicionados:
                    self.criar_marcador(mercado.localizacao(), mercado.nome)
                    marcadores_adicionados.add(mercado.nome)

    def filtrar_items(self) -> None:
        """Método que gere as ações do filtro"""

        item_produtos = self.combobox_produtos.get()
        item_lojas = self.combobox_mercados.get()

        if item_produtos != "Selecione um produto":
            self.inicializa_tabela()
            self.frame_inferior.remover_linhas(item_produtos, "Produto")

        self.mapview.delete_all_marker()

        if item_produtos != "Selecione um produto" and item_lojas == "Selecione uma loja":
            self.filtro_marcadores(item_produtos)

        elif item_lojas != "Selecione uma loja":
            for mercado in self.lista_geral_mercados:
                if mercado.nome == item_lojas:
                    self.criar_marcador(mercado.localizacao(), mercado.nome)
            self.frame_inferior.remover_linhas(item_lojas, "Mercado")

        if item_produtos == "Selecione um produto" and item_lojas == "Selecione uma loja":
            self.inicializa_marcadores()
            self.inicializa_tabela()



def main():
	Control = Controller()
	Control.inicializa_app()

if __name__ == '__main__':
	main()
