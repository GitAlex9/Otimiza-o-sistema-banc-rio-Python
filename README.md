# Sistema Bancário em Python
Este repositório contém um projeto de um sistema bancário simples, desenvolvido em Python como parte do desafio de projeto do bootcamp **Backend Python** oferecido pelo Santander em parceria com a Digital Innovation One (DIO).

## Contexto do Desafio

O desafio foi dividido em duas etapas evolutivas, com o objetivo de aplicar progressivamente os conceitos aprendidos no curso:

1.  **Etapa 1: Sistema com Estruturas Condicionais**
    * A [primeira versão do sistema](https://github.com/GitAlex9/desafio-sistema-bancario-dio) foi criada utilizando apenas variáveis, operadores e estruturas condicionais. O objetivo era simular operações de depósito, saque (com limite de 3 saques diários e valor máximo de R$ 500) e extrato para um único usuário, sem o uso de funções ou estruturas de dados complexas.

2.  **Etapa 2: Refatoração com Funções e Estruturas de Dados**
    * A segunda etapa exigia a refatoração do código para torná-lo mais modular e escalável. Os requisitos incluíam:
        * Modularizar as operações de saque, depósito e extrato em funções.
        * Implementar regras específicas para a passagem de argumentos nas funções (positional-only e keyword-only).
        * Permitir a criação de múltiplos usuários (clientes).
        * Permitir a criação de múltiplas contas correntes, vinculadas a um usuário.
        * Armazenar os dados de usuários e contas em listas e dicionários.

## Funcionalidades Implementadas

Esta versão do projeto não apenas cumpre todos os requisitos da Etapa 2, mas também incorpora funcionalidades adicionais para criar um sistema mais robusto, seguro e próximo de uma aplicação real.

### Funcionalidades Base (Requisitos do Desafio)

* **Depositar:** Recebe valores monetários para adicionar ao saldo da conta.
* **Sacar:** Permite retiradas do saldo, respeitando um limite de valor por transação e um limite de 3 saques diários.
* **Exibir Extrato:** Mostra todas as transações realizadas e o saldo atual da conta.
* **Criar Usuário (Cliente):** Cadastra um novo cliente no sistema com seus dados pessoais.
* **Criar Conta Corrente:** Cria uma nova conta bancária (Agência 0001) e a vincula a um CPF de cliente já cadastrado.
* **Listar Contas:** Exibe todas as contas e clientes cadastrados no sistema (função de admin).

### Funcionalidades Adicionais (Melhorias Implementadas)

* **Sistema de Autenticação:** Implementação de um sistema de login com CPF e senha, garantindo que apenas usuários autorizados acessem suas informações.
* **Separação de Perfis (Admin vs. Cliente):**
    * **Perfil Cliente:** Acessa apenas as funcionalidades transacionais de suas próprias contas (saque, depósito, extrato).
    * **Perfil Admin:** Possui privilégios para gerenciar o sistema, como cadastrar novos clientes e criar contas.
* **Estrutura de Dados Otimizada:** Em vez de usar listas simples, o sistema utiliza um dicionário principal onde as chaves são os CPFs dos usuários. Isso garante que não haja CPFs duplicados e torna a busca por um usuário uma operação de tempo constante O(1), muito mais eficiente.
* **Múltiplas Contas por Cliente:** A arquitetura permite que um único cliente possua diversas contas (corrente e poupança), que podem ser selecionadas após o login.
* **Melhoria de Interface de Console (CLI):**
    * Uso de menus claros e interativos para facilitar a navegação.
    * Implementação de uma função `clear_screen` para limpar o terminal a cada nova tela, tornando a experiência do usuário mais limpa e organizada.
* **Modularização Avançada:** O código foi dividido em funções com responsabilidades únicas (ex: `validate_cpf`, `select_account`), seguindo os princípios de código limpo.


## Autor

**Alex de Souza Braga**
