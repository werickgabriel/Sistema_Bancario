saldo = 0.00
limite_saque = 3
extrato = []

menu = (
    """=========================================== 
            DIGITE A OPERAÇÃO QUE DESEJA FAZER: 
    
        [1] Depósito
        [2] Saque
        [3] Extrato
        [4] Finalizar sessão
       =========================================== 
    """
)

def deposito(valor):
    global saldo
    global extrato

    saldo += valor
    extrato.append(f"Depósito de R${valor: .2f}")
    

def saque(valor):
    global saldo
    global extrato

    saldo -= valor
    extrato.append(f"Saque de R${valor: .2f}")
    


while (True):
    print(menu)

    opcao_usuario = int(input())

    if (opcao_usuario == 4):
        print("=============SESSÃO FINALIZADA==============")
        break

    if (opcao_usuario == 1):
        print("Digite o valor que deseja depositar")
        valor = float(input())

        if (valor <= 0):
            print("Valor inválido, operação encerrada.")
        
        else:
            deposito(valor)
            print("Operação concluída")
           

    if (opcao_usuario == 2):
        if (limite_saque > 0): 
            print(f"Digite o valor que deseja sacar. Você tem {limite_saque} saques restantes.")
            valor = float(input())

            if (valor > 500):
               print("Saques maiores que R$500,00 não são permitidos, tente um valor menor.")
            
            elif ( valor <= 0 or valor > saldo):
               print("Valor inválido para saque, tente novamente.")
            
            else:
               saque(valor)
               limite_saque -= 1
               print("Operação concluída")
                    
        else:
            print("Você alcançou seu limite de saque do dia, tente novamente amanhâ.")
        

    if (opcao_usuario == 3):
        print("===============EXTRATO================")
        print("\n".join(extrato) + '\n')
        print(f"Saldo: {saldo: .2f}")
