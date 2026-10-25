
from database.conexao import conectar


def verificar_tabelas():
    """Exibe as tabelas existentes no banco."""

    with conectar() as conexao:
        resultado = conexao.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = ?
              AND name NOT LIKE ?
            """,
            ("table", "sqlite_%"),
        )

        tabelas = resultado.fetchall()

        print("Tabelas encontradas:")

        for tabela in tabelas:
            print(f"- {tabela['name']}")


if __name__ == "__main__":
    verificar_tabelas()
