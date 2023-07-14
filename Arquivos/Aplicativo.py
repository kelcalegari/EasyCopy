from datetime import datetime
from threading import Thread
import time
import pyperclip
import pystray
from pystray import MenuItem as item
from PIL import Image
from Arquivos.Janela import Janela
import easygui


class Aplicativo:
    itensHistory = []
    LOG_FILE = "Arquivos/Logs/Log.log"

    def __init__(self, logs):
        self.logs = logs
        try:
            lookThread = self.initLookCopy()
            iconTaskThread = self.initIconTask()
            while True:
                if not lookThread.is_alive():
                    raise RuntimeError("Falha no lookThread")
                elif not iconTaskThread.is_alive():
                    return

                time.sleep(15)
        except Exception as erro:
            self.logs.record(msg=erro, colorize=True)

    def initIconTask(self):
        try:
            thread = Thread(
                target=self.iconTask)
            thread.daemon = True
            thread.start()
        except RuntimeError as error:
            self.logs.record(
                msg=f"Erro RuntimeError thread abrirJanela = {error}", colorize=True)
        return thread

    def iconTask(self):
        image = Image.open("Arquivos/icone.ico")
        menu = (
            item('Sair', self.sair),
            item('Abrir Janela', self.abrirJanela, default=True, visible=False),
        )
        icon = pystray.Icon("area_de_transferencia", image,
                            "Área de transferência", menu)
        icon.run()

    def sair(self, icon, item):
        icon.stop()

    def abrirJanela(self, icon, item):
        try:
            thread = Thread(
                target=Janela, args=(self.itensHistory, self.logs,))
            thread.daemon = True
            thread.start()
        except RuntimeError as error:
            self.logs.record(
                msg=f"Erro RuntimeError thread abrirJanela = {error}", colorize=True)

    def initLookCopy(self):
        try:
            thread = Thread(target=self.getCopiedList)
            # Define o thread como daemon para finalizar junto com o programa principal
            thread.daemon = True
            thread.start()
        except RuntimeError as error:
            self.logs.record(
                msg=f"Erro RuntimeError thread initLookCopy = {error}", colorize=True)
        return thread

    def getCopiedList(self):
        itemAnterior = ""
        quantErros = 0
        while True:
            try:
                while True:
                    
                    itemAtual = pyperclip.paste()
                    if (itemAnterior != itemAtual):
                        if ((itemAtual not in self.itensHistory) and (len(itemAtual) > 0)):
                            self.itensHistory.append(itemAtual)
                            itemAnterior = itemAtual
                            if len(self.itensHistory) > 50:
                                self.itensHistory.pop(0)
                        elif (len(itemAtual) > 0):
                            self.itensHistory.remove(itemAtual)
                            self.itensHistory.append(itemAtual)
                            itemAnterior = itemAtual
                        
                    time.sleep(1)

            except Exception as error:

                hora_atual = datetime.now().time()
                print("erro" + str(hora_atual.minute))
                self.logs.record(
                    msg=f"Erro Exception getCopiedList = {error}", colorize=True)
                quantErros += 1
                pyperclip.copy("")
                time.sleep(10)
                if quantErros > 1:
                    diferenca_minutos = (datetime.combine(
                        datetime.min, hora_atual) - datetime.combine(datetime.min, ultimoErro)).total_seconds() / 60
                    if diferenca_minutos > 1:
                        quantErros = 0
                    else:
                        ultimoErro = hora_atual
                else:
                    ultimoErro = hora_atual

                if quantErros > 10:
                    self.logs.record(
                        msg=f"Excedeu 10 erros no getCopiedList", colorize=True)
                    easygui.msgbox(
                        f"Erro EasyCopy parou de funcionar, inicie ele novamente! ")

                    break

                continue
