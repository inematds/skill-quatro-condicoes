# Skill em 4 condições

[![Skill em 4 condições](guia/assets/banner.jpg)](https://inematds.github.io/skill-quatro-condicoes/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Você escreveu regras no CLAUDE.md e criou skills, mas não sabe se elas ajudam ou atrapalham a IA. Este kit tira a dúvida com um teste: a mesma tarefa roda em **quatro condições**: sem nada, só com o CLAUDE.md, só com a skill e com os dois. Depois um juiz de **outra empresa** (o Codex) dá nota às quatro respostas **sem saber qual é qual**. No fim sai um relatório com a nota, o tempo, os tokens gastos e as recusas de cada condição, além de um veredito: a skill ajuda, não muda ou atrapalha, e se o CLAUDE.md e a skill brigam entre si. Funciona pela sua assinatura do Claude Code e do Codex, sem chave de API.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/skill-quatro-condicoes/guia/**

## Comece em três comandos

```bash
git clone https://github.com/inematds/skill-quatro-condicoes ~/skill-quatro-condicoes
cd ~/skill-quatro-condicoes
python3 quatro.py --tarefa minha-tarefa.md --skill ~/.claude/skills/minha-skill/SKILL.md \
  --claudemd ~/.claude/CLAUDE.md --rep 3 --saida ~/quatro-$(date +%F)
```

Abra `~/quatro-<data>/relatorio.md`.

## O que medimos de verdade

Testamos uma skill real de roteiro de Reels com o CLAUDE.md real de quem a usa. Foram 3 rodadas por condição, o Sonnet escrevendo e o Codex julgando às cegas ([relatório completo](exemplos/roteirista/resultado/relatorio.md)):

| condição | nota média (0–10) | tokens de entrada |
|---|---|---|
| nada | 4,3 | 15.212 |
| só o CLAUDE.md | **6,8** | 31.500 |
| só a skill | 5,0 | 17.930 |
| CLAUDE.md + skill | 6,2 | 34.210 |

O que isso mostrou:
- **Juntos ficaram abaixo do CLAUDE.md sozinho.** O kit apontou conflito, e havia um: a skill mandava pedir "comenta a palavra X que eu te mando o link", enquanto o CLAUDE.md, mais novo, proíbe pedir palavra ou link. A skill ficou velha e ninguém tinha percebido.
- **O CLAUDE.md dobra os tokens de entrada** (15 mil → 31 mil). Nesta tarefa ele valeu o gasto. Em outra, pode não valer, e é para isso que serve o teste.
- **Uma rodada só engana.** Na primeira medição, com 2 rodadas, a mesma condição tirou 4 numa e 7 na outra. Use `--rep 3` ou mais antes de decidir.

## Quando a IA recusa

O relatório conta as recusas de cada condição. Se a IA recusa até sem nenhuma instrução, a trava é do modelo: as empresas de fronteira travam na dúvida para se proteger de leis como o AI Act europeu e o risco de processo nos EUA. Nesse caso, passe o passo mecânico para código ou use um modelo aberto. Se só recusa com as suas instruções, o problema está na sua configuração. Veja [docs/quando-a-ia-recusa.md](docs/quando-a-ia-recusa.md).

## O processo, do início ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Escrever a tarefa (o mesmo pedido para as 4) | `minha-tarefa.md` | 🧠 você |
| 2 | (Opcional) escrever os critérios do juiz | `criterios.md` | 🧠 você |
| 3 | Rodar as 4 condições, cada uma numa pasta própria | `python3 quatro.py --tarefa … --skill … --claudemd … --rep 3 --saida …` | ⚙️ script + 🤖 `claude -p` |
| 4 | Juiz dá nota às cegas (A/B/C/D embaralhadas) | automático, no fim do passo 3 | 🤖 `codex exec` |
| 5 | Ler o veredito e o motivo de cada nota | `relatorio.md` | 🧠 você |
| 6 | Corrigir a skill ou a regra que conflita e rodar de novo | passo 3 | 🧠 você + ⚙️ script |
| 7 | Repetir a cada modelo novo | passo 3 | 🧠 você |

## Opções

| opção | padrão | para quê |
|---|---|---|
| `--modelo` | `sonnet` | modelo que executa a tarefa |
| `--juiz` | `codex` | `codex` (outra empresa) ou `claude` (Opus) |
| `--rep` | 1 | rodadas por condição; 3 ou mais para decidir |
| `--pasta` | vazia | pasta de trabalho copiada para cada rodada (tarefas que mexem em arquivos) |
| `--com-bash` | desligado | deixa a IA rodar comandos dentro da cópia |
| `--criterios` | 4 critérios gerais | o que o juiz deve olhar |
| `--condicoes` | as 4 | ex.: `nada,skill` |

## Como o isolamento funciona (e o limite dele)

Cada rodada usa `claude -p --safe-mode --disable-slash-commands`, que desliga o seu CLAUDE.md, as suas skills, hooks e MCP. O login da assinatura continua valendo. O CLAUDE.md e a skill testados entram como texto extra do sistema. Isso é uma aproximação: no uso normal a skill só é carregada quando o Claude decide usá-la, e aqui ela entra inteira desde o começo. Por isso o teste mede se **o conteúdo** da skill ajuda, não se a descrição dela faz o Claude chamá-la na hora certa.

## Requisitos

Python 3.8+, Claude Code logado na assinatura (`claude`) e, para o juiz padrão, o Codex CLI logado (`codex`). Testes sem modelo: `python3 -m unittest discover testes`.

## Licença

MIT.
