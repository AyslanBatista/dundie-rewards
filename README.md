<p align="center">
  <a href="https://github.com/AyslanBatista/dundie-rewards"><img src="https://m.media-amazon.com/images/I/51bb-MYLnNL._SX342_SY445_.jpg" alt="DundieRewards"></a>
</p>
<p align="center">
<a href="https://github.com/AyslanBatista/dundie-rewards/actions/workflows/main.yml" target="_blank">
    <img src="https://github.com/AyslanBatista/dundie-rewards/actions/workflows/main.yml/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/AyslanBatista/dundie-rewards" target="_blank">
    <img src="https://codecov.io/gh/AyslanBatista/dundie-rewards/branch/main/graph/badge.svg?token=5XYHAT14V0" alt="Coverage">
</a>
<a href="https://github.com/AyslanBatista/dundie-rewards?tab=Unlicense-1-ov-file#readme" target="_blank">
    <img src="https://img.shields.io/badge/license-MIT-007EC7.svg?color=%2334D058" alt="License">
</a>
</p>

---

# Projeto Dundie Rewards

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


## Instalação

```py
pip install seunome-dundie
```

```py
pip install -e `.[dev]`
```

## Como Logar
- Exportando variáveis
```bash
export DUNDIE_USER=email
export DUNDIE_PASSWORD=password
```


#### OU

- Inserindo seu e-mail e senha ao executar um comando
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

## Como usar
```bash
dundie --help
```
![](./assets/dundie.gif)
