---
titulo: Resumo executivo de documento longo
categoria: produtividade
descricao: Transforma um documento longo em decisão, separando o que muda o seu dia do que é só contexto.
ferramentas: [Claude, ChatGPT]
nivel: iniciante
tags: [resumo, leitura, estudo, decisao]
atualizado: 2026-07-29
---

# Resumo executivo de documento longo

Resumo comum devolve uma versão menor do texto, o que raramente ajuda. O que
você quer saber é o que fazer com aquilo. Este prompt força o corte entre
informação acionável e contexto.

Serve para contrato, relatório, artigo científico, transcrição de reunião e
material de curso.

## O prompt

```
Leia o documento abaixo e produza um resumo executivo.

Meu papel: {SEU_PAPEL}
Por que estou lendo isto: {OBJETIVO}

Entregue nesta ordem:

1. Em uma frase
A ideia central do documento, como se você tivesse dez segundos para explicar.

2. O que muda para mim
No máximo cinco pontos que afetam diretamente uma decisão, ação ou risco meu.
Se algo não afeta, não entra aqui.

3. Números e prazos
Todo dado, valor, data e prazo relevante, em lista. Se não houver, escreva
"nenhum".

4. O que ficou em aberto
Perguntas que o documento não responde e que eu precisaria responder antes de
decidir.

5. Se eu só ler um trecho
Indique a parte do documento que eu deveria ler na íntegra, e por quê.

Regras:
- Não repita o documento com outras palavras.
- Não invente nada que não esteja no texto.
- Se algo for ambíguo no original, diga que é ambíguo em vez de escolher uma
  interpretação.

Documento:
{COLE_O_DOCUMENTO}
```

## O que trocar

- `{SEU_PAPEL}`: por exemplo "sou o responsável por aprovar este contrato" ou
  "sou aluno e vou ser cobrado sobre isso numa prova".
- `{OBJETIVO}`: decidir, estudar, apresentar para alguém, checar risco.
- `{COLE_O_DOCUMENTO}`: o texto, ou anexe o arquivo e apague esta linha.

## Dicas

- O campo do papel é o que muda mais o resultado. O mesmo relatório resumido
  para um advogado e para um vendedor deveria sair diferente.
- A seção "o que ficou em aberto" costuma ser a mais útil, e é justamente a
  que nenhum resumo tradicional entrega.
- Para documentos muito longos, peça primeiro um índice comentado e depois o
  resumo só das partes que interessam.
