
import re
from datetime import datetime, timezone


saldo = 0.00
limite_transacao = 10
extrato = []
usuarios = []
contas_correntes = []


menu = (
    """=========================================== 
            DIGITE A OPERAÇÃO QUE DESEJA FAZER: 
    
        [1] Depósito
        [2] Saque
        [3] Extrato
        [4] Cadastrar usuário
        [5] Criar conta corrente
        [6] Finalizar sessão
       =========================================== 
    """
)

def deposito(valor):
    global saldo
    global extrato

    saldo += valor
    extrato.append(f"Depósito de R${valor: .2f}. {datetime.strftime(datetime.now(timezone.utc), '%d/%m/%Y %H:%M')}")
    

def saque(valor):
    global saldo
    global extrato

    saldo -= valor
    extrato.append(f"Saque de R${valor: .2f}")
    
def transacao():
    global limite_transacao

    if (limite_transacao == 0):
        print("Você ultrapassou seu limite de transações")
        return 0

    else:
        limite_transacao -= 1
        return 1    

def extrato():
    print("===============EXTRATO================")
    print("\n".join(extrato) + '\n')
    print(f"Saldo: {saldo: .2f}")


def criar_usuario():
    def formatar_cpf():
        cpf = input('Digite o seu cpf: \n')
        cpf = re.sub(r'\D', '', cpf)

        if (len(cpf) == 11):
            return cpf
        else:
            print('cpf inválido, tente novamente.')
            return formatar_cpf()

    cpf = formatar_cpf()

    if any(user['cpf'] == cpf for user in usuarios):
        print('Já existe um usuário com este cpf')

    else:
        nome = input('Digite seu nome e sobrenome: \n').lower()
        nascimento = input('Digite sua data de nascimento: dd/mm/YYYY \n')
        nascimento = datetime.strptime(nascimento, '%d/%m/%Y')
        endereco = input('Digite seu endereço com: Logradouro, bairro - cidade/sigla do estado: \n')

        usuario = {
            'nome' : nome,
            'nascimento' : nascimento,
            'cpf' : cpf,
            'endereco' : endereco
        }

        usuarios.append(usuario)
        print("Usuário cadastrado com sucesso!")
    
def criar_conta_corrente():
    nome_usuario = input("Digite o nome e sobrenome do usuário pra vincular esta conta:\n").lower()
    if any(user['nome'] == nome_usuario for user in usuarios ):
        print('Conta vinculada com sucesso')
        numero_conta = len(contas_correntes) + 1
        agencia = input('Digite o número de sua agência:\n')
        conta = {
            'nome': nome_usuario,
            'conta': numero_conta,
            'agencia': agencia
        }

        contas_correntes.append(conta)
        print('Conta corrente criada com sucesso!')

    else:
        print('Nao existe um usuario cadastrado com esse nome.')


while (True):
    print(menu)

    opcao_usuario = int(input())

    if (opcao_usuario == 6):
        print("=============SESSÃO FINALIZADA==============")
        break

    if (opcao_usuario == 1):
        if (transacao() > 0):
            print("Digite o valor que deseja depositar")
            valor = float(input())

            if (valor <= 0):
                print("Valor inválido, operação encerrada.")
        
            else:
                deposito(valor)
                print("Operação concluída")
           

    if (opcao_usuario == 2):
        
        if (transacao() > 0):    
            if (valor > 500):
               print("Saques maiores que R$500,00 não são permitidos, tente um valor menor.")
            
            elif ( valor <= 0 or valor > saldo):
               print("Valor inválido para saque, tente novamente.")
            
            else:
               saque(valor)
               limite_transacao -= 1
               print("Operação concluída")        
        

    if (opcao_usuario == 3):
        extrato()

    if (opcao_usuario == 4):
        criar_usuario()    

    if (opcao_usuario == 5):
        criar_conta_corrente()