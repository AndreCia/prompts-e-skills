# Convenções da biblioteca

Este arquivo é a fonte da verdade do repositório. Toda automação futura, a
skill `recompensas-git` inclusive, deve ler daqui em vez de carregar o padrão
por conta própria. Mudou a regra, muda neste arquivo, e só neste arquivo.

---

## Nomes

- Pastas e arquivos em `kebab-case`, sem acento, sem espaço, sem maiúscula.
  Certo: `roteiro-de-reels-30s.md`. Errado: `Roteiro de Reels 30s.md`.
- O nome do arquivo descreve o resultado, não a técnica.
  Certo: `headlines-de-anuncio.md`. Errado: `prompt-few-shot-3.md`.
- Máximo de dois níveis de pasta a partir da raiz. Navegação no celular
  quebra além disso, e a maior parte do público chega pelo Instagram.

---

## Categorias válidas

Toda categoria nova exige uma pasta, um `README.md` de índice e uma linha na
tabela do `README.md` da raiz.

| Slug | Nome exibido |
|---|---|
| `imagens` | Imagens |
| `copy-e-vendas` | Copy e vendas |
| `texto-e-conteudo` | Texto e conteúdo |
| `produtividade` | Produtividade |
| `negocios` | Negócios |

---

## Frontmatter obrigatório dos prompts

Todo arquivo em `prompts/` começa com este bloco:

```yaml
---
titulo: Título em linguagem humana
categoria: imagens
subsecao: Criando sua identidade visual
descricao: Uma linha dizendo o que o prompt entrega, sem enrolação.
ferramentas: [Claude, ChatGPT, Midjourney]
nivel: iniciante
tags: [retrato, fotografia]
atualizado: 2026-07-29
---
```

Regras dos campos:

- `categoria` precisa ser um slug da tabela acima.
- `subsecao` é opcional e não cria pasta. Ela vira um agrupamento com título
  dentro do índice da categoria. É assim que se organiza um tema sem
  aprofundar a árvore de pastas.
- `nivel` aceita `iniciante`, `intermediario` ou `avancado`.
- `atualizado` no formato `AAAA-MM-DD`, sempre atualizado quando o conteúdo
  do prompt mudar de verdade. Correção de vírgula não conta.
- `descricao` é o que aparece nos índices. Escreva pensando em quem está
  passando o olho no celular.

---

## Estrutura do corpo de um prompt

Na ordem, sem inventar seções novas:

1. `# Título`
2. Um parágrafo curto de contexto: quando usar isso.
3. `## O prompt`, com o texto dentro de um bloco de código. Bloco de código é
   obrigatório, porque é o que ativa o botão de copiar do GitHub.
4. `## O que trocar`, listando cada variável `ENTRE_CHAVES` e o que colocar.
   Quando o prompt não tem variável nenhuma, troque esta seção por
   `## Como usar` e descreva o que o prompt exige para funcionar, como enviar
   uma imagem junto ou rodar em uma ferramenta específica. Seção vazia é pior
   que seção adaptada.
5. `## Dicas`, opcional, com ajustes e variações.
6. `## Exemplo de resultado`, opcional.

Variáveis sempre em maiúsculas entre chaves: `{PUBLICO_ALVO}`, `{PRODUTO}`.

Imagens de exemplo vão em `assets/`, em JPG, com no máximo 400 KB e largura
de 1000 a 1200 pixels. Comprima antes de versionar, porque imagem pesada fica
no histórico do git para sempre:

```bash
sips -s format jpeg -s formatOptions 68 --resampleWidth 1000 entrada.png --out assets/saida.jpg
```

---

## Índices

- Cada pasta de categoria tem um `README.md` com uma tabela de prompts.
- A tabela tem as colunas: Prompt, O que faz, Nível.
- O `README.md` da raiz nunca lista prompts individuais, só categorias. Ele é
  a vitrine, não o catálogo.
- Índices são gerados a partir do frontmatter, nunca editados à mão. Editar à
  mão é como a inconsistência entra.

O bloco gerado fica entre estes marcadores, e só ele é reescrito. Tudo que
estiver fora deles é preservado:

```markdown
<!-- INICIO_INDICE -->
<!-- FIM_INDICE -->
```

Para regenerar:

```bash
python3 ~/.claude/skills/recompensa-git/scripts/catalogo.py indices
python3 ~/.claude/skills/recompensa-git/scripts/catalogo.py validar
```

---

## Skills

Cada skill vive em `skills/nome-da-skill/` e contém:

- `SKILL.md` com o frontmatter de skill (`name`, `description`).
- `README.md` explicando em português o que ela faz e como instalar.
- `scripts/`, opcional, para a parte mecânica.

---

## Publicação

- Toda adição atualiza o `CHANGELOG.md`, com data no formato `DD/MM/AAAA`.
- Commit em português, no imperativo: `adiciona prompt de headlines`.
- Nada de push automático sem revisão do diff. O repositório é público.
- Nunca versionar chave de API, token, link de afiliado disfarçado ou
  material de terceiros sem crédito.

Antes de escrever qualquer arquivo, e de novo antes do commit, rode a
varredura de dados sensíveis:

```bash
python3 ~/.claude/skills/recompensa-git/scripts/seguranca.py --texto ARQUIVO
python3 ~/.claude/skills/recompensa-git/scripts/seguranca.py --staged
```

Saída `2` significa parar. Saída `1` exige conferência item a item. O
repositório é público e o histórico do git é permanente, então apagar um
segredo no commit seguinte não desfaz o vazamento. Nesse caso a única ação
que resolve é revogar a credencial no provedor.

---

## Escrita

- Português brasileiro, com acentuação e pontuação corretas.
- Sem travessões.
- Linguagem direta. O leitor está no celular, com pouca paciência.
