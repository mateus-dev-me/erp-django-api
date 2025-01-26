# Sistema ERP API
[![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/release)
[![Django Version](https://img.shields.io/badge/Django-4.2%2B-green)](https://docs.djangoproject.com/en/stable/releases/)

Este é um projeto pessoal de desenvolvimento de uma **API para um sistema ERP** utilizando **Django Rest Framework** (DRF). O sistema ERP tem como objetivo gerenciar e automatizar diversos processos de uma empresa, incluindo o controle de usuários, funcionários, permissões, tarefas, contas a pagar e a receber.

## Funcionalidades Implementadas

Atualmente, o sistema está em desenvolvimento e possui as seguintes funcionalidades implementadas:

- **Gerenciamento de Usuários**: Cadastro, edição e exclusão de usuários.
- **Gestão de Funcionários**: Registro e controle de informações dos funcionários.
- **Controle de Grupos e Permissões**: Gerenciamento de grupos de usuários e suas permissões de acesso.
- **Controle de Tarefas**: Cadastro e controle de tarefas a serem executadas dentro da empresa.

**Em breve** serão implementadas as funcionalidades de **contas a pagar e a receber**, incluindo a geração de tarefas recorrentes, que serão automatizadas com o **Celery**.

## Tecnologias Utilizadas

- **Django**: Framework principal para o desenvolvimento da API.
- **Django Rest Framework (DRF)**: Para facilitar a criação de APIs RESTful.
- **Celery**: Utilizado para automação de tarefas recorrentes.
- **PostgreSQL**: Banco de dados relacional utilizado para persistência de dados.
- **pytest**: Ferramenta de testes automatizados para garantir a qualidade do código.
- **Docker**: Para gerenciamento do ambiente de desenvolvimento e produção.
- **Poetry**: Gerenciador de pacotes para o gerenciamento de dependências e ambiente virtual.


## Contribuições

Contribuições são bem-vindas! Se você tiver sugestões ou melhorias para o projeto, sinta-se à vontade para abrir uma **issue** ou enviar um **pull request**.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
