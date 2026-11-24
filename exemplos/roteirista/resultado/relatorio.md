# Quatro condições — roteirista-inema

- Tarefa: `./exemplos/roteirista/tarefa.md`
- Modelo que fez: `sonnet` · juiz: `codex` (às cegas)
- Rodadas por condição: 3 · kit v1.0.0

## Veredito

- A skill AJUDA: +0.7 sobre nada. Mantenha.
- O CLAUDE.md ajuda nesta tarefa (+2.5).
- Juntos pioram (6.2 contra 6.8 sozinho): há conflito entre o CLAUDE.md e a skill.

## Por condição

| condição | nota média | variação | segundos | custo estimado (US$) | tokens de entrada | erros |
|---|---|---|---|---|---|---|
| nada (sem CLAUDE.md, sem skill) | 4.3 | 4–5 | 10.4 | 0.0186 | 15.212 | 0 |
| só o CLAUDE.md | 6.8 | 6–7.5 | 10.7 | 0.0177 | 31.500 | 0 |
| só a skill | 5.0 | 4.5–5.5 | 11.9 | 0.0175 | 17.930 | 0 |
| CLAUDE.md + skill | 6.2 | 5.5–7 | 10.9 | 0.0174 | 34.210 | 0 |

O custo é a estimativa que o Claude Code calcula; na assinatura não é cobrado, mas mostra o peso de cada condição.

## O que o juiz disse

- **nada (sem CLAUDE.md, sem skill)** #1 (era a B): nota 4 — Apresenta uma dor concreta, mas divide o foco, exige fala acelerada, omite o inema.club e pede a palavra «TESTE» em troca de um envio cuja entrega não está estabelecida.
- **nada (sem CLAUDE.md, sem skill)** #2 (era a C): nota 4 — Fala com o espectador logo na abertura, mas dedica um bloco a uma segunda tese, pede para seguir no fechamento e usa na legenda a palavra-chave que o pedido proíbe, além de omitir o inema.club grátis.
- **nada (sem CLAUDE.md, sem skill)** #3 (era a B): nota 5 — A primeira pergunta traz uma dor concreta e o fechamento convida a responder, mas o texto falado passa bem de 150 palavras, a revisão das instruções do Claude vira um segundo assunto e falta citar o inema.club.
- **só o CLAUDE.md** #1 (era a A): nota 7 — Abre falando com o público e fecha com uma pergunta genuína para os comentários e a menção ao inema.club como grátis, mas mistura duas teses e reserva só sete segundos para um fecho longo.
- **só o CLAUDE.md** #2 (era a A): nota 6 — Abre com uma dor concreta e termina com uma pergunta que convida a comentar, mas omite o inema.club grátis, muda de tese ao entrar nos testes do Claude e passa das 150 palavras de referência.
- **só o CLAUDE.md** #3 (era a D): nota 7.5 — O gancho traz uma dor concreta, a fala cabe em um minuto e o fechamento pede comentários e cita o inema.club como grátis, mas a pergunta final muda o foco das recusas para as instruções do Claude e o método anunciado fica indefinido.
- **só a skill** #1 (era a C): nota 5 — Tem gancho direto em três segundos e duração plausível, mas introduz uma segunda tese, atribui ao narrador 40 anos de experiência sem base no pedido e omite tanto o convite para comentar quanto o inema.club grátis.
- **só a skill** #2 (era a B): nota 4.5 — O gancho é direto, mas o roteiro divide o foco entre recusas e testes de instruções, inclui uma credencial pessoal que o briefing não confirma e termina sem convite para comentar nem menção ao inema.club grátis.
- **só a skill** #3 (era a C): nota 5.5 — Tem um gancho direto e duração plausível, mas desenvolve o tema que diz ter reservado, acrescenta uma credencial sem base no pedido e termina com uma instrução, sem pergunta para comentar nem menção ao inema.club.
- **CLAUDE.md + skill** #1 (era a D): nota 7 — Tem gancho direto em três segundos, mantém uma tese e cabe no tempo, mas atribui ao narrador 40 anos de experiência sem base no pedido e termina sem convite para comentar nem menção ao inema.club grátis.
- **CLAUDE.md + skill** #2 (era a D): nota 5.5 — O gancho fala diretamente com quem já se culpou por uma recusa e a fala cabe no tempo previsto, mas o fechamento muda o foco para as instruções do Claude e, apesar da pergunta, não convida a comentar nem cita o inema.club grátis.
- **CLAUDE.md + skill** #3 (era a A): nota 6 — O gancho é curto e o roteiro cabe em um minuto, mas a mudança para os testes no Claude divide a tese, os 40 anos de experiência não vieram do pedido e a pergunta final não convida explicitamente a comentar nem cita o inema.club.

Respostas completas em `rodadas/`. Resposta crua do juiz em `juiz.txt`.
