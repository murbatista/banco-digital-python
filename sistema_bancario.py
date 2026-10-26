def ler_valor(mensagem):
    try:
        return float(input(mensagem).replace(",", "."))
    except ValueError:
        print("Entrada inválida! Digite um número.")
        return None


def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print("Depósito realizado com sucesso!")
    else:
        print("Valor inválido.")

    return saldo, extrato


def sacar(saldo, valor, extrato, numero_saques):
    limite_saques = 3
    limite_saque = 500

    if valor <= 0:
        print("Valor inválido.")
    elif valor > limite_saque:
        print("O valor máximo por saque é R$ 500,00.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    elif numero_saques >= limite_saques:
        print("Limite de saques diários atingido.")
    else:
        saldo -= valor
        numero_saques += 1
        extrato.append(f"Saque: R$ {valor:.2f}")
        print("Saque realizado com sucesso!")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato):
    print("\n===== EXTRATO =====")

    if not extrato:
        print("Nenhuma movimentação realizada.")
    else:
        for movimentacao in extrato:
            print(movimentacao)

    print(f"Saldo atual: R$ {saldo:.2f}")


def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()

    if not cpf.isdigit() or len(cpf) != 11:
        print("CPF inválido. Digite os 11 números.")
        return

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Já existe um usuário com esse CPF.")
            return

    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
    endereco = input("Endereço (logradouro, número - bairro - cidade/UF): ").strip()

    if not nome or not data_nascimento or not endereco:
        print("Todos os campos são obrigatórios.")
        return

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("Usuário cadastrado com sucesso!")


def criar_conta(usuarios, contas, numero_conta):
    cpf = input("Informe o CPF do titular: ").strip()

    usuario_encontrado = None

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario_encontrado = usuario
            break

    if usuario_encontrado is None:
        print("Usuário não encontrado. Cadastre o usuário primeiro.")
        return numero_conta

    conta = {
        "agencia": "0001",
        "numero_conta": numero_conta,
        "usuario": usuario_encontrado,
        "saldo": 0,
        "extrato": [],
        "numero_saques": 0
    }

    contas.append(conta)

    print("Conta corrente criada com sucesso!")
    print(f"Agência: {conta['agencia']}")
    print(f"Número da conta: {conta['numero_conta']}")
    print(f"Titular: {usuario_encontrado['nome']}")

    return numero_conta + 1


def selecionar_conta(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return None

    cpf = input("Informe o CPF do titular da conta: ").strip()

    contas_encontradas = []

    for conta in contas:
        if conta["usuario"]["cpf"] == cpf:
            contas_encontradas.append(conta)

    if not contas_encontradas:
        print("Nenhuma conta encontrada para esse CPF.")
        return None

    if len(contas_encontradas) == 1:
        return contas_encontradas[0]

    print("\nContas encontradas:")

    for conta in contas_encontradas:
        print(f"Conta: {conta['numero_conta']}")

    try:
        numero = int(input("Digite o número da conta desejada: "))
    except ValueError:
        print("Número de conta inválido.")
        return None

    for conta in contas_encontradas:
        if conta["numero_conta"] == numero:
            return conta

    print("Conta não encontrada.")
    return None


def main():
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        print("\n===== SISTEMA BANCÁRIO =====")
        print("[1] Cadastrar usuário")
        print("[2] Criar conta corrente")
        print("[3] Depositar")
        print("[4] Sacar")
        print("[5] Extrato")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario(usuarios)

        elif opcao == "2":
            numero_conta = criar_conta(
                usuarios, contas, numero_conta
            )

        elif opcao in ("3", "4", "5"):
            conta = selecionar_conta(contas)

            if conta is None:
                continue

            if opcao == "3":
                valor = ler_valor("Valor do depósito: R$ ")

                if valor is not None:
                    conta["saldo"], conta["extrato"] = depositar(
                        conta["saldo"], valor, conta["extrato"]
                    )

            elif opcao == "4":
                valor = ler_valor("Valor do saque: R$ ")

                if valor is not None:
                    (
                        conta["saldo"],
                        conta["extrato"],
                        conta["numero_saques"]
                    ) = sacar(
                        conta["saldo"],
                        valor,
                        conta["extrato"],
                        conta["numero_saques"]
                    )

            elif opcao == "5":
                exibir_extrato(conta["saldo"], conta["extrato"])

        elif opcao == "0":
            print("Obrigado por utilizar nosso sistema!")
            break

        else:
            print("Opção inválida. Tente novamente.")


main()
