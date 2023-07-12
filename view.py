import tkinter as tk
from tkinter import ttk

class Tabela(tk.Frame):
    """
    Classe que representa uma tabela.

    @brief Classe responsável por exibir uma tabela com colunas e dados.
    """

    def __init__(self, pai, tit_cols):
        """
        Construtor da classe Tabela.

        @brief Inicializa uma nova instância da classe Tabela.
        @param pai: O widget pai onde a tabela será exibida.
        @param tit_cols: Uma lista contendo os títulos das colunas da tabela.
        """
        tk.Frame.__init__(self, pai)
        self._nomes_cols = tit_cols
        self._inicializa_gui(pai)

    def _inicializa_gui(self, pai):
        """
        Inicializa a interface gráfica da tabela.

        @brief Inicializa a interface gráfica da tabela.
        @param pai: O widget pai onde a tabela será exibida.
        """
        self._tv = ttk.Treeview(self, columns=self._nomes_cols, show='headings')
        self._sb_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._tv.yview)
        self._tv.configure(yscroll=self._sb_y.set)
        self._sb_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._tv.xview)
        self._tv.configure(xscroll=self._sb_x.set)

        for tit in self._nomes_cols:
            self._tv.heading(tit, text=tit)
            self._tv.column(tit, width=90, minwidth=100)

        self._tv.grid(row=0, column=0, sticky='nsew')
        self._sb_y.grid(row=0, column=1, sticky='ns')
        self._sb_x.grid(row=1, column=0, columnspan=1, sticky='we')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def adiciona_dado(self, strings_cols):
        """
        Adiciona um dado à tabela.

        @brief Adiciona um novo dado à tabela.
        @param strings_cols: Uma lista contendo os valores das colunas para o novo dado.
        @throws Exception: Se o número de valores passados não corresponder ao número de colunas.
        """
        if len(strings_cols) != len(self._nomes_cols):
            raise Exception(f'Lista deve conter {len(self._nomes_cols)} strings (lista passada contém {len(strings_cols)})')

        self._tv.insert('', tk.END, values=strings_cols)



class View:
    """
    Classe responsável pelo View do projeto de gerenciamento.
    """

    root = tk.Tk()
    combobox_produtos = ''
    combobox_mercados = ''
    combobox_marcas = ''
    radio_var = tk.StringVar()

    def __init__(self) -> None:
        """
            A classe não deve ser instânciada.
        """

    @staticmethod
    def inicializa_gui() -> None:
        """
        Inicializa a interface gráfica.

        @brief Inicializa a interface gráfica do aplicativo.
        """
        View.root.title('View em App')
        View.root.geometry('600x480+100+100')

    @staticmethod
    def frame_superior() -> None:
        """
        Cria o frame superior da interface gráfica.

        @brief Cria o frame superior da interface gráfica.
        """
        frame_superior = tk.Frame(View.root)
        label_nome_app = tk.Label(frame_superior, text="Nome do App")
        label_nome_app.pack()
        frame_superior.grid(row=0, column=0)

    @staticmethod
    def frame_esquerdo() -> None:
        """
        Cria o frame esquerdo da interface gráfica.

        @brief Cria o frame esquerdo da interface gráfica.
        """
        frame_esquerdo = tk.Frame(View.root, bg="green")
        frame_esquerdo.grid(row=1, column=0, columnspan=2, sticky="nsew")

    @staticmethod
    def frame_direito() -> None:
        """
        Cria o frame direito da interface gráfica.

        @brief Cria o frame direito da interface gráfica.
        """
        frame_direito = tk.Frame(View.root, bg='light grey')
        comboboxes_frame = tk.Frame(frame_direito)
        combobox_label_produtos = tk.Label(comboboxes_frame, text="Produtos")
        combobox_label_produtos.grid(row=0, column=0, sticky=tk.W)
        View.combobox_produtos = ttk.Combobox(comboboxes_frame, values=["Selecione um produto", "item 2", "item 3"])
        View.combobox_produtos.current(0)
        View.combobox_produtos.grid(row=0, column=1, sticky=tk.W)

        combobox_label_mercados = tk.Label(comboboxes_frame, text="Mercados")
        combobox_label_mercados.grid(row=1, column=0, sticky=tk.W)
        View.combobox_mercados = ttk.Combobox(comboboxes_frame, values=["Selecione uma loja", "item 2", "item 3"])
        View.combobox_mercados.current(0)
        View.combobox_mercados.grid(row=1, column=1, sticky=tk.W)

        combobox_label_marcas = tk.Label(comboboxes_frame, text="Marcas")
        combobox_label_marcas.grid(row=2, column=0, sticky=tk.W)
        View.combobox_marcas = ttk.Combobox(comboboxes_frame, values=["Selecione uma marca", "item 2", "item 3"])
        View.combobox_marcas.current(0)
        View.combobox_marcas.grid(row=2, column=1, sticky=tk.W)

        comboboxes_frame.grid(row=0, column=0, sticky="ew")
        View.radio_var.set("Menor preço")
        radio_frame = tk.Frame(frame_direito, bg="light grey")
        radio_label = tk.Label(radio_frame, bg="light grey", text="Ordenar por:")
        radio_label.grid(row=0, column=0, sticky=tk.W)
        radio_button1 = tk.Radiobutton(radio_frame,bg="light grey",text="Menor preço",variable=View.radio_var,value="Menor preço")
        radio_button1.grid(row=0, column=1, sticky=tk.W)
        radio_button2 = tk.Radiobutton(radio_frame,bg="light grey",text="Maior preço",variable=View.radio_var,value="Maior preço")
        radio_button2.grid(row=1, column=1, sticky=tk.W)
        radio_button3 = tk.Radiobutton(radio_frame,bg="light grey",text="Menor peso",variable=View.radio_var,value="Menor peso")
        radio_button3.grid(row=2, column=1, sticky=tk.W)
        radio_button4 = tk.Radiobutton(radio_frame,bg="light grey",text="Maior peso",variable=View.radio_var,value="Maior peso")
        radio_button4.grid(row=3, column=1, sticky=tk.W)
        radio_button5 = tk.Radiobutton(radio_frame,bg="light grey",text="Custo benefício",variable=View.radio_var,value="Custo benefício")
        radio_button5.grid(row=4, column=1, sticky=tk.W)
        radio_frame.grid(row=1, column=0, sticky="w")

        filtrar_button = tk.Button(frame_direito,bg="light grey",text="Filtrar",command=View.filtrar_items)
        filtrar_button.grid(row=2, column=0)

        frame_direito.grid(row=1, column=1, sticky="e")

    @staticmethod
    def filtrar_items() -> None:
        """
        Filtra os itens com base nas seleções do usuário.

        @brief Filtra os itens com base nas seleções do usuário nos comboboxes e radiobuttons.
        """
        item_produtos = View.combobox_produtos.get()
        item_mercados = View.combobox_mercados.get()
        item_marcas = View.combobox_marcas.get()
        ordenacao = View.radio_var.get()

        print("Item selecionado no combobox de Produtos:", item_produtos)
        print("Item selecionado no combobox de Mercados:", item_mercados)
        print("Item selecionado no combobox de Marcas:", item_marcas)
        print("Opção selecionada no radiobutton:", ordenacao)

    @staticmethod
    def frame_inferior() -> None:
        """
        Cria o frame inferior da interface gráfica.

        @brief Cria o frame inferior da interface gráfica que contém uma tabela.
        """
        frame_inferior = Tabela(View.root, ["Produto", "Marca", "Mercado", "Preço", "Peso"])
        frame_inferior.grid(row=2, column=0, columnspan=2, sticky="nsew")

        View.root.grid_rowconfigure(1, weight=1)
        View.root.grid_columnconfigure(0, weight=1)
        View.root.grid_columnconfigure(1, weight=1)

    @staticmethod
    def loop() -> None:
        """
        Inicia o loopprincipal do tkinter.

        @brief Inicia o loop principal do tkinter para exibir a interface gráfica.
        """
        View.root.mainloop()

    @staticmethod
    def main() -> None:
        """
        Função principal para executar o aplicativo.

        @brief Função principal para executar o aplicativo de gerenciamento.
        """
        print("Iniciando o Viewer")
        View.inicializa_gui()
        View.frame_superior()
        View.frame_esquerdo()
        View.frame_direito()
        View.frame_inferior()
        View.loop()


View.main()