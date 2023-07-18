import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView


class View:
    def __init__(self):
        print("Iniciando o Módulo View")
        self.root = tk.Tk()
        self.root.title("View em App")
        self.root.geometry("600x480+100+100")
        
    def inicializar(self, lista_lojas, lista_produtos, lista_geral_mercados):
        self.lista_lojas=["Selecione uma loja"]
        self.lista_lojas.extend(lista_lojas)
        self.lista_produtos=["Selecione um produto"]
        self.lista_produtos.extend(lista_produtos)
        self.lista_geral_mercados = lista_geral_mercados
        self.inicializa_view()
        self.inicializa_marcadores()

    def inicializa_view(self):
        # Frame superior com o texto "Nome do App"
        self.frame_superior = tk.Frame(self.root)
        self.label_nome_app = tk.Label(self.frame_superior, text="Nome do App")
        self.label_nome_app.pack()
        self.frame_superior.grid(row=0, column=0)

        # Frame esquerdo com mapa
        self.frame_esquerdo = tk.Frame(self.root)
        self.mapview = TkinterMapView(self.frame_esquerdo, width=800, height=600, corner_radius=0)
        self.mapview.set_position(-5.7936, -35.1989)
        self.mapview.set_zoom(10)
        self.mapview.pack(fill=tk.BOTH, expand=True)
        self.frame_esquerdo.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Frame direito com comboboxes, radiobuttons e botão
        self.frame_direito = tk.Frame(self.root, bg="light grey")
        self.comboboxes_frame = tk.Frame(self.frame_direito)
        self.combobox_label_produtos = tk.Label(self.comboboxes_frame, text="Produtos")
        self.combobox_label_produtos.grid(row=0, column=0, sticky=tk.W)
        self.combobox_produtos = ttk.Combobox(self.comboboxes_frame, values=self.lista_produtos)
        self.combobox_produtos.current(0)
        self.combobox_produtos.grid(row=0, column=1, sticky=tk.W)

        self.combobox_label_mercados = tk.Label(self.comboboxes_frame, text="Mercados")
        self.combobox_label_mercados.grid(row=1, column=0, sticky=tk.W)
        self.combobox_mercados = ttk.Combobox(self.comboboxes_frame,  values=self.lista_lojas)
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
        self.radio_button2.grid(row=1, column=1, sticky=tk.W)
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

        # Frame inferior com Treeview
        self.frame_inferior = Tabela(
            self.root, ["Produto", "Mercado", "Preço"]
        )
        self.frame_inferior.grid(row=2, column=0, columnspan=2, sticky="nsew")

        

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def mudar_tipo_mapa(self):
        tipo_mapa = self.map_type_var.get()

        if tipo_mapa == "Satélite":
            self.mapview.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif tipo_mapa == "Padrão":
            self.mapview.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    def ordenar_menor_preco(self):
        self.frame_inferior.ordena_crescente("Preço")

    def ordenar_maior_preco(self):
        self.frame_inferior.ordena_decrescente("Preço")

    def inicializa_marcadores(self):
        for mercado in self.lista_geral_mercados:
            self.criar_marcador(mercado.localizacao(),mercado.nome)

    def criar_marcador(self, coordenadas, nome):
        lat, lon = coordenadas
        self.mapview.set_marker(lat, lon, text=nome)

    def atualiza_tabela(self, novos_dados):
        for dados in novos_dados:
                self.frame_inferior.adiciona_dado(dados)
    
    def atualiza_marcadores(self, novos_marcadores):
        self.mapview.delete_all_marker()
        for marcador in novos_marcadores:
            mark = marcador
            self.criar_marcador(mark.coordenadas,mark.nome_mercado)
    

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
    
    def remover_linhas(self, string, coluna):
        items = self._tv.get_children()

        for item in items:
            valor = self._tv.set(item, coluna)
            if valor != string:
                self._tv.delete(item)


