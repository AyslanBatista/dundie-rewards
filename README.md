# Projeto Dundie Rewards

[![CI](https://github.com/AyslanBatista/dundie-rewards/actions/workflows/main.yml/badge.svg)](https://github.com/AyslanBatista/dundie-rewards/actions/workflows/main.yml) [![codecov](https://codecov.io/gh/AyslanBatista/dundie-rewards/branch/main/graph/badge.svg?token=5XYHAT14V0)](https://codecov.io/gh/AyslanBatista/dundie-rewards)

Nós fomos contratados pela Dunder Mifflin, grande fabricante de papéis para desenvolver um sistema
de recompensas para seus colaboradores.

Michael, o gerente da empresa quer aumentar a motivação dos funcionários oferecendo um sistema
de pontos que os funcionários podem acumular de acordo com as suas metas atingidas, bonus oferecidos
pelo gerente e os funcionários podem também trocam pontos entre sí.

O funcionário pode uma vez a cada ano resgatar seus pontos em um cartão de crédito para gastar onde
quiserem.

Acordamos em contrato que o MVP (Minimum Viable Product) será uma versão para ser executada no terminal
e que no futuro terá também as interfaces UI, web e API.

Os dados dos funcionários atuais serão fornecidos em um arquivo que pode ser no formato .csv ou .json
e este mesmo arquivo poderá ser usado para versões futuras. `Nome, Depto, Cargo, Email`


## Installation

```py
pip install seunome-dundie
```

```py
pip install -e `.[dev]`
```

## Login
- Exportando variáveis
```bash
export DUNDIE_USER=email
export DUNDIE_PASSWORD=password
```


#### OU

- Inserindo seu usuário e senha ao executar um comando
```bash
dundie show
```
```bash

 ⚠  [WARNING] You need to be logged in to access this function.

Please enter the email and then the password.

👤 Email: email
🔒 Password: password

✅ [AUTHORIZED] You are logged into the account 'email'.
```

## Comandos Administrador
- Comando `dundie show` logado como administrador tem acesso a ver todos os usuários.
```bash
dundie load assets/people.csv
```
```bash
dundie add 65 --dept=Sales
dundie add 100 --email=jim@dundlermifflin.com
```
```bash
dundie remove 65 --dept=Sales
dundie remove 100 --email=jim@dundlermifflin.com
```

![](./assets/Administrador.gif)

## Comandos Funcionário
```bash
dundie show
```
```bash
dundie transfer 100 --email=jim@dundlermifflin.com
```
```bash
dundie movements
```
![](./assets/funcionario.gif)
