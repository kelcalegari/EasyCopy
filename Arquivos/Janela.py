import math
import pyperclip
import tkinter as tk


class Janela():
    tam_x = 650
    tam_y = 490
    tam_cont = 150
    cor_fundo_janela = '#2b2b2b'  # Cor de fundo escura da janela
    cor_fundo_container = '#1f1f1f'  # Cor de fundo escura dos contêineres
    cor_texto = 'white'  # Cor do texto em branco
    cor_foco = '#252525'
    lastItem = ""
    linhaS = 0

    def __init__(self, itensHistory, logs):
        self.logs = logs
        try:
            self.itensHistory = itensHistory
            self.janela = tk.Tk()
            self.janela.iconbitmap("Arquivos/iconePreto.ico")
            self.janela.geometry(f"{str(self.tam_x)}x{str(self.tam_y)}")
            self.janela.resizable(False, False)
            self.janela.configure(bg=self.cor_fundo_janela)
            self.janela.title("Área de Transfêrencia")
            self.janela.bind("<MouseWheel>", self.scroll_event)
            self.init()
            self.iniciar_loop()
        except Exception as error:
            self.logs.record(msg=f"Erro Janela = {error}", colorize=True)

    def scroll_event(self, event):
        temp = self.linhaS - int(event.delta)
        nMaxLinha = ((temp/120)) < math.ceil(len(self.itensHistory)/4)
        if ((len(self.itensHistory) > 12) and (temp >= 0) and nMaxLinha):
            self.linhaS = temp
            self.reconstruir_linhas()

    def init(self):
        try:
            self.criar_linhas()
        except Exception as error:
            self.logs.record(msg=f"Erro Janela.init = {error}", colorize=True)

    def criar_conteiner(self, x, y, texto):
        def copiar_texto(event):
            def aplicarEfeito():
                def resetar_cores():
                    try:
                        container.configure(bg=self.cor_fundo_container)
                        contDentro.configure(bg=self.cor_fundo_container)
                        label.configure(bg=self.cor_fundo_container)
                    except tk.TclError:
                        pass

                contDentro.configure(bg=self.cor_foco)
                container.configure(bg=self.cor_foco)
                label.configure(bg=self.cor_foco)
                self.janela.after(500, lambda: resetar_cores())

            pyperclip.copy(texto)
            aplicarEfeito()

        container = tk.Frame(self.janela, width=self.tam_cont,
                             height=self.tam_cont, bg=self.cor_fundo_container)
        container.place(x=x, y=y, width=self.tam_cont, height=self.tam_cont)

        contDentro = tk.Frame(container, width=self.tam_cont,
                              height=self.tam_cont, bg=self.cor_fundo_container)
        contDentro.place(x=10, y=10, width=self.tam_cont -
                         20, height=self.tam_cont-20)

        label = tk.Label(
            contDentro, text=texto, fg=self.cor_texto, bg=self.cor_fundo_container, wraplength=self.tam_cont - 20, justify=tk.LEFT, anchor=tk.NW)
        label.pack(expand=True, anchor=tk.NW)

        label.bind("<Button-1>", copiar_texto)
        contDentro.bind("<Button-1>", copiar_texto)
        container.bind("<Button-1>", copiar_texto)

    def criar_linhas(self):
        calcLinha = int(4*(self.linhaS/120))
        nCopias = len(self.itensHistory) - calcLinha
        i = -1 - calcLinha
        if nCopias != 0:
            for y in range(10, self.tam_y - int(self.tam_cont * 0.60), self.tam_cont + 10):
                for x in range(10, self.tam_x - int(self.tam_cont * 0.60), self.tam_cont + 10):
                    self.criar_conteiner(x, y, self.itensHistory[i])
                    nCopias -= 1
                    i -= 1
                    if ((nCopias == 0) or (i == -13 - calcLinha)):
                        break

                if ((nCopias == 0) or (i == -13 - calcLinha)):
                    break

    def atualizarDados(self):
        if (len(self.itensHistory) != 0):
            if self.itensHistory[-1] != self.lastItem:
                self.lastItem = self.itensHistory[-1]
                self.reconstruir_linhas()
                
        self.janela.after(1000, self.atualizarDados)

    def reconstruir_linhas(self):
        try:
            for widget in self.janela.winfo_children():
                widget.destroy()
            self.init()
        except Exception as error:
            self.logs.record(
                msg=f"Erro Janela.reconstruir_linhas = {error}", colorize=True)

    def iniciar_loop(self):
        self.janela.after(1000, self.atualizarDados)
        self.janela.mainloop()
