# Como instalar skills

Skills funcionam no **Claude Code**. Se você usa só o Claude pelo navegador,
elas não se aplicam, mas os [prompts](../prompts/) funcionam em qualquer IA.

---

## O que é uma skill

Um prompt você cola toda vez. Uma skill fica instalada e dispara sozinha
quando você descreve a situação. É a diferença entre lembrar do procedimento e
ter o procedimento pronto.

---

## Instalação

### Passo 1, baixe o material

Clique no botão verde **Code** no topo da página inicial e depois em
**Download ZIP**. Descompacte.

### Passo 2, encontre a pasta de skills

No Mac, abra o Finder e pressione `Cmd + Shift + G`. Cole:

```
~/.claude/skills
```

Se a pasta não existir, crie uma pasta chamada `skills` dentro de `.claude`.

No Windows, o caminho é `C:\Users\SEU_USUARIO\.claude\skills`.

### Passo 3, copie a skill

Copie a pasta da skill inteira, com o `SKILL.md` dentro, para lá. O resultado
deve ficar assim:

```
~/.claude/skills/
└── organizador-de-links/
    ├── SKILL.md
    └── README.md
```

Um erro comum é copiar só o arquivo `SKILL.md` solto. A pasta precisa ir junto.

### Passo 4, reinicie o Claude Code

Feche e abra de novo. Para conferir se deu certo, digite `/` e procure o nome
da skill na lista.

---

## Como usar

Você não precisa chamar a skill pelo nome. Descreva o que quer, com as suas
palavras, e ela dispara sozinha. Cada skill tem um arquivo `README.md` com os
exemplos de frase que a ativam.

Se preferir chamar direto, digite `/` seguido do nome dela.

---

## Se não funcionar

- Confira se o arquivo se chama exatamente `SKILL.md`, em maiúsculas.
- Confira se a pasta está em `~/.claude/skills/` e não solta em outro lugar.
- Reinicie o Claude Code, não só a janela do terminal.
- Descreva a situação em vez de dar uma ordem genérica. Skills disparam por
  contexto.

---

Skills novas toda semana no Instagram:
[@ciaandre](https://instagram.com/ciaandre).

Voltar para a [página inicial](../README.md).
