from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Union

class Model(ABC):
    """
    Classe abstrata responsável por gerenciar os acessos aos itens no DataBase (DB).
    Atributos:
        caminhoArquivo (str): Caminho do arquivo CSV contendo os dados do banco de dados.
        db (Dataframe:Object): Inicializa o objeto e carrega o banco de dados a partir do arquivo CSV.
    Métodos:
        __init__(): Construtor da classe Model. Inicializa o objeto e lê o arquivo CSV para carregar o banco de dados.
        encontraProduto(): Método abstrato para procurar produtos no DB.
        encontraMercado(): Método abstrato para procurar mercados no DB.
        encontraMarca(): Método abstrato para procurar marcas no DB.
    """
    caminhoArquivo = "./DataBase/data.csv"
    db = pd.read_csv(caminhoArquivo)
    def __init__(self) -> None:
        """
            Construtor da classe Model.
        """
        pass

    @abstractmethod
    def encontra_produto(self, produto: str) -> Dict[str, Union[str, List[Dict[str, Union[str, float]]]]]:
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

    @abstractmethod
    def lista_mercados(self) -> Dict[str, Union[str, List[str]]]:
        """
            Método abstrato responsável por listar os mercados no DB.

            @brief:
                Lista os mercados no banco de dados.

            @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da busca ('success' ou 'error').
                - 'mercados': Uma lista de strings contendo os nomes dos mercados disponíveis no banco de dados da Model.
        """
        mercados = Model.db['razao'].unique().tolist()

        if len(mercados) > 0:
            return {"status": "success", "mercados": mercados}
        
        return {"status": "error", "message": "Não foram encontrados mercados no banco de dados."}
    
    @abstractmethod
    def lista_produtos(self) -> Dict[str, Union[str, List[str]]]:
        """
            Método abstrato responsável por listar os Produtos no DB.

            @brief:
                Lista os Produtos no banco de dados.

            @return:
            Um dicionário com as seguintes chaves:
                - 'status': Uma string indicando o status da busca ('success' ou 'error').
                - 'Produtos': Uma lista de strings contendo os nomes dos Produtos disponíveis no banco de dados da Model.
        """
        Produtos = Model.db['description'].unique().tolist()

        if len(Produtos) > 0:
            return {"status": "success", "Produtos": Produtos}
        
        return {"status": "error", "message": "Não foram encontrados Produtos no banco de dados."}

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

