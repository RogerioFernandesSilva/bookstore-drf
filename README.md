Bookstore

Projeto Django desenvolvido durante o curso Python Back-End da EBAC (módulo 14).

🛠️ Tecnologias
Python 3.11
Django ^5.1
Django REST Framework — criação da API e dos serializers
Poetry — gerenciador de dependências e ambientes virtuais
📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

Python 3.11+
Poetry

Para verificar se o Poetry está instalado e acessível no terminal:

powershell
poetry --version

Nota (Windows): se o comando não for reconhecido, adicione a pasta C:\Users\<seu_usuario>\AppData\Roaming\Python\Scripts à variável de ambiente PATH do usuário e reinicie o terminal (ou o VS Code inteiro, se estiver usando o terminal integrado).

🚀 Passo a passo do projeto
1. Clonar o repositório
powershell
git clone <url-do-repositorio>
cd bookstore-drf
2. Instalar as dependências

O Poetry lê o arquivo pyproject.toml e instala tudo automaticamente (Django, Django REST Framework e demais dependências), criando um ambiente virtual isolado para o projeto:

powershell
poetry install
3. Rodar as migrações
powershell
poetry run python manage.py migrate
4. Subir o servidor de desenvolvimento powershell
poetry run python manage.py createsuperuser
poetry run python manage.py runserver

Depois disso, o projeto estará disponível em http://127.0.0.1:8000.

5. Rodar os testes automatizados
powershell
poetry run python manage.py test
📦 Modelos da aplicação

A app api possui três entidades principais:

Category — categoria de um produto (nome e descrição).
Product — produto vendido na loja, relacionado a uma Category (ForeignKey).
Order — pedido de compra, relacionado a um Product (ForeignKey), com quantidade, nome do cliente e status.
🔌 Serializers

Cada entidade possui um serializer em api/serializers.py, construído com ModelSerializer:

CategorySerializer — serializa/valida os campos da categoria.
ProductSerializer — exibe a categoria relacionada de forma aninhada (category) e aceita o id da categoria em category_id para criação/edição. Valida preço e estoque.
OrderSerializer — exibe o produto relacionado de forma aninhada (product, que já inclui a categoria) e aceita o id do produto em product_id. Valida a quantidade pedida contra o estoque disponível.
🧪 Testes

Os testes dos serializers ficam em api/tests/, organizados por entidade:

api/tests/
├── __init__.py
├── test_category_serializer.py
├── test_product_serializer.py
└── test_order_serializer.py

Cada arquivo verifica, entre outros pontos:

se dados válidos são aceitos;
se campos obrigatórios são exigidos;
se dados inválidos são rejeitados;
se os campos retornados pelo serializer são os esperados;
se os relacionamentos (Category ↔ Product ↔ Order) são representados corretamente;
se o serializer cria o objeto corretamente com save().

Para rodar apenas os testes da app api:

powershell
poetry run python manage.py test api
📁 Estrutura do projeto
bookstore-drf/
├── api/                     # App com models, serializers e testes
│   ├── migrations/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_category_serializer.py
│   │   ├── test_product_serializer.py
│   │   └── test_order_serializer.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── bookstore/               # Configurações principais do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py                # Utilitário de linha de comando do Django
├── pyproject.toml           # Dependências e configuração do Poetry
└── README.md
💡 Comandos úteis do Poetry
Comando	O que faz
poetry install	Instala todas as dependências do projeto
poetry add <pacote>	Adiciona uma nova dependência
poetry run <comando>	Executa um comando dentro do ambiente virtual do projeto
poetry env activate	Mostra o comando para ativar o ambiente virtual no terminal atual (substitui o antigo poetry shell, removido a partir do Poetry 2.0)
poetry show	Lista as dependências instaladas

Projeto em desenvolvimento como parte do curso EBAC - Python Back-End.
