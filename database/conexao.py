import sqlite3
from pathlib import Path

PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = PASTA_PROJETO / "caixa_eletronico.db"

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    conexao.row_factory = sqlite3.Row

    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao

def inicializar_banco():
    with conectar() as conexao:
        conexao.executescript(
            """
            CREATE TABLE IF NOT EXISTS contas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT NOT NULL UNIQUE,
                titular TEXT NOT NULL,
                senha_hash TEXT NOT NULL,
                saldo_centavos INTEGER NOT NULL DEFAULT 0 CHECK (saldo_centavos >= 0),
                bloqueada INTEGER NOT NULL DEFAULT 0 CHECK (bloqueada IN (0, 1)),
                criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conta_origem_id INTEGER,
                conta_destino_id INTEGER,
                tipo TEXT NOT NULL CHECK (tipo IN ('DEPOSITO', 'SAQUE', 'TRANSFERENCIA')),
                valor_centavos INTEGER NOT NULL CHECK (valor_centavos > 0),
                data_hora TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conta_origem_id) REFERENCES contas(id),
                FOREIGN KEY (conta_destino_id) REFERENCES contas(id)
            );

            CREATE INDEX IF NOT EXISTS idx_transacoes_origem_data ON transacoes (conta_origem_id, data_hora);
            CREATE INDEX IF NOT EXISTS idx_transacoes_destino_data ON transacoes (conta_destino_id, data_hora);
            """
        )

if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados inicializado com sucesso.")
    print(f"Localização: {CAMINHO_BANCO}")