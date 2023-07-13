from typing import List, Tuple
import pandas as pd

class Produto:
    """Uma classe que representa cada objeto"""
    def __init__(self, descricao, mercado, unit_value):
        """Objeto que representa um produto"""
        self.descricao = descricao # Descrição do produto
        self.mercado   = mercado    # Nome do mercado onde
        self.unit_value  = unit_value# Valor unitário

    def __repr__(self):
        return f"descrição: {self.descricao}, mercado: {self.mercado}, preço: {self.unit_value}"

class Mercado:
    """Uma classe que representa cada objeto"""
    def __init__(self, mercado, resultado):
        """Objeto que representa um Supermercado"""
        self.resultado = resultado
        self.mercado = mercado
    
    def localizacao(self):
        """Método que pega as coordenadas"""
        return self.resultado['x'].values[0], self.resultado['y'].values[0]
    
    def __repr__(self):
        return f'Mercado: {self.mercado}, Localização: {(self.localizacao())}'
    
class Banco_de_Dados(Exception):
    """Erro personalizado"""
    pass

class Database:
    def __init__(self, database) -> None:
        try:
            self.__data = pd.read_csv(database)
            print(f"Lendo o banco de dados: {database}")
            
        except Banco_de_Dados as erro:
            raise Banco_de_Dados(f"Foi encontrado uma exceção: {erro}")

    @property
    def data(self):
        """Retorna o banco de dados"""
        return self.__data
            



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
        self.db = Database(Model.database).data
        self.lc = Database(Model.location).data
        

    
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
                produto = Produto(row["description"], row["razao"], row["unit_value"])
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
                    produto = Produto(row["description"], row["razao"], row["unit_value"])
                    if produto.mercado not in mercados_exibidos:
                        mercados_exibidos.add(produto.mercado)
                        produtos_encontrados.append(produto)
            
            return produtos_encontrados
            
        except Exception as err:
            raise f"Erro ao encontrar o item: {str(err)}"

    def encontra_mercado(self, mercado: str) -> Tuple[float, float]:
        """
        Método abstrato responsável por procurar um mercado no banco de dados e obter suas coordenadas.

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

    def lista_mercados(self) -> List[str]:
        """
            Método abstrato responsável por listar os mercados no DB.

            @brief:
                Lista os mercados no banco de dados.

            @return:
                Retorna uma lista de mercardos
        """
        try:
            return self.db['razao'].unique().tolist()
        
        except Exception as err:
            raise f"Erro ao listar os items: {str(err)}"
    
    def lista_produtos(self) -> List[str]:
        """
            Método abstrato responsável por listar os Produtos no DB.

            @brief:
                Lista os Produtos no banco de dados.

            @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da busca ('success' ou 'error').
                - 'Produtos': Uma lista de strings contendo os nomes dos Produtos disponíveis no banco de dados da Model.
        """
        try:
            return self.db['description'].unique().tolist()
            
        except Exception as err:
            raise f"Erro ao listar os items: {str(err)}"




obj = Model()

print(obj.remove_item_db(['valor1', 'valor2', 'valor3', 'valor4', 'valor5', 'valor6']))