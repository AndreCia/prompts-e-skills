# 10 skills úteis para o Claude

As 10 skills do reel, com o link de cada uma e o jeito mais rápido de instalar.
Todas são gratuitas e de código aberto. O crédito é de quem criou: esta página
só reúne os links, não copia o código de ninguém.

| # | Skill | O que faz | Autor |
|---|---|---|---|
| 1 | [humanizer](https://github.com/blader/humanizer) | Tira a cara de IA dos seus textos | blader |
| 2 | [copywriting](https://github.com/coreyhaines31/marketingskills/tree/main/skills/copywriting) | Escreve a sua página de vendas | Corey Haines |
| 3 | [lead-magnets](https://github.com/coreyhaines31/marketingskills/tree/main/skills/lead-magnets) | Cria o material gratuito que capta contatos | Corey Haines |
| 4 | [offers](https://github.com/coreyhaines31/marketingskills/tree/main/skills/offers) | Monta uma oferta que o cliente não consegue recusar | Corey Haines |
| 5 | [ads](https://github.com/coreyhaines31/marketingskills/tree/main/skills/ads) | Planeja os seus anúncios no Meta e no Google | Corey Haines |
| 6 | [prospecting](https://github.com/coreyhaines31/marketingskills/tree/main/skills/prospecting) | Encontra clientes para você abordar | Corey Haines |
| 7 | [competitor-profiling](https://github.com/coreyhaines31/marketingskills/tree/main/skills/competitor-profiling) | Faz o raio-x completo dos seus concorrentes | Corey Haines |
| 8 | [last30days](https://github.com/mvanhorn/last30days-skill) | Descobre o que estão falando de qualquer assunto nos últimos 30 dias | mvanhorn |
| 9 | [mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | Conecta o Claude ao sistema que você já usa | Anthropic |
| 10 | [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Cria a sua própria skill | Anthropic |

---

## Instalação em um passo

Abra o Claude Code, cole o prompt abaixo e aperte enter. Ele instala as 10
para você.

```
Instale estas 10 skills no meu Claude Code, valendo para todos os projetos.

1. Confira se o Node.js está instalado (node --version). Se não estiver,
   me avise e me ajude a instalar antes de seguir.
2. Veja se em ~/.claude/skills já existe alguma pasta com um destes nomes:
   humanizer, copywriting, lead-magnets, offers, ads, prospecting,
   competitor-profiling, last30days, mcp-builder, skill-creator.
   Se existir, pare e me pergunte antes de substituir.
3. Rode estes quatro comandos, um por vez:

   npx -y skills add blader/humanizer -g -a claude-code -y
   npx -y skills add coreyhaines31/marketingskills --skill copywriting lead-magnets offers ads prospecting competitor-profiling -g -a claude-code -y
   npx -y skills add mvanhorn/last30days-skill -g -a claude-code -y
   npx -y skills add anthropics/skills --skill mcp-builder skill-creator -g -a claude-code -y

4. Confira se as 10 pastas estão em ~/.claude/skills, cada uma com um
   SKILL.md dentro.
5. Confira se o Python 3.12 ou mais novo está instalado (python3 --version),
   porque a last30days precisa dele. Se não estiver, só me avise.
6. Me diga quais entraram e quais falharam, e me lembre de reiniciar o
   Claude Code.
```

### Instalação pelo terminal

Se preferir rodar você mesmo, precisa do [Node.js](https://nodejs.org)
instalado. Cole no terminal:

```bash
npx -y skills add blader/humanizer -g -a claude-code -y
npx -y skills add coreyhaines31/marketingskills --skill copywriting lead-magnets offers ads prospecting competitor-profiling -g -a claude-code -y
npx -y skills add mvanhorn/last30days-skill -g -a claude-code -y
npx -y skills add anthropics/skills --skill mcp-builder skill-creator -g -a claude-code -y
```

Depois, feche e abra o Claude Code.

Usa outro agente, como Codex ou Cursor? Troque `claude-code` pelo nome dele,
por exemplo `-a codex`.

### Instalação manual

Abra o link de cada skill na tabela, baixe a pasta e copie para
`~/.claude/skills/`. O passo a passo com print está em
[Como instalar skills](../../guias/como-instalar-skills.md).

---

## Como usar

Digite `/` seguido do nome da skill, por exemplo `/offers`, ou só descreva o
que você quer. A skill certa dispara sozinha.

Exemplos:

- "Tira a cara de IA deste texto" chama a **humanizer**.
- "Monta a oferta do meu curso de confeitaria" chama a **offers**.
- "O que estão falando do Claude Code nos últimos 30 dias?" chama a **last30days**.

---

## Bom saber

- **last30days:** precisa do Python 3.12 ou mais novo. Reddit, arXiv e
  Techmeme funcionam de graça e sem chave. Algumas outras fontes pedem
  configuração, e a própria skill explica como na primeira vez.
- **Skills de marketing (2 a 7):** rendem mais quando você conta para o Claude
  o seu produto, o seu público e o seu preço logo no começo.
- **Segurança:** skill roda no seu computador. Todas estas são públicas e
  populares no GitHub, mas vale o hábito de olhar o `SKILL.md` antes de
  instalar qualquer skill de terceiros.

---

Skills novas toda semana no Instagram:
[@ciaandre](https://instagram.com/ciaandre).

Voltar para a [lista de skills](../README.md).
