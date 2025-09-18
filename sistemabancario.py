from abc import ABC, abstractmethod
from datetime import datetime, timezone

class Clientes():
    def __init__(self):
        self._clientes = []

    @property
    def clientes(self):
        return self._clientes

    def retornar_cliente(self, cpf):
        for cliente in self._clientes:
            if (cliente.cpf == cpf):
                return cliente
    
    def registrar_cliente(self, cliente):
        self._clientes.append(cliente)

class Contas():
    def __init__(self):
        self._contas = []

    @property
    def contas(self):
        return self._contas
    
    def retornar_conta(self, numero):
        for conta in self._contas:
            if (conta.numero == numero):
                return conta
    
    def registrar_conta(self, conta):
        self._contas.append(conta)



class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def __str__(self):
        return '\n'.join([f'{transacao}' for transacao in self._transacoes])



class Transacao(ABC):

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor    

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if (sucesso):
            conta.historico.adicionar_transacao(self)
    
    def __str__(self):
        return f"{__class__.__name__}: R${self.valor:.2f}, {datetime.strftime(datetime.now(timezone.utc), '%d/%m/%Y %H:%M')}"

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if (sucesso):
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"{__class__.__name__}: R${self.valor:.2f}, {datetime.strftime(datetime.now(timezone.utc), '%d/%m/%Y %H:%M')}"



class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class Conta:
    def __init__(self, numero, agencia, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._historico = Historico()
        self._cliente = cliente

    @property
    def historico(self):
        return self._historico
        
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def saldo(self):
        return self._saldo
    
    def nova_conta(self, cliente, numero):
        pass

    def sacar(self, valor):
            if (valor > 0 and valor <= self._saldo):
                self._saldo -= valor
                print('Saque realizado com sucesso!')
                return True
            else:
                print('Valor inválido ou saldo insuficiente.')
                return False

    def depositar(self, valor):
        if (valor > 0):
            self._saldo += valor
            print('Depósito realizado com sucesso!')
            return True
        else:
            print('Valor inválido')
            return False
        

class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente):
        super().__init__(numero, agencia, cliente)
        self._limite = 500
        self._limite_saques = 3

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self._historico.transacoes if isinstance(transacao, Saque)]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print('Valor limite excedido.')
            
        elif excedeu_saques:
            print('Limite de saque excedido.')
            
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f'Usuário: {self._cliente.nome}\nTipo de conta: {__class__.__name__}\nNúmero da conta: {self._numero}\nAgência: {self._agencia}\nSaldo: R${self._saldo:.2f}'
    
class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf


class InterfaceGrafica():
    def __init__(self):
        self.menu = (
            """=========================================== 
                    DIGITE A OPERAÇÃO QUE DESEJA FAZER: 
    
            [1] Depositar
            [2] Saque
            [3] Extrato
            [4] Cadastrar cliente
            [5] Criar conta corrente
            [6] Imprimir saldo
            [7] Finalizar sessão

               ============================================
            """
        )
    
    def menu_opcoes(self):
        print(self.menu)

    def deposito(self):
        cpf = input('Digite o cpf do cliente: ')
        cliente = lista_clientes.retornar_cliente(cpf)
        

        if not(cliente):
            print('Cliente não encontrado!')
        else:
            numero = int(input('Digite o numero da conta: '))
            conta = lista_contas.retornar_conta(numero)
            if not(conta):
                print('Conta não encontrada')
            else:
                valor = float(input('Digite o valor do depósito: '))
                cliente.realizar_transacao(conta, Deposito(valor))
                

    def saque(self):
        cpf = input('Digite o cpf do cliente: ')
        cliente = lista_clientes.retornar_cliente(cpf)
        
        if not(cliente):
            print('Cliente não encontrado!')
        else:
            numero = int(input('Digite o numero da conta: '))
            conta = lista_contas.retornar_conta(numero)
            if not(conta):
                print('Conta não encontrada')
            else:
                valor = float(input('Digite o valor do saque: '))
                cliente.realizar_transacao(conta, Saque(valor))
                


    def extrato(self):
        cpf = input('Digite o cpf do cliente: ')
        cliente = lista_clientes.retornar_cliente(cpf)
        
        if not(cliente):
            print('Não há cliente com esse cpf.')

        else:
            numero = int(input('Digite o número da conta: '))
            conta = lista_contas.retornar_conta(numero)

            if not(conta):
                print('Conta não encontrada.')

            else:
                print(conta.historico)
        

    def cadastrar_cliente(self):
        cpf = input('Digite o cpf: ')

        if (lista_clientes.retornar_cliente(cpf)):
            print('Este cpf já está cadastrado!')
        else:
            nome = input('Digite seu nome: ')
            endereco = input('Digite seu endereço: Logradouro, número - Cidade-sigla estado: ')
            nascimento = datetime.strptime(input('Digite sua data de nascimento: dd/mm/AAAA: '), '%d/%m/%Y')

            pessoa = PessoaFisica(endereco, cpf, nome, nascimento)
            lista_clientes.registrar_cliente(pessoa)
            print('Cliente cadastrado com sucesso')


    def cadastrar_conta(self):
        cpf = input('Digite o cpf do cliente: ')
        cliente = lista_clientes.retornar_cliente(cpf)

        if not(cliente):
            print('Não existe nenhum cliente com este cpf')

        else:
            numero = len(lista_contas.contas) + 1
            agencia = input('Digite o número de sua agência.(5 dígitos)\n')

            conta_corrente = ContaCorrente(numero, agencia, cliente)
            cliente.adicionar_conta(conta_corrente)
            lista_contas.contas.append(conta_corrente)
            print('Conta cadastrada com sucesso!')
            
    def imprimir_saldo(self):
        cpf = input('Digite o cpf do cliente:')
        cliente = lista_clientes.retornar_cliente(cpf)

        if not(cliente):
            print('Não existe nenhum cliente com este cpf')
        else:
            numero = int(input('Digite o número da conta: '))
            conta = lista_contas.retornar_conta(numero)

            if not(conta):
                print('Conta não encontrada.')
            else:
                print(conta)


lista_clientes = Clientes()
lista_contas = Contas()

while (True):
    ui = InterfaceGrafica()

    ui.menu_opcoes()
    opcao = input('Selecione uma opção:\n')

    if (opcao == '7'):
        break
    elif (opcao == '1'):
        ui.deposito()
    
    elif (opcao == '2'):
        ui.saque()
    
    elif (opcao == '3'):
        ui.extrato()
    
    elif (opcao == '4'):
        ui.cadastrar_cliente()

    elif (opcao == '5'):
        ui.cadastrar_conta()

    elif (opcao == '6'):
        ui.imprimir_saldo()


        
