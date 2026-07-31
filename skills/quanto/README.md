# Raio-x de contexto

Mostra quanto do seu contexto o Claude Code já gastou antes de você digitar a primeira palavra, e de onde vem esse gasto.

Você não paga esse custo uma vez por sessão. Você paga em **toda mensagem**.

## O problema

Todo turno da conversa reenvia o mesmo bloco fixo:

- o CLAUDE.md global, o do projeto e tudo que eles importam com `@`
- o nome e a description de **cada** skill instalada, usada ou não
- o texto que os hooks de `SessionStart` e `UserPromptSubmit` injetam
- as descriptions dos subagentes em `.claude/agents/`
- os schemas das ferramentas de cada servidor MCP conectado

Ninguém instala uma skill pensando "isso vai custar 200 tokens por mensagem pelo resto da vida". Mas custa. Com dezenas de skills instaladas, a conta aparece.

## Instalação

1. Baixe a pasta `quanto`.
2. Copie ela para `~/.claude/skills/` no seu computador.
3. Abra o Claude Code e peça `/quanto`.

O passo a passo completo, com print, está em
[Como instalar skills](../../guias/como-instalar-skills.md).

Opcional, para contagem mais precisa: `pip install tiktoken`. Sem ele o script cai para estimativa por caracteres e avisa isso na saída.

## Como usar

No Claude Code:

```
/quanto
```

Ou direto no terminal, sem passar pelo Claude:

```bash
python3 ~/.claude/skills/quanto/scripts/raio_x.py
```

## Exemplo de saída

```
RAIO-X DE CONTEXTO   janela 200.000 tokens
método: tiktoken o200k_base (+/- 10%)

CUSTO FIXO, COBRADO EM TODA MENSAGEM
  Skills (listagem)        6.786 tok   3.39%  #####...............  96 instaladas
  Hooks (injeção)            947 tok   0.47%  #...................  5 medidos
  CLAUDE.md + imports        898 tok   0.45%  #...................  2 arquivos
  Agents                       0 tok   0.00%  ....................  0 definidos
  --------------------------------------------------------------------
  TOTAL MEDIDO             8.631 tok   4.32%

  Sobra para trabalho: 191.369 tokens

TOP 8 QUE MAIS PESAM
  1. hook SessionStart: CLAUDE_PLUGIN_ROOT=/opt/homebrew/   849 tok
  2. md CLAUDE.md global                                    672 tok
  ...

ONDE CORTAR
  12 skills com description acima de 90 tokens. Encurtar cada
  uma para uma linha de gatilhos devolve cerca de 817 tok por mensagem.
```

Esses 8.631 tokens são reenviados a cada mensagem. Numa conversa de 50 turnos, são 431 mil tokens gastos repetindo a mesma coisa.

## Flags

| Flag | Para quê |
|---|---|
| `--janela 1000000` | Janela do modelo em uso. O padrão é 200000. |
| `--medir-hooks` | Executa os hooks de injeção para medir o que eles inserem. Sem isso ficam indeterminados. |
| `--top 15` | Tamanho do ranking. |
| `--json` | Saída estruturada, para comparar antes e depois. |
| `--cwd CAMINHO` | Mede o setup de outro projeto. |

`--medir-hooks` executa os seus hooks de verdade. Se algum deles tiver efeito colateral, saiba disso antes de usar.

## Os 7 desperdícios de contexto

O que o raio-x costuma encontrar, em ordem de retorno:

**1. Skill instalada e nunca usada.** Custa description em toda mensagem, para sempre. É o corte mais limpo que existe, porque não muda nada no seu fluxo. Desinstale.

**2. Description escrita como documentação.** A description existe para o modelo decidir *quando* carregar a skill. Três frases explicando o que ela faz por dentro é texto que você paga sempre para ler nunca. Uma linha de gatilhos resolve.

**3. CLAUDE.md como manual.** CLAUDE.md é para regra permanente, que vale em toda mensagem. Procedimento que só importa em uma situação específica custa menos como skill, carregada sob demanda.

**4. Hook de `UserPromptSubmit` falante.** É o pior caso possível: reinjeta o texto a cada mensagem sua. Um hook de 800 tokens em uma conversa de 50 turnos são 40 mil tokens gastos repetindo a mesma coisa.

**5. MCP conectado e não usado.** Cada servidor expõe schemas de ferramentas. Se as tools não forem carregadas sob demanda, você paga o catálogo inteiro para usar zero.

**6. Releitura.** Ler de novo um arquivo que já está no contexto duplica o custo dele. É o desperdício mais comum em sessão longa, e o raio-x não mede: só disciplina resolve.

**7. Retrabalho por objetivo vago.** O mais caro de todos, e o único que não aparece em métrica nenhuma. Uma tarefa mal especificada custa a execução inteira, mais a correção. Vale mais que os seis anteriores somados.

## Limitações, ditas na cara

- A contagem usa `tiktoken`, que **não** é o tokenizador da Anthropic. Trate como ordem de grandeza confiável, com margem declarada de dez por cento, não como fatura.
- MCP aparece como **indeterminado** de propósito. O custo real depende de quantas tools o servidor expõe e de estarem diferidas ou não, e isso não é auditável em disco. Chutar aqui seria mais fácil e menos honesto.
- Mede o custo **fixo** do setup. Não mede a conversa nem o resultado das ferramentas, que numa sessão longa costuma ser a maior fatia de todas.
- Diagnóstico apenas. Não altera nada no seu setup.

---

Voltar para [todas as skills](../README.md).
