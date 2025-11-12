# PLC2025 - TP4 (Máquina de Vending)

![Ano Letivo](https://img.shields.io/badge/Ano%20Letivo-2025-green)
![UC](https://img.shields.io/badge/UC-PLC-orange)

## 👤 Autor

**João Alves**  
**ID:** A108653

[Foto de João Alves]

## Descrição Geral

Este programa simula o funcionamento de uma **máquina de vending automática**, implementada em **Python** com o auxílio da biblioteca **PLY** para análise léxica.
A máquina aceita comandos escritos pelo utilizador e responde na hora, distinguindo dois modos de funcionamento:

* **Modo Cliente** — utilizado por qualquer utilizador comum.
* **Modo Administrador** — acessível apenas mediante um código especial (por defeito: `1234`).

O stock de produtos é mantido num ficheiro **[stock.json](./stock.json)**, que é carregado e gravado automaticamente sempre que a máquina é utilizada.

---

## Funcionalidades

### Modo Cliente

| Comando               | Descrição                                                                        |
| --------------------- | -------------------------------------------------------------------------------- |
| `LISTAR`              | Lista todos os produtos disponíveis na máquina (com quantidades e preços).       |
| `MOEDA <valores>`     | Insere moedas (ex: `MOEDA 1e 50c 20c`). O programa soma automaticamente o saldo. |
| `SELECIONAR <código>` | Permite comprar um produto, se houver stock e saldo suficiente.                  |
| `SALDO`               | Mostra o saldo atual do utilizador.                                              |
| `HELP`                | Mostra a lista de comandos disponíveis.                                          |
| `SAIR`                | Termina o programa, devolvendo o troco.                                          |

---

### Modo Administrador

Para entrar no modo administrador:

```bash
>> ADMIN
maq: Insira código de administrador: 1234
maq: Modo administrador ativado.
```

| Comando                                  | Descrição                                                               |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| `ADICIONAR <cod> <nome> <quant> <preço>` | Adiciona ou atualiza um produto (ex: `ADICIONAR B20 CocaCola 10 1.50`). |
| `REMOVER <cod>`                          | Remove um produto pelo código.                                          |
| `ALTERAR_PRECO <cod> <preço>`            | Atualiza o preço de um produto.                                         |
| `STATUS`                                 | Mostra produtos com stock baixo (≤ 2 unidades).                         |
| `RESET`                                  | Apaga completamente o stock.                                            |
| `CLIENT`                                 | Sai do modo administrador e volta ao modo cliente.                      |

---

## Estrutura de Dados

O stock é armazenado num ficheiro `stock.json` no formato:

```json
[
    {"cod": "A23", "nome": "Água 0.5L", "quant": 8, "preco": 0.70},
    {"cod": "B10", "nome": "Sumo Laranja", "quant": 5, "preco": 1.20}
]
```

O programa lê e grava automaticamente este ficheiro, garantindo **persistência entre execuções**.

---

## Moedas Aceites

| Símbolo | Valor (€) |
| ------- | --------- |
| `2e`    | 2.00      |
| `1e`    | 1.00      |
| `50c`   | 0.50      |
| `20c`   | 0.20      |
| `10c`   | 0.10      |
| `5c`    | 0.05      |
| `2c`    | 0.02      |
| `1c`    | 0.01      |

Exemplo:

```text
>> MOEDA 1e 50c 20c 5c
maq: Inseriu 1e (1.00€)
maq: Inseriu 50c (0.50€)
maq: Inseriu 20c (0.20€)
maq: Inseriu 5c (0.05€)
maq: Total inserido: 1.75€
maq: Saldo atual = 1e75c
```

---

## Tokens do Lexer

O programa usa **PLY** para reconhecer e processar comandos.
Os tokens definidos são:

```text
LISTAR, MOEDA, SELECIONAR, SALDO, STATUS,
ADICIONAR, REMOVER, RESET, ALTERAR_PRECO,
ADMIN, CLIENT, SAIR, HELP,
CODIGO, VALOR, NOME, NUMERO
```

Cada comando é identificado automaticamente através de expressões regulares, o que permite:

* Reconhecer nomes de produtos, códigos (`A01`, `B12`, …)
* Identificar moedas (`1e`, `50c`, …)
* Ignorar caracteres como espaços, vírgulas e pontos.

---

## Exemplo de Execução

```text
maq: Bom dia! Estou disponível para atender o seu pedido.
maq: Digite HELP para ver os comandos disponíveis.

>> LISTAR
maq:
cod | nome                 | quant | preço
--------------------------------------------
A11 | Água com gás 0.5L    |     6 |  0.80€
B12 | Coca-Cola lata 330ml |    10 |  1.30€
C05 | Batatas fritas       |     3 |  1.00€
--------------------------------------------

>> MOEDA 2e
maq: Inseriu 2e (2.00€)
maq: Saldo atual = 2e

>> SELECIONAR B12
maq: Pode retirar o produto dispensado "Coca-Cola lata 330ml"
maq: Saldo restante = 70c

>> ADMIN
maq: Insira código de administrador: 1234
maq: Modo administrador ativado.

>> ADICIONAR A15 Pepsi 33cl 7 1.20
maq: Produto 'Pepsi 33cl' adicionado com sucesso.

>> REMOVER A11
maq: Produto 'Água com gás 0.5L' (A11) removido com sucesso.

>> CLIENT
maq: Modo cliente ativado. Permissões de administrador revogadas.

>> SAIR
maq: Pode retirar o troco: 3x 20c, 1x 10c.
maq: Até à próxima!
```

---

## Estrutura Interna

O ficheiro principal contém:

* **Classe `VendingMachine`** — responsável por:

  * Gestão do stock (carregar, gravar, adicionar, remover, alterar)
  * Processamento de saldo e moedas
  * Gestão dos modos cliente e admin
  * Execução e interpretação dos comandos do utilizador

* **Analisador léxico (PLY)** — define e reconhece todos os comandos e argumentos válidos.

## 📂 Lista de Resultados

| Item | Descrição | Link |
|:---:|:---|:---:|
| **📄 Stock** | Ficheiro JSON do stock | [🔗 Ver ficheiro](./stock.json) |
| **📄 Solução** | Máquina de Vending | [🔗 Ver Solução](./maq_vending.py) |

---

### 📚 Trabalho Prático 4 · Processamento de Linguagens e Compiladores · 2025
