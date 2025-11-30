# 🕶️ E-Commerce de Óculos – Projeto Completo

Este repositório contém o desenvolvimento de uma **loja online de óculos**, composta por três camadas principais:

* **API Backend** construída com **Flask (Python)**
* **Frontend** utilizando **HTML, CSS e JavaScript puro**, localizados na pasta `templates/`
* **Banco de Dados** em **MySQL**, executado através do **XAMPP**

O objetivo do projeto é fornecer um sistema simples, funcional e bem estruturado para simular um e-commerce completo, desde produtos cadastrados até carrinho e pagamentos.

---

## 📌 Visão Geral do Sistema

A aplicação permite:

* Visualização de óculos, filtrados por **marca**, **forma** e **material**
* Gerenciamento de **carrinho de compras**
* Registro de **usuários**
* Registro de **pagamentos**
* Lógica administrativa (via entidade *Adm*)
* Processamento de itens do carrinho relacionados aos produtos

Toda a comunicação entre o frontend e o banco de dados acontece por meio da **API Flask**, responsável por fornecer endpoints para listagem, cadastro, autenticação e operações do carrinho.

---

## 🛠️ Tecnologias Utilizadas

### **Backend**

* Python 3
* Flask
* Flask-CORS (se aplicável)
* MySQL Connector / SQLAlchemy (dependendo da sua implementação)

### **Frontend**

* HTML5
* CSS3
* JavaScript puro
* Arquivos localizados em:

  ```
  /templates
  ```

### **Banco de Dados**

* MySQL
* Gerenciado via **XAMPP (phpMyAdmin)**
* Scripts e modelo conceitual incluídos na pasta de banco

---

## 🗂️ Estrutura Geral do Repositório

```
/api/              → API Flask (backend)
/templates/        → HTML, CSS e JS do frontend
/database/         → Scripts SQL + diagramas
README.md          → Este arquivo
```

---

## 🗄️ Banco de Dados

O banco segue um modelo baseado no diagrama conceitual contendo tabelas como:

* `Usuario`
* `Carrinho`
* `Pagamento`
* `Itens_Carrinho`
* `Oculos`
* `Marca`
* `Forma`
* `Material`
* `Adm`

As relações foram projetadas para representar um fluxo real de e-commerce, com usuários podendo possuir múltiplos carrinhos e pagamentos, e produtos ligados às suas respectivas características.

O banco deve ser importado via:

```
http://localhost/phpmyadmin
```

Usando o MySQL do XAMPP com:

* **Host**: `localhost`
* **Usuário**: `root`
* **Senha**: *(vazia por padrão)*

---

## 🚀 Executando o Projeto

### **1. Iniciar o backend (Flask)**

Dentro da pasta `/api`:

```
python app.py
```

O servidor irá iniciar, normalmente em:

```
http://localhost:5000
```

---

### **2. Iniciar o MySQL pelo XAMPP**

1. Abra o XAMPP Control Panel
2. Ative:

   * **Apache**
   * **MySQL**
3. Acesse phpMyAdmin
4. Importe o script SQL localizado na pasta `/database`

---

### **3. Abrir o frontend**

Como os arquivos estão na pasta `templates/`, basta abrir o HTML principal no navegador (ou servir via Flask, caso configurado).

---

## 📦 Objetivo do Projeto

O foco é demonstrar:

* **Integração completa** entre API Python + Frontend + Banco
* **Fluxo real de loja virtual**
* **Modelagem de dados profissional**
* **Aplicação prática do Flask com MySQL**

---

## 📧 Contato e Contribuição

Pull Requests são sempre bem-vindos!
Se desejar sugerir melhorias ou relatar problemas, utilize as *Issues* do repositório.

---
