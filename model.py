from typing import List, Tuple
import pandas as pd

class Produto:
    """Uma classe que representa cada objeto"""
    def __init__(self, descricao, mercado, unit_value, index=None) -> None:
        """Objeto que representa um produto"""
        self.descricao = descricao # Descrição do produto
        self.mercado   = mercado    # Nome do mercado onde
        self.unit_value  = unit_value# Valor unitário
        self.index = index
    def __repr__(self) -> str:
        """Método que retorna uma string do que é o objeto"""
        return f"descrição: {self.descricao}, mercado: {self.mercado}, preço: {self.unit_value}"

class Mercado:
    """Uma classe que representa cada objeto"""
    def __init__(self, nome, local) -> None:
        """Objeto que representa um Supermercado"""
        self.local = local
        self.nome = nome
    def localizacao(self) -> Tuple(float, float):
        """Método que pega as coordenadas"""
        if not self.local.empty:
            return self.local['x'].values[0], self.local['y'].values[0]
        else:
            raise ValueError("O DataFrame self.local está vazio, não é possível obter a localização.")
    def __repr__(self) -> str:
        """Método que retorna uma string do que é o objeto"""
        return f'Mercado: {self.nome}, Localização: {(self.localizacao())}'
    
class BD(Exception):
    """Erro personalizado"""

class Database:
    """Classe responsável por abrir os DB's"""
    def __init__(self, database) -> None:
        """Objeto que representa um Database"""
        self.database = database
        try:
            self.__data = pd.read_csv(self.database)
            print(f"Lendo o banco de dados: {self.database}")
        except BD as erro:
            print(f"Foi encontrado uma exceção: {erro}")

    @property
    def data(self) -> pd:
        """Retorna o banco de dados"""
        return self.__data
    
    def __repr__(self) -> str:
        """Método que retorna uma string do que é o objeto"""
        return f'Banco de Dados, no caminho {self.database}'
    
class Model:
    """
    @brief
        Classe responsável por gerenciar os acessos aos itens no DataBase (DB).
    
    """
    database = './DataBase/data.csv'
    location='./Database/location.csv'

    def __init__(self) -> None:
        """
            Construtor da classe Model.
        """
        print("\n")
        self.db = Database(Model.database).data
        self.lc = Database(Model.location).data
        print("\nIniciando o módulo Model")
        
    
    def encontra_produto(self, produto: str) -> List[Produto]:
        """
            Método abstrato responsável por procurar os produtos no DB.

            @brief:
                Recebe um produto como entrada e retorna um dicionário contendo as informações dos produtos encontrados.
            @param produto:
                Uma string contendo o nome do produto a ser procurado no banco de dados.
            @return:
                Uma lista de objetos 
        """
        try:
            resultado = self.db[self.db['description'].str.contains(produto)]
            produtos_encontrados = []
            mercados_exibidos = set()
            for index, row in resultado.iterrows():
                produto = Produto(row["description"], row["razao"], row["unit_value"], index=index)
                if produto.mercado not in mercados_exibidos:
                    mercados_exibidos.add(produto.mercado)
                    produtos_encontrados.append(produto)
            return produtos_encontrados
        except Exception as err:
            raise f"Erro ao encontrar o item: {str(err)}"
    
    def encontra_marca(self, marca: str) -> List[Produto]:
        """
        Implementação do método encontra_marca da classe Model.

        Realiza a busca por marcas no banco de dados específico da Model.

        @brief:
            Realiza a busca por marcas no banco de dados da Model.

        @param marca:
            Uma string contendo o nome da marca a ser procurada no banco de dados da Model.

        @return:
           Uma lista de objetos
        """
        try:
            produtos_encontrados = []
            mercados_exibidos = set()
            for index, row in self.db.iterrows():
                if marca in row['description']:
                    produto = Produto(row["description"], row["razao"], row["unit_value"], index)
                    if produto.mercado not in mercados_exibidos:
                        mercados_exibidos.add(produto.mercado)
                        produtos_encontrados.append(produto)
            return produtos_encontrados
        except Exception as err:
            raise f"Erro ao encontrar o item: {str(err)}"

    def encontra_mercado(self, mercado: str) -> Mercado:
        """
        Método responsável por pesquisar o mercado no db.

        @param mercado:
            Uma string contendo o nome do mercado a ser pesquisado no banco de dados.

        @return:
           Um objeto que representa um mercado
        """
        try:
            return Mercado(mercado, self.lc[self.lc['name'] == mercado])
        except Exception as err:
            raise f"Erro ao encontrar o item: {str(err)}"

    def adiciona_item_db(self, item: List[str]) -> None:
        """
        Método responsável por adicionar um item ao DataFrame.

        @param item:
            Uma lista contendo os valores do item a ser adicionado.
            Exemplo:
                item -> ['valor1', 'valor2', 'valor3', 'valor4', 'valor5', 'valor6']

        """
        try:
            self.db.loc[len(self.db)] = item
            self.db.to_csv(Model.database, index=False)
        except Exception as err:
            raise f"Erro ao adicionar o item: {str(err)}"

    def remove_item_db(self, item: List[str]) -> None:
        """
        Método responsável por remover um item do DataFrame.

        @param item:
            Uma lista contendo os valores do item a ser removido.
            Exemplo:
                item -> ['valor1', 'valor2', 'valor3', 'valor4', 'valor5', 'valor6']
        """
        try:
            linhas_remover = self.db[self.db.apply(lambda row: row.tolist() == item, axis=1)]
            self.db.drop(linhas_remover.index, inplace=True)
            self.db.to_csv(Model.database, index=False)
        except Exception as err:
            raise f"Erro ao remover o item: {str(err)}"

    def adiciona_item_lc(self, item: List[str]) -> None:
        """
        Método responsável por adicionar um item ao DataFrame.

        @param item:
            Uma lista contendo os valores do item a ser adicionado.
            Exemplo:
                item -> ['valor1', 'valor2', 'valor3', 'valor4']
        """
        try:
            self.lc.loc[len(self.lc)] = item
            self.lc.to_csv(Model.location, index=False)
        except Exception as err:
            raise f"Erro ao adicionar o item: {str(err)}"

    def remove_item_lc(self, item: List[str]) -> None:
        """
        Método responsável por remover um item do DataFrame.

        @param item:
            Uma lista contendo os valores do item a ser removido.
            Exemplo:
                item -> ['valor1', 'valor2', 'valor3', 'valor4']

        """
        try:
            linhas_remover = self.lc[self.lc.apply(lambda row: row.tolist() == item, axis=1)]
            self.lc.drop(linhas_remover.index, inplace=True)
            self.lc.to_csv(Model.location, index=False)

        except Exception as err:
            raise f"Erro ao remover o item: {str(err)}"

    def lista_mercados(self) -> List[Mercado]:
        """
            Método abstrato responsável por listar os mercados no DB.

            @brief:
                Lista os mercados no banco de dados.

            @return:
                Retorna uma lista de mercardos
        """
        mercados = []
        try:
            for mercado in self.lc['name'].unique().tolist():
                mercados.append(self.encontra_mercado(mercado))
            
            return mercados

        except Exception as err:
            raise f"Erro ao listar os items: {str(err)}"

    
    def lista_produtos(self) -> List[Produto]:
        """
        Método abstrato responsável por listar os Produtos no DB.

        @brief:
            Lista os Produtos no banco de dados.

        @return:
            Lista de objetos Produto.
        """
        produtos = []
        try:
            for index, row in self.db.iterrows():
                produto = Produto(row["description"], row["razao"], row["unit_value"], index=index)
                produtos.append(produto)
            
            return produtos
        
        except Exception as err:
            raise f"Erro ao listar os items: {str(err)}"





