
import os
import urllib.request

from Arquivos.Aplicativo import Aplicativo
from Arquivos.Logger import Logs

class main:
    LOG_FILE = "Arquivos/Logs/Log.log"
    nome_da_pasta = "Arquivos"
    urlIcone = "https://raw.githubusercontent.com/kelcalegari/EasyCopy/master/Arquivos/icone.ico"
    urlIconePreto = "https://raw.githubusercontent.com/kelcalegari/EasyCopy/master/Arquivos/iconePreto.ico"
    nomeIcone = nome_da_pasta + "/icone.ico"
    nomeIconePreto = nome_da_pasta + "/iconePreto.ico"

    def __init__(self):
        logs = Logs(filename=self.LOG_FILE)
        try:
            self.isNewProgram()           
            Aplicativo(logs)
        except Exception as error:
            logs.record(
                msg=f"Erro Main = {error}", colorize=True)
            return

    def isNewProgram(self):
        # Verificar se a pasta já existe
        if not os.path.exists(self.nome_da_pasta):
            # Criar a pasta
            os.makedirs(self.nome_da_pasta)
            os.makedirs(f"{self.nome_da_pasta}/Logs")
            urllib.request.urlretrieve(self.urlIcone, self.nomeIcone)
            urllib.request.urlretrieve(self.urlIconePreto, self.nomeIconePreto)

main()
    
