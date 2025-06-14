import textwrap
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty



class Cliente:
    def __init__(self,endereco):
        self.contas = []
        self.endereco = endereco
    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)
    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self,nome,data_nasci,cpf,endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nasci
        self.cpf = cpf


class Conta:
    def __init__(self,numero,cliente):
         self._saldo = 0
         self._numero = numero
         self._agencia = '0001'
         self._cliente = cliente
         self._historico = Historico()
    @classmethod
    def nova_conta(cls,cliente,numero):
         return cls(numero,cliente)
    @property
    def saldo(self):
         return self._saldo
    @property
    def numero(self):
         return self._numero
    @property
    def agencia(self):
         return self._agencia
    @property
    def cliente(self):
         return self._cliente
    @property
    def historico(self):
         return self._historico
    
    def sacar(self,valor):
        saldo = self.saldo
        if valor > saldo:
            print('Você não tem saldo suficiente')
        
        elif valor > 0:
            self._saldo -= valor
            print('\n === Saque realizado com sucesso!! ===')
            return True
        else:
            print('Operação falhou! o valor informado é inválido.')
        return False

    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print('\n=== Depósito realizado com sucesso ===')
        else:
            print('Operação falhou! o valor informado é inválido.')
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente,limite=500,limite_saq=3):
         super().__init__(numero, cliente)
         self.limite = limite
         self.limite_saques = limite_saq
    
    def sacar(self,valor):
         numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])
         if valor > self.limite:
              print('O valor do saque excedeu o limite !!!')
         elif numero_saques >= self.limite_saques:
              print('Número de saques foi excedido!!')
         else:
              return super().sacar(valor)
         return False
    
    def __str__(self):
         return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
         """


class Historico:
     def __init__(self):
        self._transacoes = []
     @property
     def transacoes(self):
          return self._transacoes
     def adicionar_transacao(self,transacao):
          self._transacoes.append({'tipo':transacao.__class__.__name__,'valor':transacao.valor,'data':datetime.now().strftime("%d-%m-%Y %H:%M:%s"),})


class Transacao(ABC):
     @property
     @abstractproperty
     def valor(self):
          pass 
     
     @abstractclassmethod
     def registrar(self,conta):
          pass
     

class Saque(Transacao):
     def __init__(self,valor):
          self._valor = valor 
     
     @property
     def valor(self):
          return self._valor
     def registrar(self,conta):
          sucesso_transacao = conta.sacar(self.valor)
          if sucesso_transacao:
               conta.historico.adicionar_transacao(self)
         
class Deposito(Transacao):
     def __init__(self,valor):
          self._valor = valor 
     
     @property
     def valor(self):
          return self._valor
     def registrar(self,conta):
          sucesso_transacao = conta.depositar(self.valor)
          if sucesso_transacao:
               conta.historico.adicionar_transacao(self)





def menu():
    menu = """
    =============== MENU =============
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair

    """
    return input(textwrap.dedent(menu)).lower()


def depositar(clientes):
     cpf = input('informe o cpf do cliente: ')
     cliente = filtrar_usuario(cpf,clientes)
     if not cliente:
          print('cliente não encontrado!!')
          return
     valor = float(input('informe o valor do depósito: '))
     transacao = Deposito(valor)
     conta = recuperar_conta_cliente(cliente)
     if not conta:
          return
     cliente.realizar_transacao(conta,transacao)
          

def exibir_extrato(clientes):
    cpf = input('informe o cpf do cliente: ')
    cliente = filtrar_usuario(cpf,clientes)
    if not cliente:
          print('cliente não encontrado!!')
          return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
          return
    
    print(f'\n************* Extrato ********************')
    transacoes = conta.historico.transacoes
    extrato = ''
    if not transacoes:
         extrato = 'Não foram realizadas movimentações.'
    else:
         for transacao in transacoes:
              extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")


def criar_usuario(usuarios):
      cpf = input('Informe o CPF (somente número): ')
      usuario = filtrar_usuario(cpf,usuarios)
      if usuario:
            print('Já existe esse cliente')
            return 
      nome = input('Informe o nome completo: ')
      data_nasc = input('Informe a data de nascimento (dd-mm-aaaa): ')
      endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ')
      cliente = PessoaFisica(nome=nome,data_nasci=data_nasc,cpf=cpf,endereco=endereco)
      usuarios.append(cliente)
      print('=== Cliente criado com sucesso! ===')


def filtrar_usuario(cpf,usuarios):
      aux = [i for i in usuarios if i.cpf == cpf]
      return aux[0] if aux else None

def sacar(clientes):
     cpf = input('informe o cpf do cliente: ')
     cliente = filtrar_usuario(cpf,clientes)
     if not cliente:
          print('cliente não encontrado!!')
          return
     valor = float(input('informe o valor do saque: '))
     transacao = Saque(valor)
     conta = recuperar_conta_cliente(cliente)
     if not conta:
          return
     cliente.realizar_transacao(conta,transacao)

def recuperar_conta_cliente(cliente):
     if not cliente.contas:
          print('\n@@@ Cliente não possui conta! @@@')
          return
     # FIXME: não permite cliente escolher a conta
     return cliente.contas[0] 

def criar_conta(numero_conta,usuarios,contas): 
    cpf = input('Informe o CPF (somente número): ')
    usuario = filtrar_usuario(cpf,usuarios)
    if not usuario:
        print('cliente não encontrado!!')
        return
    conta = ContaCorrente.nova_conta(cliente=usuario,numero=numero_conta)
    contas.append(conta)
    usuario.contas.append(conta)
    print('\n === Conta criada com sucesso! ===')
    


def listar_contas(contas):
     for conta in contas:
          print('='*100)
          print(textwrap.dedent(str(conta)))


clientes = []
contas = []

while True:
    opcao = menu()

    if opcao == 'd':
        print('Depósito')
        depo = float(input('ensira um valor do depósito: '))
        depositar(clientes)
        
    elif opcao == 's':
        print('Saque')
        saque =  float(input('Informe o valor do saque: '))
        sacar(clientes)

    elif opcao == 'e':
        exibir_extrato(clientes)
    elif opcao == 'nu':
        criar_usuario(clientes)
    elif opcao == 'nc':
        numero_conta = len(contas) + 1    
        criar_conta(numero_conta,clientes,contas)  
        
    elif opcao == 'lc':
         listar_contas(contas)
    elif opcao == 'q':
        break
    else:
        print('Operação inválida, por favor selecione novamente !!!')
