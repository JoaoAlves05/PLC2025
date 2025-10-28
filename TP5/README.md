# PLC2025 - TP5 - Analisador Recursivo-Descendente de Expressões Aritméticas

<div align="center">

![Ano Letivo](https://img.shields.io/badge/Ano%20Letivo-2025-green)
![UC](https://img.shields.io/badge/UC-PLC-orange)

</div>

### 👤 Autor

<div align="left">

**João Alves**
**ID:** A108653

<img src="../me.jpg" width="132" height="176" alt="Foto de João Alves" style="border-radius: 8px;">

</div>

---

## Descrição Geral

Este programa analisa **expressões aritméticas** com os operadores `+`, `-`, `*`, `/` e parênteses, utilizando um **analisador recursivo-descendente**.

Foi desenvolvido em **Python**, recorrendo à biblioteca **PLY** para a análise léxica.
O objetivo é mostrar, passo a passo, como uma expressão é processada pela gramática.

---

## Funcionalidade

O programa:

* Lê expressões a partir do **stdin**, usando por exemplo o comando:

  ```bash
  cat testes/input2.txt | python3 tp5.py
  ```
* Mostra as **derivações** e **reconhecimentos** de cada parte da expressão;
* Indica quando a expressão está correta ou contém **erros de sintaxe**.

---

## Gramática Utilizada

```
Expressao  → Termo OprSomSub
OprSomSub  → (+|-) Termo OprSomSub | ε
Termo      → Fator OprMultDiv
OprMultDiv → (*|/) Fator OprMultDiv | ε
Fator      → NUM | ( Expressao )
```

---

## Ficheiros de Teste

Foram criados **5 ficheiros** dentro do diretório [**testes**](./testes) (`input1.txt` a `input5.txt`) com várias expressões:

| Ficheiro     | Descrição                 |
| ------------ | ------------------------- |
| `input1.txt` | Expressões simples        |
| `input2.txt` | Expressões com parênteses |
| `input3.txt` | Expressões mais longas    |
| `input4.txt` | Erros nos parênteses      |
| `input5.txt` | Erros nos operadores      |

Cada ficheiro contém **2–3 expressões** para testar diferentes situações.

---

## Estrutura Interna

O ficheiro **`tp5.py`** inclui:

* Um **analisador léxico** para identificar números, operadores e parênteses;
* Um **conjunto de funções recursivas** que implementam a gramática;
* Um **módulo principal** que lê as expressões e apresenta o resultado.

---

## 📂 Lista de Resultados

|      Item      | Descrição                        |            Link            |
| :------------: | :------------------------------- | :------------------------: |
| **📄 Solução** | Analisador Recursivo-Descendente | [🔗 Ver Solução](./tp5.py) |
|  **📄 Inputs** | Ficheiros de teste               |  [🔗 Ver Inputs](./testes) |

---

<div align="center">

*📚 Trabalho Prático 5 · Processamento de Linguagens e Compiladores · 2025*

</div>
