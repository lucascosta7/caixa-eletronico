import hashlib
import secrets
import hmac
from database.conexao import conectar

def gerar_hash_senha(senha):
    salt = secrets.token_bytes(10)

    hash_senha = hashlib.pbkdf2_hmac( 
        "sha256",
        senha.encode("utf-8"),
        salt,
        600_000,
    )

    return salt.hex() + ":" + hash_senha.hex()

def cadastrar_conta(titular, senha, deposito_inicial=0):
    titular = titular.strip()

    if not titular:
        raise ValueError("O nome do titular é obrigatório.")

    if len(senha) < 6:
        raise ValueError("A senha deve ter pelo menos 6 caracteres.")

    if not isinstance(deposito_inicial, int) or isinstance(deposito_inicial, bool):
        raise ValueError("O depósito inicial deve ser informado em centavos.")

    if deposito_inicial < 0:
        raise ValueError("O depósito inicial não pode ser negativo.")

    numero_conta = secrets.token_hex(4).upper()
    senha_hash = gerar_hash_senha(senha)

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO contas (numero, titular, senha_hash, saldo_centavos)
            VALUES (?, ?, ?, ?)
            """,
            (numero_conta, titular, senha_hash, deposito_inicial),
        )

        conta_id = cursor.lastrowid

    return {
        "id": conta_id,
        "numero": numero_conta,
        "titular": titular,
        "saldo_centavos": deposito_inicial,
    }

def verificar_senha(senha_digitada, senha_hash):
    salt_hex, hash_original, = senha_hash.split(":")
    salt = bytes.fromhex(salt_hex)

    hash_digitada = hashlib.pbkdf2_hmac(
        "sha256",
        senha_digitada.encode("utf-8"),
        salt,
        600_000,
    ).hex()

    return hmac.compare_digest(hash_digitada, hash_original)

def autenticar_conta(numero_conta, senha):
    with conectar() as conexao:
        conta = conexao.execute(
            """
            SELECT id, numero, titular, senha_hash, saldo_centavos, bloqueada
            FROM contas
            WHERE numero = ?
            """,
            (numero_conta.strip().upper(),),
        ).fetchone()

        if conta is None:
            raise None

        if conta["bloqueada"]:
            return None

        if not verificar_senha(senha, conta["senha_hash"]):
            return None

        return {
            "id": conta["id"],
            "numero": conta["numero"],
            "titular": conta["titular"],
            "saldo_centavos": conta["saldo_centavos"],
        }