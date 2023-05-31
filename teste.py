import pyperclip
import time

numbers = [str(i) for i in range(1, 31)]

for number in numbers:
    pyperclip.copy(number)
    print("Número", number, "copiado para a área de transferência.")
    time.sleep(1.1)