#!/usr/bin/env python3
"""Raio-X de contexto: mede o custo fixo que seu setup do Claude Code cobra
em TODA mensagem, antes de você digitar qualquer coisa.

Uso:
    python3 raio_x.py [--janela 200000] [--json] [--top 8] [--medir-hooks]

Mede apenas o que é auditável em disco. O que não dá para medir sem
conectar aparece marcado como indeterminado, nunca chutado.
"""

import argparse
import glob
import json
import os
import re
import sys

HOME = os.path.expanduser("~")


# ---------------------------------------------------------------- tokenização
def montar_contador():
    """Retorna (função_contadora, rótulo_do_método, margem_declarada)."""
    try:
        import tiktoken

        enc = tiktoken.get_encoding("o200k_base")
        return (lambda t: len(enc.encode(t, disallowed_special=())),
                "tiktoken o200k_base", "+/- 10%")
    except Exception:
        # Fallback: português acentuado tokeniza mais denso que inglês.
        return (lambda t: int(len(t) / 3.6), "estimativa por caracteres", "+/- 25%")


CONTAR, METODO, MARGEM = montar_contador()


def ler(caminho):
    try:
        with open(caminho, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def carregar_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


# ------------------------------------------------------------------ CLAUDE.md
def medir_claude_md(cwd):
    """CLAUDE.md global, do projeto e ancestrais, seguindo imports @arquivo."""
    itens = []
    vistos = set()

    def adicionar(caminho, rotulo, profundidade=0):
        caminho = os.path.realpath(caminho)
        if caminho in vistos or not os.path.isfile(caminho):
            return
        vistos.add(caminho)
        texto = ler(caminho)
        if not texto.strip():
            return
        itens.append({"nome": rotulo, "tokens": CONTAR(texto)})
        if profundidade >= 3:
            return
        base = os.path.dirname(caminho)
        for imp in re.findall(r"^@([^\s]+)", texto, re.MULTILINE):
            alvo = os.path.expanduser(imp)
            if not os.path.isabs(alvo):
                alvo = os.path.join(base, alvo)
            adicionar(alvo, f"{rotulo} -> @{os.path.basename(alvo)}", profundidade + 1)

    adicionar(f"{HOME}/.claude/CLAUDE.md", "CLAUDE.md global")

    diretorio = os.path.realpath(cwd)
    ancestrais = []
    while True:
        ancestrais.append(diretorio)
        pai = os.path.dirname(diretorio)
        if pai == diretorio or diretorio == HOME:
            break
        diretorio = pai
    for d in reversed(ancestrais):
        for nome in ("CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md"):
            adicionar(os.path.join(d, nome), f"{nome} ({os.path.basename(d) or '/'})")

    return itens


# --------------------------------------------------------------------- skills
def extrair_frontmatter(texto):
    if not texto.startswith("---"):
        return {}
    fim = texto.find("\n---", 3)
    if fim == -1:
        return {}
    campos = {}
    for linha in texto[3:fim].splitlines():
        m = re.match(r"^(name|description):\s*(.*)$", linha.strip())
        if m:
            campos[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return campos


def medir_skills(cwd):
    """Cada skill instalada paga nome + description na listagem de todo turno.
    O corpo do SKILL.md só entra no contexto quando a skill é invocada."""
    caminhos = []
    caminhos += [(p, "pessoal") for p in glob.glob(f"{HOME}/.claude/skills/*/SKILL.md")]
    caminhos += [(p, "plugin") for p in
                 glob.glob(f"{HOME}/.claude/plugins/cache/**/SKILL.md", recursive=True)]
    caminhos += [(p, "projeto") for p in
                 glob.glob(os.path.join(cwd, ".claude/skills/**/SKILL.md"), recursive=True)]

    # O cache de plugins guarda versões antigas lado a lado. Só uma entra na
    # listagem, então deduplicamos por nome e contamos as cópias à parte.
    por_nome, duplicatas = {}, 0
    for caminho, origem in caminhos:
        fm = extrair_frontmatter(ler(caminho))
        nome = fm.get("name") or os.path.basename(os.path.dirname(caminho))
        desc = fm.get("description", "")
        if not desc:
            continue
        item = {
            "nome": nome,
            "origem": origem,
            "tokens": CONTAR(f"- {nome}: {desc}\n"),
            "corpo_tokens": CONTAR(ler(caminho)),
        }
        anterior = por_nome.get(nome)
        if anterior is None:
            por_nome[nome] = item
        else:
            duplicatas += 1
            if item["tokens"] > anterior["tokens"]:
                por_nome[nome] = item
    return list(por_nome.values()), duplicatas


# --------------------------------------------------------------------- agents
def medir_agents(cwd):
    itens = []
    padroes = [f"{HOME}/.claude/agents/*.md", os.path.join(cwd, ".claude/agents/*.md")]
    for padrao in padroes:
        for caminho in glob.glob(padrao):
            fm = extrair_frontmatter(ler(caminho))
            nome = fm.get("name") or os.path.basename(caminho)[:-3]
            desc = fm.get("description", "")
            if desc:
                itens.append({"nome": nome, "tokens": CONTAR(f"- {nome}: {desc}\n")})
    return itens


# ---------------------------------------------------------------------- hooks
LEITURA_PURA = re.compile(r"^\s*(cat|echo|printf)\s")


def executar_hook(cmd, evento, cwd, timeout=15):
    """Roda o hook e mede o texto que ele injeta. Opt-in: hooks podem ter
    efeito colateral, então só acontece com --medir-hooks."""
    import subprocess

    entrada = json.dumps({
        "session_id": "raio-x", "cwd": cwd, "hook_event_name": evento,
        "source": "startup", "transcript_path": "",
    })
    try:
        r = subprocess.run(["bash", "-c", cmd], input=entrada, capture_output=True,
                           text=True, timeout=timeout, cwd=cwd)
    except (subprocess.SubprocessError, OSError):
        return None
    saida = (r.stdout or "").strip()
    if not saida:
        return 0
    try:  # hooks estruturados injetam só o additionalContext
        dados = json.loads(saida)
        especifico = dados.get("hookSpecificOutput", {})
        if "additionalContext" in especifico:
            return CONTAR(str(especifico["additionalContext"]))
    except ValueError:
        pass
    return CONTAR(saida)


def medir_hooks(cwd, executar=False):
    """Só hooks de SessionStart/UserPromptSubmit injetam texto no contexto.
    Medimos os de leitura pura sempre; os demais só com executar=True."""
    medidos, indeterminados, vistos = [], [], set()
    for arquivo in ("settings.json", "settings.local.json"):
        conf = carregar_json(f"{HOME}/.claude/{arquivo}")
        for evento in ("SessionStart", "UserPromptSubmit"):
            for grupo in conf.get("hooks", {}).get(evento, []):
                for hook in grupo.get("hooks", []):
                    cmd = str(hook.get("command", ""))
                    if not cmd or (evento, cmd) in vistos:
                        continue
                    vistos.add((evento, cmd))
                    rotulo = f"{evento}: {cmd.strip().splitlines()[0][:44]}"
                    if LEITURA_PURA.match(cmd):
                        alvos = re.findall(r"(/[^\s'\"]+|~[^\s'\"]+)", cmd)
                        total = sum(CONTAR(ler(os.path.expanduser(a)))
                                    for a in alvos if os.path.isfile(os.path.expanduser(a)))
                        if total:
                            medidos.append({"nome": rotulo, "tokens": total})
                            continue
                    if executar:
                        medido = executar_hook(cmd, evento, cwd)
                        if medido is not None:
                            medidos.append({"nome": rotulo, "tokens": medido})
                            continue
                    indeterminados.append(rotulo)
    return medidos, indeterminados


# ------------------------------------------------------------------------ mcp
def medir_mcp(cwd):
    servidores = {}
    for caminho in (f"{HOME}/.claude/settings.json",
                    f"{HOME}/.claude/settings.local.json",
                    f"{HOME}/.claude.json",
                    os.path.join(cwd, ".mcp.json")):
        conf = carregar_json(caminho)
        for nome in conf.get("mcpServers", {}):
            servidores.setdefault(nome, os.path.basename(caminho))
    conf_global = carregar_json(f"{HOME}/.claude.json")
    for proj, dados in (conf_global.get("projects") or {}).items():
        if os.path.realpath(proj) == os.path.realpath(cwd):
            for nome in (dados.get("mcpServers") or {}):
                servidores.setdefault(nome, "projeto")
    return servidores


# --------------------------------------------------------------------- saida
def barra(fracao, largura=20):
    cheio = max(0, min(largura, round(fracao * largura)))
    return "#" * cheio + "." * (largura - cheio)


def num(valor):
    """Formata no padrão brasileiro: 9.369"""
    return f"{valor:,}".replace(",", ".")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--janela", type=int, default=200000)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--medir-hooks", action="store_true",
                    help="executa os hooks de injeção para medir o que eles inserem")
    ap.add_argument("--cwd", default=os.getcwd())
    args = ap.parse_args()

    cwd = os.path.realpath(args.cwd)
    md = medir_claude_md(cwd)
    skills, duplicatas = medir_skills(cwd)
    agents = medir_agents(cwd)
    hooks, hooks_indef = medir_hooks(cwd, executar=args.medir_hooks)
    mcp = medir_mcp(cwd)

    blocos = [
        ("Skills (listagem)", sum(i["tokens"] for i in skills), f"{len(skills)} instaladas"),
        ("CLAUDE.md + imports", sum(i["tokens"] for i in md), f"{len(md)} arquivos"),
        ("Hooks (injeção)", sum(i["tokens"] for i in hooks), f"{len(hooks)} medidos"),
        ("Agents", sum(i["tokens"] for i in agents), f"{len(agents)} definidos"),
    ]
    total = sum(t for _, t, _ in blocos)

    if args.json:
        print(json.dumps({
            "metodo": METODO, "margem": MARGEM, "janela": args.janela,
            "total_medido": total, "blocos": blocos, "skills": skills,
            "skills_duplicadas_em_disco": duplicatas,
            "claude_md": md, "agents": agents, "hooks": hooks,
            "hooks_indeterminados": hooks_indef, "mcp": mcp,
        }, ensure_ascii=False, indent=2))
        return

    print(f"\nRAIO-X DE CONTEXTO   janela {num(args.janela)} tokens")
    print(f"método: {METODO} ({MARGEM})\n")
    print("CUSTO FIXO, COBRADO EM TODA MENSAGEM")
    for nome, tok, obs in sorted(blocos, key=lambda b: -b[1]):
        pct = tok / args.janela
        print(f"  {nome:<22} {num(tok):>7} tok  {pct*100:>5.2f}%  "
              f"{barra(pct*8)}  {obs}")
    print(f"  {'-'*68}")
    print(f"  {'TOTAL MEDIDO':<22} {num(total):>7} tok  "
          f"{total/args.janela*100:>5.2f}%")
    print(f"\n  Sobra para trabalho: {num(args.janela - total)} tokens")

    print(f"\nTOP {args.top} QUE MAIS PESAM")
    ranking = ([{"nome": f"skill {i['nome']}", "tokens": i["tokens"]} for i in skills]
               + [{"nome": f"md {i['nome']}", "tokens": i["tokens"]} for i in md]
               + [{"nome": f"hook {i['nome']}", "tokens": i["tokens"]} for i in hooks]
               + [{"nome": f"agent {i['nome']}", "tokens": i["tokens"]} for i in agents])
    for pos, item in enumerate(sorted(ranking, key=lambda i: -i["tokens"])[:args.top], 1):
        print(f"  {pos}. {item['nome'][:52]:<52} {item['tokens']:>5} tok")

    print("\nINDETERMINADO (não dá para medir em disco)")
    if mcp:
        print(f"  MCP: {len(mcp)} servidores ({', '.join(sorted(mcp))})")
        print("       cada tool exposta custa schema no contexto. Se as tools estiverem")
        print("       diferidas (carregadas sob demanda), o custo cai para só o nome.")
    for h in hooks_indef:
        print(f"  hook não medido: {h}")
    if hooks_indef:
        print("  rode com --medir-hooks para executar e medir esses hooks")
    if not mcp and not hooks_indef:
        print("  nada")

    print("\nONDE CORTAR")
    achou = False
    gordos = [i for i in skills if i["tokens"] > 90]
    if gordos:
        achou = True
        economia = sum(i["tokens"] - 60 for i in gordos)
        print(f"  {len(gordos)} skills com description acima de 90 tokens. Encurtar cada")
        print(f"  uma para uma linha de gatilhos devolve cerca de {num(economia)} tok"
              f" por mensagem.")
    if duplicatas:
        achou = True
        print(f"  {duplicatas} skills duplicadas em disco (versões antigas no cache de")
        print(f"  plugins). Não custam contexto, mas confundem a listagem.")
    maior_md = max(md, key=lambda i: i["tokens"], default=None)
    if maior_md and maior_md["tokens"] > 500:
        achou = True
        print(f"  {maior_md['nome']} tem {num(maior_md['tokens'])} tok. Tudo que não for")
        print(f"  regra permanente cabe melhor numa skill, carregada sob demanda.")
    if not achou:
        print("  nada óbvio. Seu custo fixo já está enxuto.")
    print()


if __name__ == "__main__":
    sys.exit(main())
