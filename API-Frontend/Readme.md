# 👓 Projeto E-commerce de Óculos (API + Frontend)

Este projeto consiste em uma aplicação web completa de e-commerce para venda de óculos, desenvolvida utilizando o framework **Flask** em Python. A aplicação inclui um sistema de autenticação robusto para usuários e administradores, gerenciamento de produtos (CRUD) e um fluxo de vendas completo com carrinho de compras e checkout.

## 🚀 Tecnologias Utilizadas

O projeto é construído com as seguintes tecnologias:

| Categoria | Tecnologia | Descrição |
| :--- | :--- | :--- |
| **Backend** | **Python** | Linguagem de programação principal. |
| **Framework Web** | **Flask** | Micro-framework para o desenvolvimento da API e do servidor web. |
| **Autenticação** | **Flask-Login** | Gerenciamento de sessões de usuário e controle de acesso. |
| **Banco de Dados** | **SQLite/Módulos Python** | O projeto utiliza módulos Python (`Models` e `Database`) para simular ou interagir com um banco de dados (provavelmente SQLite ou um mock, dada a estrutura). |
| **Frontend** | **HTML/CSS/JavaScript** | Utilizado para a interface do usuário (Templates e `static`). |

## 📁 Estrutura do Projeto

A aplicação segue uma estrutura modular para organização e manutenção:

| Diretório/Arquivo | Descrição |
| :--- | :--- |
| `app.py` | Ponto de entrada da aplicação. Configura o Flask, o Flask-Login e registra os Blueprints (rotas). |
| `Database/` | Contém a lógica de conexão e interação com o banco de dados (`database.py`). |
| `Models/` | Contém as classes de modelo que representam as entidades do sistema e a lógica de negócio (e.g., `Usuario`, `Oculos`, `Vendas`, `CRUD`). |
| `Router/` | Contém os Blueprints do Flask, onde as rotas da API e as funções de visualização são definidas (`router_auth.py`, `router_oculos.py`, `router_vendas.py`). |
| `Templates/` | Contém os arquivos HTML (Jinja2) para renderização das páginas web. |
| `static/` | Contém arquivos estáticos como CSS, JavaScript e imagens. |

## ✨ Funcionalidades Principais

O sistema oferece duas áreas principais de acesso: **Área do Cliente** e **Área Administrativa**.

### 1. Autenticação e Usuários

*   **Registro de Cliente:** Criação de novas contas de usuário.
*   **Login de Cliente:** Acesso à loja e funcionalidades de compra.
*   **Login de Administrador:** Acesso restrito ao painel de gerenciamento de produtos.
*   **Logout:** Encerramento de sessão para ambos os tipos de usuário.

### 2. Gerenciamento de Produtos (CRUD - Apenas Admin)

*   **Criação (Create):** Adicionar novos modelos de óculos ao catálogo.
*   **Leitura (Read):** Visualizar todos os óculos cadastrados.
*   **Atualização (Update):** Modificar informações de um óculos existente.
*   **Exclusão (Delete):** Remover um óculos do catálogo.

### 3. Fluxo de Compra (Cliente)

*   **Home:** Visualização do catálogo de óculos.
*   **Detalhe do Produto:** Visualização de informações detalhadas de um óculos.
*   **Carrinho de Compras:** Adicionar, remover e atualizar a quantidade de itens.
*   **Checkout:** Fluxo de pagamento que inclui cadastro de endereço e finalização da compra.

## 🗺️ Rotas da API e do Sistema

As rotas são organizadas em três Blueprints principais: `auth`, `oculos` e `venda`.

### 1. Rotas de Autenticação (`auth_bp` - Prefixo: `/`)

| Rota | Método | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Exibe a tela de login. | Público |
| `/registro` | `GET` | Exibe a tela de registro. | Público |
| `/registro` | `POST` | Processa o cadastro de um novo usuário. | Público |
| `/login` | `GET` | Exibe a tela de login. | Público |
| `/login` | `POST` | Processa o login do usuário. | Público |
| `/logout` | `GET/POST` | Encerra a sessão do usuário. | Cliente/Admin |
| `/adm/login` | `GET` | Exibe a tela de login do administrador. | Público |
| `/adm/login` | `POST` | Processa o login do administrador. | Público |
| `/adm/logout` | `GET/POST` | Encerra a sessão do administrador. | Admin |

### 2. Rotas de Produtos e Visualização (`oculos_bp` - Prefixo: `/`)

| Rota | Método | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| `/home` | `GET` | Exibe a página inicial da loja (catálogo). | Cliente Logado |
| `/item/<id>` | `GET` | Exibe a página de detalhes de um óculos específico. | Cliente Logado |
| `/oculos` | `POST` | **API:** Cria um novo óculos. | Admin |
| `/oculos` | `GET` | Exibe o painel de gerenciamento de óculos. | Admin |
| `/oculos/update/<id>` | `PUT` | **API:** Atualiza um óculos existente. | Admin |
| `/oculos/delete/<id>` | `DELETE` | **API:** Deleta um óculos. | Admin |

### 3. Rotas de Vendas e Carrinho (`venda_bp` - Prefixo: `/`)

| Rota | Método | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| `/carrinho` | `GET` | Exibe o carrinho de compras do usuário. | Cliente Logado |
| `/carrinho/adicionar` | `POST` | **API:** Adiciona um item ao carrinho. | Cliente Logado |
| `/carrinho/atualizar` | `POST` | **API:** Atualiza a quantidade de um item no carrinho. | Cliente Logado |
| `/carrinho/remover` | `POST` | **API:** Remove um item do carrinho. | Cliente Logado |
| `/carrinho/limpar` | `POST` | **API:** Limpa todos os itens do carrinho. | Cliente Logado |
| `/endereco/<id_compra>` | `GET` | Exibe a tela de cadastro de endereço. | Cliente Logado |
| `/endereco/<id_compra>` | `POST` | Salva o endereço na sessão e redireciona para o pagamento. | Cliente Logado |
| `/<id>/pag` | `GET` | Exibe a tela de pagamento (para item único ou carrinho). | Cliente Logado |
| `/pagamento` | `POST` | **API:** Finaliza o pagamento e a compra. | Cliente Logado |

## 🛠️ Como Executar o Projeto

1.  **Pré-requisitos:** Certifique-se de ter o Python 3 instalado.
2.  **Instalação de Dependências:**
    \`\`\`bash
    # Assumindo que você está no diretório raiz do projeto (Projeto_Api/Projeto_Api)
    pip install Flask Flask-Login
    # Outras dependências podem ser necessárias, como um driver de banco de dados, se não for SQLite.
    \`\`\`
3.  **Execução:**
    \`\`\`bash
    python app.py
    \`\`\`
4.  **Acesso:** A aplicação estará disponível em `http://127.0.0.1:5000/` (ou a porta padrão do Flask).

---
