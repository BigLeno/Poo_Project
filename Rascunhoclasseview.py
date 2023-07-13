import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
from typing import List, Tuple
import pandas as pd

class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("Nome do App")
        self.lista_mercados=["Selecione uma loja"]
        self.lista_produtos=["Selecione um produto"]
        self.inicializa_gui()

    def inicializa_gui(self):
        self.frame_superior()
        self.frame_esquerdo()
        self.frame_direito()
        self.frame_inferior()

    def frame_superior(self):
        self.frame_superior = tk.Frame(self.root)
        self.label_nome_app = tk.Label(self.frame_superior, text="Nome do App")
        self.label_nome_app.pack()
        self.frame_superior.grid(row=0, column=0)

    def frame_esquerdo(self):
        self.frame_esquerdo = tk.Frame(self.root)
        self.mapview = TkinterMapView(self.frame_esquerdo, width=800, height=600, corner_radius=0)
        self.mapview.set_position(-5.7936, -35.1989)
        self.mapview.set_zoom(10)
        self.mapview.pack(fill=tk.BOTH, expand=True)
        self.frame_esquerdo.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def frame_direito(self):
        self.frame_direito = tk.Frame(self.root, bg="light grey")
        self.comboboxes_frame = tk.Frame(self.frame_direito)
        self.combobox_label_produtos = tk.Label(self.comboboxes_frame, text="Produtos")
        self.combobox_label_produtos.grid(row=0, column=0, sticky=tk.W)
        self.combobox_produtos = ttk.Combobox(self.comboboxes_frame, values=self.lista_produtos)
        self.combobox_produtos.current(0)
        self.combobox_produtos.grid(row=0, column=1, sticky=tk.W)

        self.combobox_label_mercados = tk.Label(self.comboboxes_frame, text="Mercados")
        self.combobox_label_mercados.grid(row=1, column=0, sticky=tk.W)
        self.combobox_mercados = ttk.Combobox(self.comboboxes_frame, values=self.lista_lojas)
        self.combobox_mercados.current(0)
        self.combobox_mercados.grid(row=1, column=1, sticky=tk.W)

        self.comboboxes_frame.grid(row=0, column=0, sticky="ew")
        
        self.radio_var = tk.StringVar()
        self.radio_var.set("Menor preço")
        self.radio_frame = tk.Frame(self.frame_direito, bg="light grey")
        self.radio_label = tk.Label(
            self.radio_frame, bg="light grey", text="Ordenar por:"
        )
        self.radio_label.grid(row=0, column=0, sticky=tk.W)
        self.radio_button1 = tk.Radiobutton(
            self.radio_frame,
            bg="light grey",
            text="Menor preço",
            variable=self.radio_var,
            value="Menor preço",
            command=self.ordenar_menor_preco,
        )
        self.radio_button1.grid(row=0, column=1, sticky=tk.W)
        self.radio_button2 = tk.Radiobutton(
            self.radio_frame,
            bg="light grey",
            text="Maior preço",
            variable=self.radio_var,
            value="Maior preço",
            command=self.ordenar_maior_preco,
        )
        
        self.radio_frame.grid(row=1, column=0, sticky="w")

        self.map_type_var = tk.StringVar()
        self.map_type_var.set("Padrão")
        self.map_type_frame = tk.Frame(self.frame_direito, bg="light grey")
        self.map_type_label = tk.Label(
            self.map_type_frame, bg="light grey", text="Tipo de Mapa:"
        )
        self.map_type_label.grid(row=0, column=0, sticky=tk.W)
        self.map_type_button1 = tk.Radiobutton(
            self.map_type_frame,
            bg="light grey",
            text="Padrão",
            variable=self.map_type_var,
            value="Padrão",
            command=self.mudar_tipo_mapa,
        )
        self.map_type_button1.grid(row=0, column=1, sticky=tk.W)
        self.map_type_button2 = tk.Radiobutton(
            self.map_type_frame,
            bg="light grey",
            text="Satélite",
            variable=self.map_type_var,
            value="Satélite",
            command=self.mudar_tipo_mapa,
        )
        self.map_type_button2.grid(row=1, column=1, sticky=tk.W)
        self.map_type_frame.grid(row=2, column=0, sticky="w")

        self.filtrar_button = tk.Button(
            self.frame_direito,
            bg="light grey",
            text="Filtrar",
            command=self.filtrar_items,
        )
        self.filtrar_button.grid(row=3, column=0)

        self.frame_direito.grid(row=1, column=1, sticky="e")

    def frame_inferior(self):
        self.frame_inferior = Tabela(
            self.root, ["Produto", "Mercado", "Preço"]
        )
        self.frame_inferior.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)


    def mudar_tipo_mapa(self):
        tipo_mapa = self.map_type_var.get()

        if tipo_mapa == "Satélite":
            self.mapview.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif tipo_mapa == "Padrão":
            self.mapview.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    def filtrar_items(self):
        self.controle.filtrar_items(self)

    def ordenar_menor_preco(self):
        self.frame_inferior.ordena_crescente("Preço")

    def ordenar_maior_preco(self):
        self.frame_inferior.ordena_decrescente("Preço")


class Tabela(tk.Frame):
    def __init__(self, pai, tit_cols):
        tk.Frame.__init__(self, pai)
        self._nomes_cols = tit_cols
        self._inicializa_gui(pai)

    def _inicializa_gui(self, pai):
        self._tv = ttk.Treeview(
            self, columns=self._nomes_cols, show="headings"
        )
        self._sb_y = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self._tv.yview
        )
        self._tv.configure(yscroll=self._sb_y.set)
        self._sb_x = ttk.Scrollbar(
            self, orient=tk.HORIZONTAL, command=self._tv.xview
        )
        self._tv.configure(xscroll=self._sb_x.set)

        for tit in self._nomes_cols:
            self._tv.heading(tit, text=tit)
            self._tv.column(tit, width=90, minwidth=100)

        self._tv.grid(row=0, column=0, sticky="nsew")
        self._sb_y.grid(row=0, column=1, sticky="ns")
        self._sb_x.grid(row=1, column=0, columnspan=1, sticky="we")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def adiciona_dado(self, strings_cols):
        if len(strings_cols) != len(self._nomes_cols):
            raise Exception(
                f'Lista deve conter {len(self._nomes_cols)} strings (lista passada contém {len(strings_cols)})'
            )

        self._tv.insert("", tk.END, values=strings_cols)

    def remove_dados(self, pos):
        items = self._tv.get_children()
        if pos < 0 or pos >= len(items):
            raise Exception(f"Posição inválida: {pos}")

        item = items[pos]
        self._tv.delete(item)
    def ordena_crescente(self, coluna):
        items = self._tv.get_children()
        valores = []

        for item in items:
            valor = self._tv.set(item, coluna)
            valores.append((valor, item))

        valores.sort(key=lambda x: x[0])

        for idx, (_, item) in enumerate(valores):
            self._tv.move(item, "", idx)

    def ordena_decrescente(self, coluna):
        items = self._tv.get_children()
        valores = []

        for item in items:
            valor = self._tv.set(item, coluna)
            valores.append((valor, item))

        valores.sort(key=lambda x: x[0], reverse=True)

        for idx, (_, item) in enumerate(valores):
            self._tv.move(item, "", idx)
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
class Model:
    """
    @brief
        Classe responsável por gerenciar os acessos aos itens no DataBase (DB).
    
    """

    def __init__(self, database='./DataBase/data.csv', location='./Database/location.csv') -> None:
        """
            Construtor da classe Model.
        """
        self.database = database
        self.location = location
        self.db = pd.read_csv(self.database)
        self.lc = pd.read_csv(self.location)

    
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

        except Exception as e:
            raise f"Erro ao encontrar o item: {str(e)}"
    
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
            
        except Exception as e:
            raise f"Erro ao encontrar o item: {str(e)}"

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
        
        except Exception as e:
            raise f"Erro ao encontrar o item: {str(e)}"

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
            self.db.to_csv(self.database, index=False)

        except Exception as e:
            raise f"Erro ao adicionar o item: {str(e)}"

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
            self.db.to_csv(self.database, index=False)
        
        except Exception as e:
            return f"Erro ao remover o item: {str(e)}"

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
            self.lc.to_csv(self.location, index=False)

        except Exception as e:
            raise f"Erro ao adicionar o item: {str(e)}"

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
            self.lc.to_csv(self.location, index=False)

        except Exception as e:
            raise f"Erro ao remover o item: {str(e)}"

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
        
        except Exception as e:
            raise f"Erro ao listar os items: {str(e)}"
    
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
            
        except Exception as e:
            raise f"Erro ao listar os items: {str(e)}"
class Controle:
    def __init__(self):
        self.model = Model()
    
    def iniciar(self):
        root = tk.Tk()
        root.title("View em App")
        root.geometry("1200x800+10+10")
        app = AppView(root, self.model)
        self.salvar_mercados(app)
        self.salvar_produtos(app)
        self.atualizar_tabela(app)
        root.mainloop()
    
    def salvar_mercados(self, app):
        mercados = self.model.lista_mercados()
        app.lista_mercados.extend(mercados)
    
    def salvar_produtos(self, app):
        produtos = self.model.lista_produtos()
        app.lista_produtos.extend(produtos)
    def atualizar_tabela(self, app):
        produtos = self.model.encontra_produto("")
        for produto in produtos:
            app.frame_inferior.adiciona_dado([produto.descricao, produto.mercado, produto.unit_value])
    def filtrar_items(self, app):
        item_produtos = app.combobox_produtos.get()
        item_mercados = app.combobox_mercados.get()

        if item_produtos == "Selecione um produto" and item_mercados == "Selecione uma loja":
            # Mostrar todos os produtos e mercados
            self.atualizar_tabela(app)
        elif item_produtos == "Selecione um produto":
            # Filtrar por mercado selecionado
            produtos = self.model.encontra_mercado(item_mercados).resultado
            app.frame_inferior.limpar_tabela()
            for index, row in produtos.iterrows():
                app.frame_inferior.adiciona_dado([row["description"], row["razao"], row["unit_value"]])
        elif item_mercados == "Selecione uma loja":
            # Filtrar por produto selecionado
            produtos = self.model.encontra_produto(item_produtos)
            app.frame_inferior.limpar_tabela()
            for produto in produtos:
                app.frame_inferior.adiciona_dado([produto.descricao, produto.mercado, produto.unit_value])
        else:
            # Filtrar por produto e mercado selecionados
            produtos = self.model.encontra_produto(item_produtos)
            app.frame_inferior.limpar_tabela()
            for produto in produtos:
                if produto.mercado == item_mercados:
                    app.frame_inferior.adiciona_dado([produto.descricao, produto.mercado, produto.unit_value])

APP_controle=Controle()
