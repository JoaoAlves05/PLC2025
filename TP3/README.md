# PLC2025 - TP3 (Analisador Léxico)

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

## 📋 Resumo

Este trabalho prático implementa um **analisador léxico** para o SPARQL, utilizando **Python e PLY**.  
O lexer reconhece os principais elementos da linguagem, incluindo:

- Variáveis (`?nome`, `?desc`, etc.)  
- Nomes com prefixo (`dbo:MusicalArtist`, `foaf:name`, etc.)  
- Strings (`"Chuck Berry"@en`)  
- Números (`1000`)  
- Palavras-chave reservadas (`SELECT`, `WHERE`, `LIMIT`, `a`)  
- Símbolos (`{`, `}`, `.`)  

O programa lê a query **diretamente do stdin**, permitindo correr, por exemplo:

```bash
cat query.txt | python3 tp3.py
```

## 📂 Lista de Resultados

| Item | Descrição | Link |
|:---:|:---|:---:|
| **📄 Input** | Query SPARQL de exemplo | [🔗 Ver ficheiro](./query.txt) |
| **📄 Solução** | Analisador Léxico | [🔗 Ver Solução](./tp3.py) |

---

<div align="center">

*📚 Trabalho Prático 3 · Processamento de Linguagens e Compiladores · 2025*

</div>