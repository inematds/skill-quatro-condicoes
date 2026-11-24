# CLAUDE.md — skill-quatro-condicoes

Kit público (inematds/skill-quatro-condicoes, autor dos commits `inematds <inematds@gmail.com>`).

- `quatro.py` roda o modelo só pela assinatura (`claude -p --safe-mode --disable-slash-commands`) e o juiz pelo `codex exec -s read-only` ou `claude -p`. Nenhuma API. `--bare` NÃO serve (exige chave de API).
- Isolamento: `--safe-mode` desliga CLAUDE.md, skills, hooks e MCP do usuário; o CLAUDE.md e a skill testados entram por `--append-system-prompt`. É uma aproximação (a skill entra inteira, não sob demanda) — dizer isso no guia.
- Antes de commitar: `python3 -m unittest discover testes` → OK.
- Números do guia/README/vídeo saem só de `exemplos/*/resultado/relatorio.md` medidos. Nunca inventar.
- O exemplo não pode conter o texto do CLAUDE.md do Nei (só as respostas). `rodadas/*.json` não guardam o sistema.
- Guia em `guia/` (PT) + `guia/en/` + `guia/es/`; README em 3 idiomas, pelo `inema-traduz`.
- Origem: Q&A de comunidade (23/11/2026) — sem citar fonte, autor ou aula.

## Self-learning

Quando eu for corrigido ou perceber um erro: antes de seguir, acrescente a lição como regra de uma linha no TOPO de `## Lessons`.

## Lessons
- (vazio)
