# Sistema Bancário em Python

Este projeto implementa um sistema bancário simples em Python, permitindo operações de **depósito, saque, consulta de extrato e saída**.

## 📌 Funcionalidades

- **Depósito:** O usuário pode inserir um valor válido para adicionar ao saldo.
- **Saque:** Permite retirar dinheiro, respeitando regras de saldo disponível, limite de saque e número máximo de saques por dia.
- **Extrato:** Exibe todas as transações realizadas e o saldo atual.
- **Sair:** Encerra a execução do programa.

## 🔧 Regras de Operação

1. **Depósitos devem ser positivos**.
2. **Saques estão limitados a R$ 500 por operação**.
3. **O número máximo de saques diários é 3**.
4. **O saldo deve ser suficiente para o saque desejado**.
5. **O extrato exibe todas as movimentações realizadas**.

## 🚀 Como Executar

1. **Instale o Python** (caso não tenha).
2. **Copie o código para um arquivo Python (`sistema_bancario.py`)**.
3. **Execute o script:** 
   ```sh
   python sistema_bancario.py
   ```
