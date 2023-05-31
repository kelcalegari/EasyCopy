
import os
import urllib.request

from Arquivos.Aplicativo import Aplicativo
from Arquivos.Logger import Logs

class main:
    LOG_FILE = "Arquivos/Logs/Log.log"
    nome_da_pasta = "Arquivos"
    urlIcone = "https://raw.githubusercontent.com/kelcalegari/AreaTransferencia/edc5918e4212a06724f49d47dc0703b7bea96b98/Arquivos/icone.ico?token=GHSAT0AAAAAACAYFV5TQNP7SWXGZ4H5UQ26ZDSLEEA"
    urlIconePreto = "https://raw.githubusercontent.com/kelcalegari/AreaTransferencia/edc5918e4212a06724f49d47dc0703b7bea96b98/Arquivos/iconePreto.ico?token=GHSAT0AAAAAACAYFV5TECYSK67C4BGRR7GSZDSLEYA"
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
    
