# 🏦 Banco Digital | Sistema de Caixa Eletrônico em Python

Aplicação desktop de um sistema bancário desenvolvido em Python, com interface gráfica moderna, persistência de dados em SQLite e funcionalidades essenciais de um caixa eletrônico.

O projeto permite cadastrar clientes, autenticar usuários, consultar saldos, realizar depósitos e saques, transferir valores entre contas e consultar o histórico de movimentações.

Desenvolvido com o objetivo de praticar programação orientada a objetos, interfaces gráficas, persistência de dados, validação de operações financeiras e organização de projetos Python.

---

## 📸 Sobre o projeto

O **Banco Digital** simula as operações básicas de um sistema bancário por meio de uma aplicação desktop para Windows.

A interface foi desenvolvida com CustomTkinter, utilizando um design minimalista, com tons de azul-marinho, branco e azul, priorizando a clareza e a facilidade de uso.

### Principais características

- Interface gráfica intuitiva.
- Cadastro de novas contas bancárias.
- Autenticação por número da conta e senha.
- Armazenamento persistente de dados em banco SQLite.
- Consulta de saldo disponível.
- Operações de depósito e saque.
- Transferências entre contas.
- Extrato com histórico de movimentações.
- Validação de valores monetários.
- Armazenamento de valores financeiros em centavos inteiros para evitar imprecisões comuns em operações com números de ponto flutuante.

---

## ✨ Funcionalidades

### 👤 Cadastro de clientes

- Cadastro de um novo titular.
- Criação e confirmação de senha.
- Geração automática do número da conta, conforme a implementação do serviço de contas.
- Possibilidade de informar um depósito inicial.
- Armazenamento dos dados no banco SQLite.

### 🔐 Autenticação

- Login utilizando número da conta e senha.
- Verificação das credenciais por meio do serviço de autenticação.
- Exibição de mensagens para situações de erro.

### 💰 Consulta de saldo

- Visualização do saldo da conta autenticada.
- Atualização do saldo após as operações bancárias.

### 📥 Depósitos

- Entrada de valores monetários.
- Validação do valor informado.
- Atualização do saldo e registro da movimentação.

### 📤 Saques

- Solicitação de um valor para saque.
- Validação das regras da operação.
- Atualização do saldo e registro da movimentação.

### 🔄 Transferências

- Transferência de valores entre contas cadastradas.
- Identificação da conta de destino pelo número da conta.
- Atualização dos saldos envolvidos e registro da movimentação, conforme as regras implementadas nos serviços.

### 📄 Extrato bancário

- Consulta do histórico de movimentações.
- Exibição do tipo de transação, direção, data e valor.
- Apresentação das movimentações em uma janela com rolagem.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia                                                | Finalidade                                          |
| --------------------------------------------------------- | --------------------------------------------------- |
| [Python](https://www.python.org/)                         | Linguagem de programação                            |
| [CustomTkinter](https://customtkinter.tomschimansky.com/) | Interface gráfica desktop                           |
| Tkinter                                                   | Caixas de diálogo e componentes gráficos auxiliares |
| [SQLite](https://www.sqlite.org/)                         | Banco de dados relacional                           |
| `sqlite3`                                                 | Integração entre Python e SQLite                    |
| `hashlib` ou biblioteca de hash utilizada no serviço      | Proteção de senhas, conforme a implementação        |
| `decimal`                                                 | Tratamento de valores monetários                    |
| `pathlib`                                                 | Manipulação de caminhos de arquivos                 |
| `venv`                                                    | Isolamento das dependências do projeto              |

> O projeto utiliza bibliotecas da biblioteca padrão do Python e a dependência externa CustomTkinter. Caso os serviços utilizem outras bibliotecas externas, elas também deverão ser instaladas.

---

## 📋 Pré-requisitos

Antes de executar o projeto, você precisará ter instalado:

- Python 3.12 ou superior, preferencialmente uma versão testada com as dependências utilizadas.
- Git, caso deseje clonar o repositório.
- Visual Studio Code ou outro editor de código de sua preferência.

O projeto foi desenvolvido e testado em ambiente Windows com Python 3.14.

---

## 🚀 Instalação e execução

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/caixa-eletronico.git
```

Entre na pasta do projeto:

```bash
cd caixa-eletronico
```

### 2. Crie um ambiente virtual

No Windows, utilizando PowerShell:

```powershell
python -m venv .venv
```

O ambiente virtual mantém as dependências do projeto isoladas de outras instalações Python do computador.

### 3. Ative o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se estiver utilizando o Prompt de Comando (CMD), execute:

```cmd
.venv\Scripts\activate.bat
```

### 4. Instale as dependências

Instale o CustomTkinter:

```powershell
python -m pip install customtkinter
```

Se o projeto possuir outras dependências externas, instale-as também.

### 5. Execute a aplicação

Na raiz do projeto, execute:

```powershell
python main.py
```

A janela do Banco Digital deverá abrir. Na tela inicial, você poderá criar uma conta ou entrar com uma conta já cadastrada.

---

## 📂 Estrutura do projeto

A estrutura abaixo representa a organização esperada dos principais arquivos e módulos do projeto. Ajuste os arquivos de teste conforme os que realmente estiverem presentes no seu repositório.

```text
caixa-eletronico/
│
├── main.py
│
├── database/
│   ├── __init__.py
│   └── conexao.py
│
├── services/
│   ├── __init__.py
│   ├── contas.py
│   └── operacoes.py
│
├── testar_cadastro.py
├── testar_login.py
├── testar_saldo.py
├── testar_deposito.py
├── testar_extrato.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Responsabilidade dos módulos

**`main.py`**

Responsável pela inicialização da aplicação, interface gráfica, telas de login e cadastro, painel principal e interação com as operações bancárias.

**`database/conexao.py`**

Responsável pela conexão com o SQLite, inicialização do banco de dados, criação das tabelas e configuração da conexão.

**`services/contas.py`**

Responsável pelas operações relacionadas às contas, como cadastro e autenticação de clientes.

**`services/operacoes.py`**

Responsável pelas operações bancárias, incluindo consulta de saldo, depósitos, saques, transferências e extrato.

**`testar_*.py`**

Scripts utilizados para verificar individualmente as funcionalidades durante o desenvolvimento.

**`requirements.txt`**

Arquivo destinado à lista de dependências externas necessárias para executar o projeto.

---

## 🗄️ Banco de dados

O sistema utiliza SQLite, um banco de dados relacional que dispensa a instalação de um servidor de banco de dados separado.

Na configuração atual, o arquivo `caixa_eletronico.db` é criado na raiz do projeto quando o banco é inicializado.

### Tabela `contas`

Armazena os dados das contas bancárias, incluindo:

- Identificador da conta.
- Número da conta.
- Nome do titular.
- Hash da senha.
- Saldo armazenado em centavos.
- Indicador de bloqueio.
- Data de criação.

### Tabela `transacoes`

Armazena as movimentações financeiras, incluindo:

- Identificador da transação.
- Conta de origem.
- Conta de destino.
- Tipo da operação.
- Valor em centavos.
- Data e hora da movimentação.

O banco utiliza restrições para evitar valores negativos no saldo, limitar os tipos de transação permitidos e manter referências entre contas e movimentações.

O histórico de transações permite consultar as operações registradas ao longo do uso da aplicação.

---

## 🧪 Testes

Durante o desenvolvimento, foram utilizados scripts independentes para testar as principais operações do sistema.

Por exemplo:

```powershell
python testar_cadastro.py
python testar_login.py
python testar_saldo.py
python testar_deposito.py
python testar_extrato.py
```

Execute esses comandos somente se os respectivos arquivos estiverem presentes na raiz do projeto.

Os testes ajudam a identificar problemas nos serviços antes de integrar ou modificar a interface gráfica.

**Observação:** os scripts acima são testes manuais. O projeto poderá ser ampliado com testes automatizados utilizando `unittest` ou `pytest`.

---

## 🔒 Segurança e limitações

Este projeto tem finalidade educacional e demonstra conceitos de desenvolvimento de aplicações desktop com operações financeiras simuladas.

Embora utilize banco de dados, validações e armazenamento de hashes de senha, ele **não deve ser utilizado para administrar dinheiro real nem para armazenar dados bancários reais**.

Antes de utilizar uma aplicação financeira em um ambiente real, seriam necessários, entre outros:

- Mecanismos de autenticação e autorização mais robustos.
- Proteção adequada contra tentativas repetidas de acesso.
- Revisão independente da implementação de segurança.
- Garantias de integridade e atomicidade das operações financeiras.
- Registro de auditoria e monitoramento.
- Tratamento seguro de erros e informações sensíveis.
- Testes automatizados abrangentes.
- Estratégias de backup e recuperação.
- Adequação às normas e obrigações legais aplicáveis.

A presença de um hash de senha, por si só, não garante a segurança completa do sistema.

---

## 📚 Objetivos de aprendizagem

Este projeto foi desenvolvido para praticar:

- Programação orientada a objetos em Python.
- Criação de interfaces gráficas com CustomTkinter.
- Organização do código em módulos.
- Manipulação de bancos de dados relacionais.
- Operações CRUD.
- Autenticação e validação de dados.
- Tratamento de exceções.
- Manipulação de valores monetários.
- Versionamento de código com Git e GitHub.

---

## 👨‍💻 Autor

**Lucas Gabriel**

Projeto desenvolvido para fins de estudo e prática de desenvolvimento de software com Python.

- GitHub: [Acesse meu perfil](https://github.com/lucascosta7)

---

## 📄 Licença

Este projeto ainda não possui uma licença definida.

Se desejar permitir que outras pessoas utilizem, modifiquem e distribuam o código, considere adicionar uma licença, como a [MIT License](https://opensource.org/license/mit).

Até que uma licença seja adicionada ao repositório, não presuma que terceiros possuem autorização para reutilizar o código.

---

⭐ Se este projeto for útil para seus estudos, fique à vontade para acompanhar sua evolução no GitHub.
