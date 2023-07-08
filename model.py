from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Union, Tuple

class Model(ABC):
    """
    @brief
        Classe abstrata responsável por gerenciar os acessos aos itens no DataBase (DB).
    @Atributos:
        dataBase (str): Caminho do arquivo CSV contendo os dados do banco de dados.
        location (str): Caminho do arquivo CSV contendo as coordenadas dos supermercados.
        db (Dataframe:Object): Inicializa o objeto e carrega o banco de dados a partir do arquivo CSV.
        lc (Dataframe:Object): Inicializa o objeto e carrega o banco de dados a partir do arquivo CSV.
    @Métodos:
        __init__(): Construtor da classe Model. Inicializa o objeto e lê o arquivo CSV para carregar o banco de dados.
        encontraProduto(): Método abstrato para procurar produtos no DB.
        encontraMercado(): Método abstrato para procurar mercados no DB.
        encontraMarca(): Método abstrato para procurar marcas no DB.
    """
    dataBase = './DataBase/data.csv'
    location = './Database/location.csv'
    db = pd.read_csv(dataBase)
    lc = pd.read_csv(location)
    def __init__(self) -> None:
        """
            Construtor da classe abstrata Model.

            A classe não deve ser instânciada!
        """
        pass
    
    @staticmethod
    @abstractmethod
    def encontra_produto(produto: str) -> Dict[str, Union[str, List[Dict[str, Union[str, float]]]]]:
        """
            Método abstrato responsável por procurar os produtos no DB.

            @brief:
                Recebe um produto como entrada e retorna um dicionário contendo as informações dos produtos encontrados.
            @param produto:
                Uma string contendo o nome do produto a ser procurado no banco de dados.
            @return:
                Um dicionário com as seguintes chaves:
                    - 'status': Uma string indicando o status da busca ('success' ou 'error').
                    - 'produtos': Uma lista de dicionários, onde cada dicionário representa um produto encontrado.
                        Cada dicionário possui as seguintes chaves:
                            - 'descricao': Uma string contendo a descrição do produto.
                            - 'mercado': Uma string contendo o nome do mercado.
                            - 'preco_unidade': Um valor float indicando o preço por unidade do produto.
        """
        try:
            resultado = Model.db[Model.db['description'].str.contains(produto)]
            produtos_encontrados = []
            mercados_exibidos = set()
            if not resultado.empty:
                for index, row in resultado.iterrows():
                    mercado=row['razao']
                    preco_unidade=row['unit_value']
                    descricao=row['description']
                    if mercado not in mercados_exibidos:
                        produtos_encontrados.append({"descricao": descricao, "mercado": mercado, "preco_unidade": preco_unidade})
                        mercados_exibidos.add(mercado)
                return {"status": "success", "produtos": produtos_encontrados}

            return {"status": "error", "message": "Não encontramos o item que você está buscando."}
        
        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao encontrar o item: {str(e)}"}
    
    @staticmethod
    @abstractmethod
    def encontra_marca(marca: str) -> Dict[str, Union[str, List[Dict[str, Union[str, float]]]]]:
        """
        Implementação do método encontra_marca da classe Model.

        Realiza a busca por marcas no banco de dados específico da Model.

        @brief:
            Realiza a busca por marcas no banco de dados da Model.

        @param marca:
            Uma string contendo o nome da marca a ser procurada no banco de dados da Model.

        @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da busca ('success' ou 'error').
                - 'produtos': Uma lista de dicionários, onde cada dicionário representa um produto da marca encontrada.
                    Cada dicionário possui as seguintes chaves:
                        - 'descricao': Uma string contendo a descrição do produto.
                        - 'mercado': Uma string contendo o nome do mercado.
                        - 'preco_unidade': Um valor float indicando o preço por unidade do produto.
        """
        try:
            produtos_encontrados = []
            mercados_exibidos = set()

            for index, row in Model.db.iterrows():
                if marca in row['description']:
                    mercado = row['razao']
                    preco_unidade = row['unit_value']
                    descricao = row['description']

                    if mercado not in mercados_exibidos:
                        produto = {"descricao": descricao, "mercado": mercado, "preco_unidade": preco_unidade}
                        produtos_encontrados.append(produto)
                        mercados_exibidos.add(mercado)
            
            if len(produtos_encontrados) > 0:
                return {"status": "success", "produtos": produtos_encontrados}
            
            return {"status": "error", "message": "Não foram encontrados produtos da marca especificada."}
        
        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao encontrar o item: {str(e)}"}

    @staticmethod
    @abstractmethod
    def encontra_mercado(mercado: str) -> Dict[str, Union[str, Tuple[float, float]]]:
        """
        Método abstrato responsável por procurar um mercado no banco de dados e obter suas coordenadas.

        @param mercado:
            Uma string contendo o nome do mercado a ser pesquisado no banco de dados.

        @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da operação ('success' ou 'error').
                - 'coordenadas': Uma tupla contendo as coordenadas do mercado encontrado (x, y).
        """
        try:
            resultado = Model.lc[Model.lc['name'] == mercado]

            if not resultado.empty:
                x = resultado['x'].values[0]
                y = resultado['y'].values[0]
                return {"status": "success", "coordenadas": (x, y)}
            
            return {"status": "error", "message": "O mercado não foi encontrado."}
        
        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao encontrar o item: {str(e)}"}

    @staticmethod    
    @abstractmethod
    def adiciona_item_db(item: List[str]) -> Dict[str, Union[str, bool]]:
        """
        Método responsável por adicionar um item ao DataFrame.

        @param item:
            Uma lista contendo os valores do item a ser adicionado.
            Exemplo:
                item -> ['valor1', 'valor2', 'valor3', 'valor4', 'valor5', 'valor6']

        @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da operação ('success' ou 'error').
                - 'mensagem': Uma string contendo a mensagem de retorno.
        """
        try:
            Model.db.loc[len(Model.db)] = item
            Model.db.to_csv(Model.dataBase, index=False)
            return {"status": "success", "mensagem": "Item adicionado com sucesso."}
        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao adicionar o item: {str(e)}"}

    @staticmethod
    @abstractmethod
    def remove_item_db(item: List[str]) -> Dict[str, Union[str, bool]]:
        """
        Método responsável por remover um item do DataFrame.

        @param item:
            Uma lista contendo os valores do item a ser removido.
            Exemplo:
                item -> ['valor1', 'valor2', 'valor3', 'valor4', 'valor5', 'valor6']

        @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da operação ('success' ou 'error').
                - 'mensagem': Uma string contendo a mensagem de retorno.
        """
        try:
            linhas_remover = Model.db[Model.db.apply(lambda row: row.tolist() == item, axis=1)]
            Model.db.drop(linhas_remover.index, inplace=True)
            Model.db.to_csv(Model.dataBase, index=False)
            return {"status": "success", "mensagem": "Item removido com sucesso."}
        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao remover o item: {str(e)}"}

    @staticmethod
    @abstractmethod
    def adiciona_item_lc(item: List[str]) -> Dict[str, Union[str, bool]]:
        """
        Método responsável por adicionar um item ao DataFrame.

        @param item:
            Uma lista contendo os valores do item a ser adicionado.
            Exemplo:
                item -> ['valor1', 'valor2', 'valor3', 'valor4']

        @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da operação ('success' ou 'error').
                - 'mensagem': Uma string contendo a mensagem de retorno.
        """
        try:
            Model.lc.loc[len(Model.lc)] = item
            Model.lc.to_csv(Model.location, index=False)
            return {"status": "success", "mensagem": "Item adicionado com sucesso."}
        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao adicionar o item: {str(e)}"}

    @staticmethod
    @abstractmethod
    def remove_item_lc(item: List[str]) -> Dict[str, Union[str, bool]]:
        """
        Método responsável por remover um item do DataFrame.

        @param item:
            Uma lista contendo os valores do item a ser removido.
            Exemplo:
                item -> ['valor1', 'valor2', 'valor3', 'valor4']

        @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da operação ('success' ou 'error').
                - 'mensagem': Uma string contendo a mensagem de retorno.
        """
        try:
            linhas_remover = Model.lc[Model.lc.apply(lambda row: row.tolist() == item, axis=1)]
            Model.lc.drop(linhas_remover.index, inplace=True)
            Model.lc.to_csv(Model.location, index=False)
            return {"status": "success", "mensagem": "Item removido com sucesso."}
        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao remover o item: {str(e)}"}

    @staticmethod
    @abstractmethod
    def lista_mercados() -> Dict[str, Union[str, List[str]]]:
        """
            Método abstrato responsável por listar os mercados no DB.

            @brief:
                Lista os mercados no banco de dados.

            @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da busca ('success' ou 'error').
                - 'mercados': Uma lista de strings contendo os nomes dos mercados disponíveis no banco de dados da Model.
        """
        try:
            mercados = Model.db['razao'].unique().tolist()

            if len(mercados) > 0:
                return {"status": "success", "mercados": mercados}
            
            return {"status": "error", "message": "Não foram encontrados mercados no banco de dados."}
        
        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao listar os items: {str(e)}"}
    
    @staticmethod
    @abstractmethod
    def lista_produtos() -> Dict[str, Union[str, List[str]]]:
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
            Produtos = Model.db['description'].unique().tolist()

            if len(Produtos) > 0:
                return {"status": "success", "Produtos": Produtos}
            
            return {"status": "error", "message": "Não foram encontrados Produtos no banco de dados."}

        except Exception as e:
            return {"status": "error", "mensagem": f"Erro ao listar os items: {str(e)}"}




