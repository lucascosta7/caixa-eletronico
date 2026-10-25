from database.conexao import conectar

def consultar_saldo(conta_id):
    with conectar() as conexao:
        conta = conexao.execute(
            """
            SELECT saldo_centavos, bloqueada
            FROM contas
            WHERE id = ?
            """,
            (conta_id,),
        ).fetchone()

        if conta is None:
            raise ValueError("Conta não encontrada.")

        if conta["bloqueada"]:
            raise ValueError("Esta conta está bloqueada.")

        return conta["saldo_centavos"]

def depositar(conta_id, valor_centavos):
    if not isinstance(valor_centavos, int) or isinstance(valor_centavos, bool):
        raise ValueError("O valor deve ser um inteiro de centavos.")

    if valor_centavos <= 0:
        raise ValueError("O valor do depósito deve ser maior que zero.")

    with conectar() as conexao:
        conta = conexao.execute(
            """
            SELECT bloqueada
            FROM contas
            WHERE id = ?
            """,
            (conta_id,),
        ).fetchone()

        if conta is None:
            raise ValueError("Conta não encontrada.")

        if conta["bloqueada"]:
            raise ValueError("Esta conta está bloqueada.")

        conexao.execute(
            """
            UPDATE contas
            SET saldo_centavos = saldo_centavos + ?
            WHERE id = ?
            """,
            (valor_centavos, conta_id),
        )

        conexao.execute(
            """
            INSERT INTO transacoes (conta_destino_id, tipo, valor_centavos)
            VALUES (?, 'DEPOSITO', ?)
            """,
            (conta_id, valor_centavos),
        )

    return consultar_saldo(conta_id)

def sacar(conta_id, valor_centavos):
    if not isinstance(valor_centavos, int) or isinstance(valor_centavos, bool):
        raise ValueError("O valor deve ser um número inteiro de centavos.")

    if valor_centavos <= 0:
        raise ValueError("O saque deve ser maior que zero.")

    with conectar() as conexao:
        conta = conexao.execute(
            """
            SELECT saldo_centavos, bloqueada
            FROM contas
            WHERE id = ?
            """,
            (conta_id,),
        ).fetchone()

        if conta is None:
            raise ValueError("Conta não encontrada.")

        if conta["bloqueada"]:
            raise ValueError("Esta conta está bloqueada.")

        if conta["saldo_centavos"] < valor_centavos:
            raise ValueError("Saldo insuficiente para realizar o saque.")

        conexao.execute(
            """
            UPDATE contas
            SET saldo_centavos = saldo_centavos - ?
            WHERE id = ?
            """,
            (valor_centavos, conta_id),
        )

        conexao.execute(
            """
            INSERT INTO transacoes (conta_origem_id, tipo, valor_centavos)
            VALUES (?, 'SAQUE', ?)
            """,
            (conta_id, valor_centavos),
        )

    return consultar_saldo(conta_id)


def consultar_extrato(conta_id):
    with conectar() as conexao:
        conta = conexao.execute(
            "SELECT id FROM contas WHERE id = ?",
            (conta_id,),
        ).fetchone()

        if conta is None:
            raise ValueError("Conta não encontrada.")

        transacoes = conexao.execute(
            """
            SELECT tipo, valor_centavos, data_hora,
                CASE
                    WHEN conta_destino_id = ? THEN 'ENTRADA'
                    ELSE 'SAIDA'
                END AS direcao
            FROM transacoes
            WHERE conta_origem_id = ? OR conta_destino_id = ?
            ORDER BY id DESC
            """,
            (conta_id, conta_id, conta_id),
        ).fetchall()

    return [dict(transacao) for transacao in transacoes]

def transferir(conta_origem_id, numero_conta_destino, valor_centavos):
    if not isinstance(valor_centavos, int) or isinstance(valor_centavos, bool):
        raise ValueError("O valor deve ser um número inteiro de centavos.")

    if valor_centavos <= 0:
        raise ValueError("O valor da transferência deve ser maior que zero.")

    numero_conta_destino = numero_conta_destino.strip().upper()

    with conectar() as conexao:
        origem = conexao.execute(
            """
            SELECT id, saldo_centavos, bloqueada
            FROM contas
            WHERE id = ?
            """,
            (conta_origem_id,),
        ).fetchone()

        if origem is None:
            raise ValueError("Conta de origem não encontrada.")

        if origem["bloqueada"]:
            raise ValueError("A conta de origem está bloqueada.")

        destino = conexao.execute(
            """
            SELECT id, bloqueada
            FROM contas
            WHERE numero = ?
            """,
            (numero_conta_destino,),
        ).fetchone()

        if destino is None:
            raise ValueError("Conta de destino não encontrada.")

        if destino["bloqueada"]:
            raise ValueError("A conta de destino está bloqueada.")

        if origem["id"] == destino["id"]:
            raise ValueError("Não é possível transferir para a própria conta.")

        if origem["saldo_centavos"] < valor_centavos:
            raise ValueError("Saldo insuficiente para realizar a transferência.")

        conexao.execute(
            """
            UPDATE contas
            SET saldo_centavos = saldo_centavos - ?
            WHERE id = ?
            """,
            (valor_centavos, origem["id"]),
        )

        conexao.execute(
            """
            UPDATE contas
            SET saldo_centavos = saldo_centavos + ?
            WHERE id = ?
            """,
            (valor_centavos, destino["id"]),
        )

        conexao.execute(
            """
            INSERT INTO transacoes (conta_origem_id, conta_destino_id, tipo, valor_centavos)
            VALUES (?, ?, 'TRANSFERENCIA', ?)
            """,
            (conta_origem_id, destino["id"], valor_centavos),
        )

    return consultar_saldo(conta_origem_id)