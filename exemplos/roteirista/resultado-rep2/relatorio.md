# Quatro condições — SKILL.md

- Tarefa: `./exemplos/roteirista/tarefa.md`
- Modelo que fez: `sonnet` · juiz: `codex` (às cegas)
- Rodadas por condição: 2 · kit v1.0.0

## Veredito

- A skill AJUDA: +1.5 sobre nada. Mantenha.
- O CLAUDE.md ajuda nesta tarefa (+1.5).

## Por condição

| condição | nota | segundos | custo estimado (US$) | tokens de entrada | erros |
|---|---|---|---|---|---|
| nada (sem CLAUDE.md, sem skill) | 4.0 | 9.9 | 0.0 | 15232.0 | 0 |
| só o CLAUDE.md | 5.5 | 11.2 | 0.1 | 31500.0 | 0 |
| só a skill | 5.5 | 11.1 | 0.0 | 17930.0 | 0 |
| CLAUDE.md + skill | 6.0 | 11.4 | 0.1 | 34210.0 | 0 |

O custo é a estimativa que o Claude Code calcula; na assinatura não é cobrado, mas mostra o peso de cada condição.

## O que o juiz disse

- **nada (sem CLAUDE.md, sem skill)** #1 (era a B): nota 4 — Abre com uma dor concreta, mas mistura duas teses, exige fala acelerada para caber no tempo e termina pedindo para seguir, sem pergunta para os comentários nem menção ao inema.club.
- **nada (sem CLAUDE.md, sem skill)** #2 (era a C): nota 4 — O exemplo de abertura é concreto, mas a fala é longa para 60 segundos em ritmo natural, desvia para o teste de instruções do Claude e fecha pedindo para salvar e compartilhar, sem pergunta para comentar nem menção ao inema.club grátis.
- **só o CLAUDE.md** #1 (era a A): nota 7 — Abre com uma dor concreta, cabe no tempo e fecha com pergunta para os comentários e menção ao inema.club grátis, mas introduz uma segunda tese sobre testar instruções no Claude.
- **só o CLAUDE.md** #2 (era a A): nota 4 — A abertura traz uma dor concreta, mas o roteiro acrescenta a pauta de testar instruções, passa do ritmo de fala previsto e termina com um pedido para seguir, deixando a pergunta para comentar só na legenda e omitindo o inema.club grátis.
- **só a skill** #1 (era a C): nota 6 — Sustenta uma tese e cabe no tempo, mas o gancho afirma a conclusão sem falar diretamente com quem assiste, o fecho omite a pergunta para os comentários e o inema.club, e a fala atribui ao narrador uma experiência que o briefing não informa.
- **só a skill** #2 (era a B): nota 5 — O gancho fala com o espectador e a duração é plausível, mas o roteiro abre uma segunda pauta sobre o Claude, atribui ao narrador 40 anos de experiência sem base no pedido e omite tanto o convite para comentar quanto o inema.club grátis.
- **CLAUDE.md + skill** #1 (era a D): nota 5 — Abre com uma pergunta direta e cabe no tempo, mas muda de assunto no fim, atribui ao narrador uma experiência que o briefing não informa e omite a pergunta para os comentários e a menção ao inema.club.
- **CLAUDE.md + skill** #2 (era a D): nota 7 — O gancho fala diretamente com o espectador e a fala sustenta uma única tese, mas acrescenta uma credencial sem base no pedido e fecha com uma pergunta para reflexão sem convidar a comentar nem citar o inema.club grátis.

Respostas completas em `rodadas/`. Resposta crua do juiz em `juiz.txt`.
