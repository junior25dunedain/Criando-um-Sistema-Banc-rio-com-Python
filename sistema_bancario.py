menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

"""

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUE = 3


while True:
    opcao = input(menu).lower()

    if opcao == 'd':
        print('Depósito')
        depo = float(input('ensira um valor do depósito: '))
        if depo > 0:
            saldo += depo
            extrato += f"Depósito: R$ {depo:.2f}\n"
        else:
            print('Operação falhou! o valor informado é inválido.')
    elif opcao == 's':
        print('Saque')
        saque =  float(input('Informe o valor do saque: '))
        if saque > saldo:
            print('Você não tem saldo suficiente')
        elif saque > limite:
            print('O valor do saque excedeu o limite de 500 reais')
        elif numero_saques >= LIMITE_SAQUE:
            print('Número de saques foi excedido!!')
        elif saque > 0:
            saldo -= saque
            extrato += f"Saque: R$ {saque:.2f}\n"
            numero_saques += 1
        else:
            print('Operação falhou! o valor informado é inválido.')

    elif opcao == 'e':
        print(f'\n************* Extrato ********************')
        print('Não foram realizadas movimentações.' if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
    elif opcao == 'q':
        break
    else:
        print('Operação inválida, por favor selecione novamente !!!')
