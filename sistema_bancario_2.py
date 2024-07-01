from typing import List

BASE_ERROR = "Operação falhou!"


def menu():
    menu = """
        BEM VINDO AO GJBANK!

        SELECIONE UMA DAS SEGUINTES OPÇÕES:
      |---------------------|
      | [1] Extrato         |
      | [2] Sacar           |
      | [3] Depositar       |
      | [4] Criar usuário   |
      | [5] Criar conta     |
      | [6] Listar contas   |
      | [7] Listar usuário  |
      | [0] Sair            |
      |---------------------|

        => """

    return input(menu)


def get_bank_statement(balance: float, bank_statement: str):
    print("\n================ EXTRATO ================")
    print(
        "Não foram realizadas movimentações." if not bank_statement else bank_statement
    )
    print(f"\nSaldo: R$ {balance:.2f}")
    print("==========================================")


def withdraw(
    value: float,
    balance: float,
    bank_statement: str,
    withdraws: int,
    value_limit: int,
    withdraws_limit: int,
):
    # withdraws = 0
    exceeded_balance = value > balance

    exceeded_limit = value > value_limit

    exceeded_withdraws = withdraws >= withdraws_limit

    if exceeded_balance:
        print(f"{BASE_ERROR} Você não tem saldo suficiente.")

    elif exceeded_limit:
        print(f"{BASE_ERROR} O valor do saque excede o limite.")

    elif exceeded_withdraws:
        print(f"{BASE_ERROR} Número máximo de saques excedido.")

    elif value > 0:
        balance -= value
        bank_statement += f"Saque: R$ {value:.2f}\n"
        withdraws += 1
        print(
            f"""Saque de R$ {value:.2f} realizado com sucesso!
---------------------------------------------\n"""
        )

    else:
        print(f"{BASE_ERROR} O valor informado é inválido.")

    return balance, bank_statement


def deposit(balance: float, value: float, bank_statement: str):
    if value > 0.0:
        balance += value
        bank_statement += f"Depósito: R$ {value:.2f}\n"
        print(
            f"""Depósito de R$ {value:.2f} realizado com sucesso!
    ---------------------------------------------\n"""
        )

    else:
        print(f"{BASE_ERROR} O valor informado é inválido.")

    return balance, bank_statement


def create_user(users_list: [str]):
    cpf = input("Insira seu CPF: ")

    user = filter_users(cpf, users_list)

    if user:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    name = input("Informe o nome completo: ")
    birth_date = input("Informe a data de nascimento (dd-mm-aaaa): ")
    address = input("Informe o endereço (rua, nº - bairro - cidade/Estado): ")

    users_list.append(
        {
            "nome": name,
            "data_nascimento": birth_date,
            "cpf": cpf,
            "endereco": address,
        }
    )

    print("=== Usuário criado com sucesso! ===")


def create_account(agency: str, account_number: int, users_list: List):
    cpf = input("Informe o CPF do usuário: ")
    user = filter_users(cpf, users_list)

    if user:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agency, "numero_conta": account_number, "usuario": user}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def filter_users(cpf: str, users_list: List):
    filtered_users = [user for user in users_list if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None


def get_accounts(accounts_list: [str]):
    if not accounts_list:
        print(f"{BASE_ERROR} Usuário ainda não tem conta criada.")
    for account in accounts_list:
        new_account_line = f"""\
            Agência:\t{account['agencia']}
            C/C:\t\t{account['numero_conta']}
            Titular:\t{account['usuario']['nome']}
        """
        print("=" * 100)
        print(new_account_line)


def get_users(users_list: [str]):
    if not users_list:
        print(f"{BASE_ERROR} Não existe usuário cadastrado!")
    for user in users_list:
        user_line = f"""\
            Nome:\t{user['nome']}
            Data de nascimento:\t\t{user['data_nascimento']}
            CPF:\t{user['cpf']}
            Endereço:\t{user['endereco']}
        """
        print("=" * 100)
        print(user_line)


def main():
    WITHDRAW_VALUE_LIMIT = 500
    WITHDRAWS_LIMIT = 3
    AGENCY = "0001"

    users_list = []
    accounts_list = []
    balance = 0
    bank_statement = ""
    withdraws = 0

    while True:
        option = menu()

        if option == "1":
            get_bank_statement(balance, bank_statement=bank_statement)

        elif option == "2":
            value = float(input("Informe o valor do saque: "))

            balance, bank_statement = withdraw(
                value=value,
                balance=balance,
                bank_statement=bank_statement,
                withdraws=withdraws,
                value_limit=WITHDRAW_VALUE_LIMIT,
                withdraws_limit=WITHDRAWS_LIMIT,
            )

        elif option == "3":
            value = float(input("Informe o valor do depósito: "))

            balance, bank_statement = deposit(value, balance, bank_statement)

        elif option == "4":
            create_user(users_list=users_list)

        elif option == "5":
            account_number = len(accounts_list) + 1
            account = create_account(
                AGENCY, account_number=account_number, users_list=users_list
            )

            if account:
                accounts_list.append(account)

        elif option == "6":
            get_accounts(accounts_list)

        elif option == "7":
            get_users(users_list)

        elif option == "0":
            print("=== Saindo do sistema... ===")
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )


main()
