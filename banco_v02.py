import os
from datetime import date, datetime

# --- Funções Utilitárias ---

def clear_screen():
    """Limpa a tela do terminal"""

    if os.name == 'nt':
        _ = os.system('cls')

    else:
        _ = os.system('clear')

def show_menu(menu_text, options):
    """Função genérica para exibir e validar menus."""
    while True:
        try:
            choice = int(input(menu_text))
            if choice in options:
                return choice
            print(f"\nOpção inválida! Digite apenas uma das opções: {options}.\n")
        except ValueError:
            print("\nErro: Digite apenas números.\n")

# --- Constantes e Variáveis Globais ---
AGENCIA = "0001"
WITHDRAWAL_LIMIT_COUNT = 3

next_account_number = 1
current_user = None

# --- Estrutura de Dados Inicial ---
users = {
    "12312312312": {
        "name": "José Maria", "born": "10/01/1960", "address": "Rua das borboletas, 123 - borboletário - borboletas/MG",
        "senha": "123", "type_account": ["admin", "cliente"], 
        "conta": [
            {"agencia": AGENCIA, "numero": next_account_number, "balance": 1500.0, "bank_statement": "", "tipo": "corrente", "data_abertura": "02/06/2025", "withdrawal_number": 0, "withdrawal_limit_value": 500.00, "last_withdrawal_date": None}
        ]
    },
    "11122233344": {
        "name": "Sabino Setepano", "born": "01/01/1980", "address": "Rua das caçambas, 111 - caçambeiros - caçambas/MG",
        "senha": "232323", "type_account": ["admin"], "conta": []
    }
}

next_account_number += 1

# --- Funções da Área Administrativa ---

def login_admin():
    """Menu de login administrativo."""

    clear_screen()
    print("=========================================================")
    print("Para fins de estudo: (CPF) 12312312312 e (Senha) 123!\n")
    if validate_login("admin"):
        admin_area()

def admin_area():
    """Área administrativa."""

    while True:
        clear_screen()
        menu = f"""======== BEM-VINDO, {current_user['name']}! (Admin) =========

[1] Cadastrar novo cliente
[2] Criar nova conta para cliente existente
[3] Listar clientes e contas
[0] Voltar ao menu anterior (Logout)

=>"""
        choice = show_menu(menu, [0, 1, 2, 3])
        
        if choice == 0:
            break

        elif choice == 1:
            clear_screen()
            register_new_customer()
            input("\nPressione Enter para continuar...")

        elif choice == 2:
            clear_screen()
            new_bank_account_area()
            input("\nPressione Enter para continuar...")

        elif choice == 3:
            clear_screen()
            list_accounts_and_customers()
            input("\nPressione Enter para continuar...")

def register_new_customer():
    """Registra um novo cliente no sistema."""

    print("--- Cadastro de Novo Cliente ---")

    while True:
        novo_cpf = input("Digite o CPF (apenas números) do novo cliente: ").strip()
        
        if not novo_cpf.isdigit() or len(novo_cpf) != 11:
            print("Erro: CPF deve conter exatamente 11 dígitos numéricos.")
            continue
            
        if novo_cpf in users:
            print("Erro: CPF já cadastrado.")
            continue
            
        users[novo_cpf] = {
            "name": input("Informe o nome completo: ").strip(),
            "born": input("Informe a data de nascimento (DD/MM/AAAA): ").strip(),
            "address": input("Endereço (Rua, nº - Bairro - Cidade/UF): ").strip(),
            "senha": input("Crie uma senha para o usuário: "),
            "type_account": ["cliente"],
            "conta": []
        }
        print(f"\n✔ Cliente {users[novo_cpf]['name']} cadastrado com sucesso!")
        print("Agora, crie uma conta para este cliente na opção [2] do menu.")
        break

def new_bank_account_area():
    """Interface para criar novas contas."""

    menu = """====== Criar nova Conta ========
[1] Criar conta corrente
[2] Criar conta poupança
[0] Voltar

+>"""
    choice = show_menu(menu, [0, 1, 2])
    if choice == 0:
        return

    account_type = "corrente" if choice == 1 else "poupança"
    clear_screen()
    print(f"=== Nova Conta {account_type.capitalize()} ===")
    cpf_user = input("Digite o CPF do cliente para vincular a conta: ").strip()

    if validate_cpf(cpf_user, exist=True):
        if "cliente" not in users[cpf_user]["type_account"]:
            users[cpf_user]["type_account"].append("cliente")
            print(f"\n-> Perfil 'cliente' foi atribuído ao usuário {users[cpf_user]['name']}.")
        
        new_bank_account_number(cpf_user, account_type)

def new_bank_account_number(cpf_user, account_type):
    """Cria e adiciona uma nova conta a um usuário."""

    global next_account_number

    menu = f"""
=== Confirmação de Criação de Conta ===
Cliente: {users[cpf_user]["name"]}
CPF: {cpf_user[:3]}.{cpf_user[3:6]}.{cpf_user[6:9]}-{cpf_user[9:]}
Tipo: {account_type.capitalize()}

[S] para CONFIRMAR
[N] para CANCELAR
=> """
    
    confirm = input(menu).strip().lower()
    if confirm == 's':
        nova_conta = {
            "agencia": AGENCIA, "numero": next_account_number, "balance": 0.0, "bank_statement": "",
            "tipo": account_type, "data_abertura": date.today().strftime("%d/%m/%Y"),
            "withdrawal_number": 0, "withdrawal_limit_value": 500.00, "last_withdrawal_date": None
        }
        users[cpf_user]["conta"].append(nova_conta)
        print(f"""
✔ Conta criada com sucesso!
┌─────────────────────────────
│ Cliente: {users[cpf_user]['name']}
│ Agência: {AGENCIA} 
│ Conta Nº: {next_account_number}
│ Tipo: {account_type.capitalize()}
└─────────────────────────────
""")
        next_account_number += 1
    else:
        print("\nOperação cancelada.")

def list_accounts_and_customers():
    """Exibe uma lista de todos os usuários e suas contas."""

    print("=== Lista de Clientes e Contas ===")

    if not users:
        print("Nenhum usuário cadastrado.")
        return

    for cpf, data in users.items():
        print("="*40)
        print(f"Nome: {data['name']} | CPF: {cpf}")
        print(f"Perfis: {', '.join(data['type_account'])}")
        if "cliente" in data["type_account"] and data["conta"]:
            for conta in data["conta"]:
                print(f"  -> Conta {conta['tipo'].capitalize()}: Ag {conta['agencia']} / C.C {conta['numero']} | Saldo: R$ {conta['balance']:.2f}")
        else:
            print("  -> Nenhuma conta bancária cadastrada.")
    print("="*40)

# --- Funções da Área do Cliente ---

def login_customer():
    """Menu de login do cliente."""

    clear_screen()
    print("===== Acesso à Área do Cliente =====")

    if validate_login("cliente"):
        customer_area()

def select_account(customer):
    """Permite que o cliente com múltiplas contas escolha qual usar."""

    if not customer["conta"]:
        print("\nVocê ainda não possui uma conta. Fale com seu gerente.")
        return None

    if len(customer["conta"]) == 1:
        return 0

    clear_screen()
    print("Identificamos mais de uma conta para o seu CPF.")
    menu_text = "Por favor, escolha qual delas gostaria de utilizar:\n\n"
    options = []
    
    for i, conta in enumerate(customer["conta"], 1):
        menu_text += f"[{i}] Conta {conta['tipo'].capitalize()} | Ag: {conta['agencia']} | Nº: {conta['numero']}\n"
        options.append(i)
    menu_text += "\n=> "
    
    choice = show_menu(menu_text, options)
    return choice - 1

def customer_area():
    """Área do cliente, onde as transações são realizadas."""

    active_account_index = select_account(current_user)
    
    if active_account_index is None:
        input("\nPressione Enter para continuar...")
        return

    while True:
        clear_screen()

        active_account = current_user["conta"][active_account_index]

        menu = f"""======== Olá, {current_user['name']}! ========
Conta Ativa: {active_account['tipo'].capitalize()} | Ag: {active_account['agencia']} | Nº: {active_account['numero']}
Saldo: R$ {active_account['balance']:.2f}

[1] Consultar Extrato
[2] Realizar Depósito
[3] Realizar Saque
[4] Trocar de Conta
[0] Sair (Logout)

=>"""
        choice = show_menu(menu, [0, 1, 2, 3, 4])
        
        if choice == 0: break

        elif choice == 1:
            clear_screen()
            display_bank_statement(active_account["balance"], bank_statement=active_account["bank_statement"])
            input("\nPressione Enter para continuar...")

        elif choice == 2:
            handle_deposit(active_account)

        elif choice == 3:
            handle_withdraw(active_account)

        elif choice == 4:
            new_index = select_account(current_user)

            if new_index is not None: active_account_index = new_index

def handle_deposit(account):
    """Lida com a entrada do usuário para depósito."""

    try:
        value = float(input("\nInforme o valor a ser depositado: R$ "))
        new_balance, new_statement = deposit(account["balance"], value, account["bank_statement"])
        account["balance"], account["bank_statement"] = new_balance, new_statement

    except ValueError:
        print("\nErro: Digite um valor numérico válido.")

    input("\nPressione Enter para continuar...")

def handle_withdraw(account):
    """Lida com a entrada do usuário para saque."""

    try:
        value = float(input(f"\nInforme o valor do saque (limite por transação R$ {account['withdrawal_limit_value']:.2f}): R$ "))

        new_balance, new_statement, new_wd_num, new_wd_date = withdraw(
            balance=account["balance"], value=value, bank_statement=account["bank_statement"],
            limit_value=account["withdrawal_limit_value"], withdrawal_number=account["withdrawal_number"],
            limit_count=WITHDRAWAL_LIMIT_COUNT, last_withdrawal_date=account["last_withdrawal_date"]
        )

        account.update({
            "balance": new_balance, "bank_statement": new_statement,
            "withdrawal_number": new_wd_num, "last_withdrawal_date": new_wd_date
        })

    except ValueError:
        print("\nErro: Digite um valor numérico válido.")

    input("\nPressione Enter para continuar...")

# --- Funções de Transação e Validação ---

def validate_login(user_type):
    """Valida o login e armazena o usuário atual."""

    global current_user

    while True:
        login = input("Login (CPF): ").strip()
        senha = input("Senha: ").strip()
        user_data = users.get(login)

        if user_data and senha == user_data["senha"]:
            if user_type in user_data["type_account"]:
                current_user = user_data
                print(f"\nLogin bem-sucedido!")
                input("Pressione Enter para entrar...")
                return True
            
            else:
                print(f"\nErro: Este usuário não possui permissão de {user_type}.")

        else:
            print("\nLogin ou senha incorretos!")
        
        choice = input("Pressione Enter para tentar novamente ou digite 'sair' para voltar: ").strip().lower()
        if choice == "sair": return False

def validate_cpf(cpf_user, exist=True):
    """Valida o formato do CPF e se ele existe no sistema."""

    if not cpf_user.isdigit() or len(cpf_user) != 11:
        print("Erro: CPF deve conter exatamente 11 dígitos numéricos.")
        return False
    
    if exist and cpf_user not in users:
        print("Erro: CPF não encontrado no sistema.")
        return False
    
    return True

def withdraw(*, balance, value, bank_statement, limit_value, withdrawal_number, limit_count, last_withdrawal_date=None):
    """Processa a lógica de saque."""

    today_str = date.today().strftime("%d/%m/%Y")
    if last_withdrawal_date != today_str:
        withdrawal_number = 0
        last_withdrawal_date = today_str
    
    if value <= 0: print("\nOperação falhou! O valor do saque deve ser positivo.")

    elif value > balance: print("\nOperação falhou! Saldo insuficiente.")

    elif value > limit_value: print(f"\nOperação falhou! O valor do saque excede seu limite de R$ {limit_value:.2f} por transação.")

    elif withdrawal_number >= limit_count: print(f"\nOperação falhou! Limite diário de {limit_count} saques atingido.")

    else:
        balance -= value
        withdrawal_number += 1
        operation_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        bank_statement += f"Saque: R$ {value:<10.2f} | Data: {operation_time}\n"
        print(f"\n✔ Saque de R$ {value:.2f} realizado com sucesso!")

    return balance, bank_statement, withdrawal_number, last_withdrawal_date

def deposit(balance, value, bank_statement, /):
    """Processa a lógica de depósito."""

    if value > 0:
        balance += value
        operation_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        bank_statement += f"Depósito: R$ {value:<8.2f} | Data: {operation_time}\n"
        print(f"\n✔ Depósito de R$ {value:.2f} realizado com sucesso!")

    else:
        print("\nOperação falhou! O valor do depósito deve ser positivo.")

    return balance, bank_statement

def display_bank_statement(balance, /, *, bank_statement):
    """Exibe o extrato formatado."""

    print(" EXTRATO BANCÁRIO ".center(47, "="))
    if not bank_statement:
        print("\nNão foram realizadas movimentações.\n")

    else:
        print(bank_statement)

    print(f"Saldo Atual: R$ {balance:.2f}")
    print("=" * 47)

# --- Função Principal ---

def main():
    while True:
        global current_user
        current_user = None
        
        clear_screen()

        menu = """================================================
Olá! Seja bem vindo ao nosso sistema bancário!!
Por favor, escolha uma das opções abaixo.

[1] Acesso Administrativo
[2] Acesso Cliente
[0] Sair

=> """
        choice = show_menu(menu, [0, 1, 2])
        
        if choice == 0:
            clear_screen()
            print("Obrigado por usar nosso sistema. Até logo!\n")
            break

        elif choice == 1:
            login_admin()
            
        elif choice == 2:
            login_customer()

if __name__ == "__main__":
    main()