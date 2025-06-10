import textwrap

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

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUE = 3
AGENCIA = '0001'
usuarios = []
contas = []

def Saque(*,saldo,valor,extrato,limite,numero,limite_saq):
    if valor > saldo:
            print('Você não tem saldo suficiente')
    elif valor > limite:
            print('O valor do saque excedeu o limite de 500 reais')
    elif numero >= limite_saq:
            print('Número de saques foi excedido!!')
    elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero += 1
            print('\n === Saque realizado com sucesso!! ===')
    else:
            print('Operação falhou! o valor informado é inválido.')
    return saldo, extrato

def depositar(saldo,valor,extrato,/):
    if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print('\n=== Depósito realizado com sucesso ===')
    else:
            print('Operação falhou! o valor informado é inválido.')
    return saldo,extrato


def exibir_extrato(saldo,/,*,extrato):
    print(f'\n************* Extrato ********************')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")


def criar_usuario(usuarios):
      cpf = input('Informe o CPF (somente número): ')
      usuario = filtrar_usuario(cpf,usuarios)
      if usuario:
            print('Já existe esse usuário')
            return 
      nome = input('Informe o nome completo: ')
      data_nasc = input('Informe a data de nascimento (dd-mm-aaaa): ')
      endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ')
      usuarios.append({'nome':nome,'data de nascimento':data_nasc,'CPF':cpf,'endereço': endereco})
      print('=== Usuário criado com sucesso! ===')


def filtrar_usuario(cpf,usuarios):
      aux = [i for i in usuarios if i['CPF'] == cpf]
      return aux[0] if aux else None


def criar_conta(agen,numero_conta,usuarios): 
    cpf = input('Informe o CPF (somente número): ')
    usuario = filtrar_usuario(cpf,usuarios)
    if usuario:
         print('\n === Conta criada com sucesso! ===')
         return {'agencia':agen,'numero_conta':numero_conta,'usuario':usuario}
    print('\n Usuário não encontrado, criação de conta encerrada!')


def listar_contas(contas):
     for conta in contas:
          linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
          """
          print('='*100)
          print(textwrap.dedent(linha))

while True:
    opcao = menu()

    if opcao == 'd':
        print('Depósito')
        depo = float(input('ensira um valor do depósito: '))
        saldo,extrato = depositar(saldo,depo,extrato)
        
    elif opcao == 's':
        print('Saque')
        saque =  float(input('Informe o valor do saque: '))
        saldo, extrato = Saque(saldo=saldo,valor=saque,extrato=extrato,limite=limite,numero=numero_saques,limite_saq=LIMITE_SAQUE)

    elif opcao == 'e':
        exibir_extrato(saldo,extrato=extrato)
    elif opcao == 'nu':
        criar_usuario(usuarios)
    elif opcao == 'nc':
        numero_conta = len(contas) + 1    
        conta =  criar_conta(AGENCIA,numero_conta,usuarios)  
        if conta:
            contas.append(conta)
    elif opcao == 'lc':
         listar_contas(contas)
    elif opcao == 'q':
        break
    else:
        print('Operação inválida, por favor selecione novamente !!!')
