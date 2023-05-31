from threading import Thread
import time
import pyperclip
import pystray
from pystray import MenuItem as item
from PIL import Image


from Arquivos.Janela import Janela


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

                time.sleep(30)

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
        quantErros = 0
        while True:
            try:
                while True:
                    # Verifica se algo novo foi copiado
                    itemAtual = pyperclip.paste()
                    if ((itemAtual not in self.itensHistory) and (len(itemAtual) > 0)):
                        self.itensHistory.append(itemAtual)
                        if len(self.itensHistory) > 50:
                            self.itensHistory.pop(0)

                    time.sleep(1)
            except Exception as error:
                self.logs.record(
                    msg=f"Erro Exception getCopiedList = {error}", colorize=True)
                quantErros += 1
                if quantErros > 10:
                    self.logs.record(
                        msg=f"Excedeu 10 erros no getCopiedList", colorize=True)
                    break
                continue
