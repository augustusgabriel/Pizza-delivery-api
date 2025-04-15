# 🍕 PIZZA DELIVERY API

Este é um projeto de API REST para gerenciamento de pedidos de pizzaria, desenvolvido com **FastAPI**, **SQLAlchemy**, **Docker** e **PostgreSQL**. Criado com foco em aprendizado, boas práticas de desenvolvimento e estrutura de API escalável.

---

## 📌 Tecnologias utilizadas

- FastAPI

- SQLAlchemy

- PostgreSQL

- Pydantic

- Uvicorn

---

## 🚀 Funcionalidades

- Cadastro e login de usuários
- Realização de pedidos
- Atualização e cancelamento de pedidos
- Diferenciação de permissões (usuário comum e superusuário)
- Documentação automática com Swagger

---

## 📦 Rotas Implementadas

| Método | Rota                                   | Funcionalidade                        | Acesso       |
|--------|----------------------------------------|---------------------------------------|--------------|
| POST   | `/auth/signup/`                        | Registro de novo usuário              | Público      |
| POST   | `/auth/login/`                         | Login do usuário                      | Público      |
| POST   | `/orders/order/`                       | Criar novo pedido                     | Autenticado  |
| PUT    | `/orders/order/update/{order_id}/`     | Atualizar um pedido                   | Autenticado  |
| PUT    | `/orders/order/status/{order_id}/`     | Atualizar status de um pedido         | Superuser    |
| DELETE | `/orders/order/delete/{order_id}/`     | Remover um pedido                     | Autenticado  |
| GET    | `/orders/user/orders/`                 | Listar pedidos do usuário             | Autenticado  |
| GET    | `/orders/orders/`                      | Listar todos os pedidos               | Superuser    |
| GET    | `/orders/orders/{order_id}/`           | Detalhar um pedido específico         | Superuser    |
| GET    | `/orders/user/order/{order_id}/`       | Detalhar pedido específico do usuário | Autenticado  |
| GET    | `/docs/`                               | Acessar a documentação da API         | Público      |

---

## 🛠️ Como rodar o projeto

### Pré-requisitos

- [Python 3.10+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)

---

### 🔧 Passos para rodar localmente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/augustusgabriel/Pizza-delivery-api.git
   cd Pizza-delivery-api
   ```
2. **Crie e ative o ambiente virtual:**

    ```
    python -m venv venv
    source venv/bin/activate    # Linux/Mac
    venv\Scripts\activate       # Windows
    ```
3. **Instale as dependências:**

    ```
    pip install -r requirements.txt
    ```

4. **Configure a conexão com o banco de dados:**

    No arquivo `database.py`, edite a URI da seguinte forma:

    ```
    engine = create_engine(
        'postgresql://postgres:<username>:<password>@localhost/<database>',
        echo=True
    )
    ```

5. **Crie as tabelas no banco de dados:**

    ```
    python init_db.py
    ```

6. **Execute a aplicação:**

    ```
    uvicorn main:app --reload
    ```

🧪 **Teste a API**

Acesse a documentação interativa via Swagger em:
http://localhost:8000/docs
