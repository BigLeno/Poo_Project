from model_v2 import Model

class Controle:

    def __init__(self):
        self.model = Model()

    def lista_lojas(self, lista_lojas):
        lojas = self.model.lista_mercados()
        lista_lojas.extend(lojas)

    def lista_produtos(self, lista_produtos):
        produtos = self.model.lista_produtos()
        lista_produtos.extend(produtos)

    def filtro_produtos(self, produto, lista_dados):

        produtos_encontrados = self.model.encontra_produto(produto)
        
        for produto in produtos_encontrados:
            lista_dados.append([produto.descricao, produto.mercado, produto.unit_value])

    def filtro_lojas(self, mercado):
        mercado_encontrado = self.model.encontra_mercado(mercado)
        coordenadas = mercado_encontrado.localizacao()
        self.view.criar_marcador(coordenadas, mercado)

    def consultar_localizacao(self, mercado):
        mercado_achei = self.model.encontra_mercado(mercado)
        coordenadas = mercado_achei.localizacao()
        x, y = coordenadas
        lista_coordenadas = [x, y]
        return lista_coordenadas


class dados:
    def __init__(self, arg):
        super(dados, self).__init__()

        self.arg = arg
        
