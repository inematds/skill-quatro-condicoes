#!/usr/bin/env python3
"""skill-quatro-condicoes — a mesma tarefa em 4 condições, nota às cegas.

Condições:
  nada      sem CLAUDE.md e sem skill (modo seguro do Claude Code)
  claudemd  só o seu CLAUDE.md
  skill     só a skill
  ambos     CLAUDE.md + skill

Cada rodada acontece numa cópia própria da pasta de trabalho. Depois um juiz
(por padrão o Codex, de outra empresa) recebe as 4 respostas embaralhadas como
A/B/C/D, sem saber qual é qual, e dá nota de 0 a 10. O relatório desembaralha.

Usa só a assinatura (claude -p e codex exec). Não chama API nenhuma.

Uso:
  python3 quatro.py --tarefa tarefa.md --skill ~/.claude/skills/x/SKILL.md \
      --claudemd ~/.claude/CLAUDE.md --saida ~/quatro-$(date +%F)
"""
import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

VERSAO = "1.0.0"
CONDICOES = ["nada", "claudemd", "skill", "ambos"]
NOMES = {
    "nada": "nada (sem CLAUDE.md, sem skill)",
    "claudemd": "só o CLAUDE.md",
    "skill": "só a skill",
    "ambos": "CLAUDE.md + skill",
}
LIMITE_SISTEMA = 120_000  # um argumento do Linux aguenta ~128 KB
LIMITE_RESPOSTA_JUIZ = 12_000  # caracteres de cada resposta mostrados ao juiz
RECUSA = re.compile(r"(?i)(não posso (ajudar|fazer)|não vou (fazer|ajudar)|me recuso|não consigo ajudar com|"
                    r"não é algo que eu possa|I can(no|')t help|I won't|I'm not able to help|I can(no|')t assist|"
                    r"no puedo ayudar)")


def recusou(texto):
    """Detecta recusa só no começo da resposta (onde a recusa costuma aparecer)."""
    return bool(RECUSA.search((texto or "")[:600]))


def ler(p):
    return Path(p).expanduser().read_text(encoding="utf-8", errors="replace")


def texto_sistema(cond, claudemd, skill):
    """Monta o texto extra do sistema para cada condição."""
    partes = []
    if cond in ("claudemd", "ambos") and claudemd:
        partes.append("# Instruções do usuário (CLAUDE.md)\n\n" + claudemd)
    if cond in ("skill", "ambos") and skill:
        partes.append("# Skill disponível — siga-a nesta tarefa\n\n" + skill)
    t = "\n\n---\n\n".join(partes)
    if len(t.encode()) > LIMITE_SISTEMA:
        raise SystemExit(f"[erro] condição {cond}: CLAUDE.md + skill passam de {LIMITE_SISTEMA} bytes")
    return t


def comando_claude(modelo, sistema, com_bash):
    cmd = ["claude", "-p", "--safe-mode", "--disable-slash-commands",
           "--output-format", "json", "--model", modelo,
           "--permission-mode", "acceptEdits"]
    ferramentas = ["Read", "Write", "Edit", "Glob", "Grep"] + (["Bash"] if com_bash else [])
    cmd += ["--allowedTools", ",".join(ferramentas)]
    if sistema:
        cmd += ["--append-system-prompt", sistema]
    return cmd


def arquivos_da_pasta(pasta, limite=40_000):
    """Lista os arquivos que a rodada deixou na pasta (texto curto, para o juiz)."""
    out, total = [], 0
    for f in sorted(Path(pasta).rglob("*")):
        if not f.is_file() or ".git" in f.parts:
            continue
        rel = f.relative_to(pasta)
        try:
            t = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            out.append(f"--- {rel} (binário, {f.stat().st_size} bytes)")
            continue
        bloco = f"--- {rel}\n{t}"
        if total + len(bloco) > limite:
            out.append(f"--- {rel} (cortado: passou do limite)")
            continue
        total += len(bloco)
        out.append(bloco)
    return "\n".join(out)


def rodar_uma(cond, rep, args, tarefa, claudemd, skill, saida):
    pasta = saida / "rodadas" / f"{cond}-{rep}"
    if pasta.exists():
        shutil.rmtree(pasta)
    if args.pasta:
        shutil.copytree(Path(args.pasta).expanduser(), pasta, ignore=shutil.ignore_patterns(".git", "node_modules"))
    else:
        pasta.mkdir(parents=True)
    antes = {str(p.relative_to(pasta)) for p in pasta.rglob("*") if p.is_file()}
    sistema = texto_sistema(cond, claudemd, skill)
    t0 = time.time()
    if os.environ.get("QUATRO_FALSO"):  # para os testes: não chama modelo
        dado = {"result": f"resposta falsa de {cond}", "total_cost_usd": 0.01 * (CONDICOES.index(cond) + 1),
                "num_turns": 1, "usage": {"input_tokens": len(sistema) // 4, "output_tokens": 50}}
        cod = 0
    else:
        try:
            r = subprocess.run(comando_claude(args.modelo, sistema, args.com_bash), input=tarefa,
                               capture_output=True, text=True, cwd=pasta, timeout=args.timeout)
            cod = r.returncode
            try:
                dado = json.loads(r.stdout)
            except json.JSONDecodeError:
                dado = {"result": (r.stdout or r.stderr)[-3000:], "is_error": True}
        except subprocess.TimeoutExpired:
            cod, dado = -1, {"result": f"[estourou {args.timeout}s]", "is_error": True}
    seg = time.time() - t0
    uso = dado.get("usage") or {}
    depois = {str(p.relative_to(pasta)) for p in pasta.rglob("*") if p.is_file()}
    reg = {
        "condicao": cond, "rep": rep, "codigo": cod, "segundos": round(seg, 1),
        "erro": bool(dado.get("is_error")) or cod != 0,
        "custo_estimado_usd": dado.get("total_cost_usd"),
        "turnos": dado.get("num_turns"),
        "tokens_entrada": (uso.get("input_tokens") or 0) + (uso.get("cache_read_input_tokens") or 0)
        + (uso.get("cache_creation_input_tokens") or 0),
        "tokens_saida": uso.get("output_tokens") or 0,
        "arquivos_novos": sorted(depois - antes),
        "resposta": dado.get("result") or "",
        "recusou": recusou(dado.get("result")),
        "pasta": str(pasta),
    }
    (pasta.parent / f"{cond}-{rep}.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1))
    return reg


# ---------- juiz ----------

def embaralhar(regs, semente):
    """Devolve [(letra, reg)] em ordem aleatória reprodutível."""
    rnd = random.Random(semente)
    ordem = regs[:]
    rnd.shuffle(ordem)
    return list(zip("ABCDEFGH", ordem))


def prompt_juiz(tarefa, criterios, letras):
    blocos = []
    for letra, reg in letras:
        corpo = reg["resposta"][:LIMITE_RESPOSTA_JUIZ]
        arq = arquivos_da_pasta(reg["pasta"]) if reg["arquivos_novos"] else ""
        extra = ("### Arquivos criados\n" + arq[:LIMITE_RESPOSTA_JUIZ]) if arq else ""
        blocos.append(f"## Resposta {letra}\n\n{corpo}\n\n{extra}")
    crit = criterios or ("1. Cumpre o que a tarefa pede, sem faltar nada.\n2. Está certo (sem erro de fato ou de código).\n"
                         "3. Está claro e pronto para usar.\n4. Não inventa coisa que não foi pedida.")
    return (
        "Você é um avaliador independente. Avalie cada resposta à mesma tarefa, sem saber como foi gerada.\n"
        "Dê nota de 0 a 10 para cada uma, pelos critérios abaixo. Seja duro e consistente: a mesma qualidade "
        "recebe a mesma nota.\n\n"
        f"# Tarefa\n\n{tarefa}\n\n# Critérios\n\n{crit}\n\n" + "\n\n".join(blocos) +
        "\n\n# Formato da sua resposta\nResponda SÓ com JSON, sem texto antes ou depois:\n"
        '{"notas": {"A": {"nota": 0, "motivo": "uma frase"}, ...}}'
    )


def extrair_json(texto):
    m = re.search(r"\{.*\}", texto or "", re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def chamar_juiz(juiz, prompt, timeout):
    if os.environ.get("QUATRO_FALSO"):
        letras = re.findall(r"## Resposta ([A-H])", prompt)
        return json.dumps({"notas": {l: {"nota": 5 + i, "motivo": "falso"} for i, l in enumerate(letras)}})
    if juiz == "codex":
        cmd = ["codex", "exec", "-s", "read-only", "--skip-git-repo-check", "-"]
        modelo = os.environ.get("QUATRO_JUIZ_MODELO")
        if modelo:
            cmd[2:2] = ["-m", modelo]
    else:
        cmd = ["claude", "-p", "--safe-mode", "--disable-slash-commands", "--model",
               os.environ.get("QUATRO_JUIZ_MODELO", "opus")]
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout,
                       cwd=os.environ.get("TMPDIR", "/tmp"))
    return r.stdout


def julgar(regs, tarefa, criterios, juiz, semente, timeout):
    letras = embaralhar(regs, semente)
    bruto = chamar_juiz(juiz, prompt_juiz(tarefa, criterios, letras), timeout)
    dado = extrair_json(bruto) or {}
    notas = dado.get("notas", {})
    for letra, reg in letras:
        n = notas.get(letra) or {}
        reg["letra"] = letra
        reg["nota"] = n.get("nota")
        reg["motivo"] = n.get("motivo", "")
    return bruto


# ---------- relatório ----------

def media(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return round(sum(xs) / len(xs), 1) if xs else None


def resumo(regs):
    lin = []
    for c in CONDICOES:
        rs = [r for r in regs if r["condicao"] == c]
        if not rs:
            continue
        lin.append({
            "condicao": c, "rodadas": len(rs), "nota": media([r.get("nota") for r in rs]),
            "nota_min": min([r["nota"] for r in rs if isinstance(r.get("nota"), (int, float))], default=None),
            "nota_max": max([r["nota"] for r in rs if isinstance(r.get("nota"), (int, float))], default=None),
            "segundos": media([r["segundos"] for r in rs]),
            "custo": (round(sum(x for x in [r["custo_estimado_usd"] for r in rs] if x) / len(rs), 4)
                      if any(r["custo_estimado_usd"] for r in rs) else None),
            "tokens_entrada": media([r["tokens_entrada"] for r in rs]),
            "erros": sum(r["erro"] for r in rs),
            "recusas": sum(r.get("recusou", False) for r in rs),
        })
    return lin


def veredito(lin, margem=0.5):
    """Regras simples e explícitas: diferença menor que a margem = empate."""
    n = {l["condicao"]: l["nota"] for l in lin if l["nota"] is not None}
    if "nada" not in n or len(n) < 2:
        return ["Faltou nota para comparar (o juiz não respondeu?)."]
    out = []
    if "skill" in n:
        d_skill = n["skill"] - n["nada"]
        if d_skill >= margem:
            out.append(f"A skill AJUDA: +{d_skill:.1f} sobre nada. Mantenha.")
        elif d_skill <= -margem:
            out.append(f"A skill ATRAPALHA: {d_skill:.1f} sobre nada. Revise ou aposente.")
        else:
            out.append(f"A skill NÃO MUDA a nota ({d_skill:+.1f}). Se gasta mais, é peso morto para esta tarefa.")
    if "claudemd" in n:
        d_cm = n["claudemd"] - n["nada"]
        if d_cm <= -margem:
            out.append(f"O CLAUDE.md ATRAPALHA nesta tarefa ({d_cm:.1f}). Procure a regra que confunde.")
        elif d_cm >= margem:
            out.append(f"O CLAUDE.md ajuda nesta tarefa (+{d_cm:.1f}).")
        else:
            out.append(f"O CLAUDE.md não muda a nota nesta tarefa ({d_cm:+.1f}).")
    rec = {l["condicao"]: l.get("recusas", 0) for l in lin}
    if any(rec.values()):
        quem = ", ".join(f"{NOMES[c]}: {k}" for c, k in rec.items() if k)
        out.append(f"Houve RECUSA ({quem}). Se recusa até em 'nada', é o modelo: passe o passo mecânico para código "
                   "ou teste um modelo aberto (veja docs/quando-a-ia-recusa.md). Se só recusa com instruções, é a sua configuração.")
    if "ambos" in n:
        melhor_sozinho = max(n.get("skill", 0), n.get("claudemd", 0))
        if n["ambos"] < melhor_sozinho - margem:
            out.append(f"Juntos pioram ({n['ambos']} contra {melhor_sozinho} sozinho): há conflito entre o CLAUDE.md e a skill.")
    return out


def escrever_relatorio(saida, args, regs, lin, ver, bruto_juiz):
    nome_skill = (Path(args.skill).parent.name if Path(args.skill).name == "SKILL.md" else Path(args.skill).stem) if args.skill else "sem skill"
    L = [f"# Quatro condições — {nome_skill}", "",
         f"- Tarefa: `{args.tarefa}`", f"- Modelo que fez: `{args.modelo}` · juiz: `{args.juiz}` (às cegas)",
         f"- Rodadas por condição: {args.rep} · kit v{VERSAO}", "",
         "## Veredito", ""] + [f"- {v}" for v in ver] + ["",
         "## Por condição", "",
         "| condição | nota média | variação | segundos | custo estimado (US$) | tokens de entrada | recusas | erros |",
         "|---|---|---|---|---|---|---|---|"]
    for l in lin:
        var = f"{l['nota_min']}–{l['nota_max']}" if l["rodadas"] > 1 else "—"
        tok = f"{int(l['tokens_entrada']):,}".replace(",", ".") if l["tokens_entrada"] else "—"
        L.append(f"| {NOMES[l['condicao']]} | {l['nota']} | {var} | {l['segundos']} | {l['custo']} | {tok} | {l['recusas']} | {l['erros']} |")
    if any(l["nota_max"] is not None and l["nota_min"] is not None and l["nota_max"] - l["nota_min"] >= 2 for l in lin):
        L += ["", "⚠️ A nota de uma mesma condição variou 2 pontos ou mais entre rodadas: rode com `--rep 3` ou mais antes de decidir."]
    L += ["", "O custo é a estimativa que o Claude Code calcula; na assinatura não é cobrado, mas mostra o peso de cada condição.",
          "", "## O que o juiz disse", ""]
    for r in sorted(regs, key=lambda r: (CONDICOES.index(r["condicao"]), r["rep"])):
        L.append(f"- **{NOMES[r['condicao']]}** #{r['rep']} (era a {r.get('letra')}): nota {r.get('nota')} — {r.get('motivo')}")
    L += ["", "Respostas completas em `rodadas/`. Resposta crua do juiz em `juiz.txt`."]
    (saida / "relatorio.md").write_text("\n".join(L) + "\n")
    (saida / "juiz.txt").write_text(bruto_juiz or "")
    (saida / "resultado.json").write_text(json.dumps({"versao": VERSAO, "resumo": lin, "veredito": ver,
                                                     "rodadas": regs}, ensure_ascii=False, indent=1))


def main(argv=None):
    ap = argparse.ArgumentParser(description="A mesma tarefa em 4 condições, nota às cegas.")
    ap.add_argument("--tarefa", required=True, help="arquivo com o pedido (o mesmo nas 4 condições)")
    ap.add_argument("--skill", help="SKILL.md a testar")
    ap.add_argument("--claudemd", help="CLAUDE.md a testar")
    ap.add_argument("--criterios", help="arquivo com os critérios do juiz (opcional)")
    ap.add_argument("--pasta", help="pasta de trabalho copiada para cada rodada (opcional)")
    ap.add_argument("--modelo", default="sonnet", help="modelo que executa (padrão: sonnet)")
    ap.add_argument("--juiz", choices=["codex", "claude"], default="codex")
    ap.add_argument("--rep", type=int, default=1, help="rodadas por condição (padrão 1; 3 dá mais confiança)")
    ap.add_argument("--condicoes", default=",".join(CONDICOES))
    ap.add_argument("--com-bash", action="store_true", help="libera o Bash nas rodadas (padrão: só ler/escrever arquivos)")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--semente", type=int, default=None)
    ap.add_argument("--saida", required=True)
    a = ap.parse_args(argv)
    conds = [c for c in a.condicoes.split(",") if c in CONDICOES]
    if not a.skill:
        conds = [c for c in conds if c not in ("skill", "ambos")]
    if not a.claudemd:
        conds = [c for c in conds if c not in ("claudemd", "ambos")]
    if len(conds) < 2:
        raise SystemExit("[erro] preciso de pelo menos 2 condições (dê --skill e/ou --claudemd)")
    saida = Path(a.saida).expanduser()
    saida.mkdir(parents=True, exist_ok=True)
    tarefa = ler(a.tarefa)
    claudemd = ler(a.claudemd) if a.claudemd else ""
    skill = ler(a.skill) if a.skill else ""
    criterios = ler(a.criterios) if a.criterios else ""
    regs = []
    for rep in range(1, a.rep + 1):
        for c in conds:
            print(f"[rodada] {c} #{rep}…", flush=True)
            r = rodar_uma(c, rep, a, tarefa, claudemd, skill, saida)
            print(f"   {r['segundos']} s · {r['tokens_entrada']} tokens de entrada · erro={r['erro']}", flush=True)
            regs.append(r)
    print(f"[juiz] {a.juiz} avaliando {len(regs)} respostas às cegas…", flush=True)
    semente = a.semente if a.semente is not None else int(time.time())
    # com várias rodadas, o juiz vê um lote por rodada (sempre as 4 condições juntas)
    bruto_total = []
    for rep in range(1, a.rep + 1):
        lote = [r for r in regs if r["rep"] == rep]
        bruto_total.append(julgar(lote, tarefa, criterios, a.juiz, semente + rep, a.timeout))
    lin = resumo(regs)
    ver = veredito(lin)
    escrever_relatorio(saida, a, regs, lin, ver, "\n\n=====\n\n".join(bruto_total))
    print("\n".join(ver))
    print(f"[ok] relatório: {saida / 'relatorio.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
