# Skill Under 4 Conditions

[![Skill Under 4 Conditions](guia/assets/banner.jpg)](https://inematds.github.io/skill-quatro-condicoes/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What It Is

You wrote rules in CLAUDE.md and created skills, but you don’t know whether they help or hinder the AI. This kit answers that with a test: the same task runs under **four conditions**: with nothing, with only CLAUDE.md, with only the skill, and with both. Then a judge from **another company** (Codex) scores all four responses **without knowing which is which**. The result is a report with the score, time, tokens used, and refusals for each condition, along with a verdict: whether the skill helps, makes no difference, or hinders, and whether CLAUDE.md and the skill conflict. It works with your Claude Code and Codex subscriptions, without an API key.

## 📖 User Guide

Full guide (landing page + walkthrough): **https://inematds.github.io/skill-quatro-condicoes/guia/**

## Get Started in Three Commands

```bash
git clone https://github.com/inematds/skill-quatro-condicoes ~/skill-quatro-condicoes
cd ~/skill-quatro-condicoes
python3 quatro.py --tarefa minha-tarefa.md --skill ~/.claude/skills/minha-skill/SKILL.md \
  --claudemd ~/.claude/CLAUDE.md --rep 3 --saida ~/quatro-$(date +%F)
```

Open `~/quatro-<data>/relatorio.md`.

## What We Actually Measured

We tested a real Reels scriptwriting skill with the real CLAUDE.md used by its owner. We ran 3 rounds per condition, with Sonnet writing and Codex judging blindly ([full report](exemplos/roteirista/resultado/relatorio.md)):

| condition | average score (0–10) | input tokens |
|---|---|---|
| nothing | 4.3 | 15,212 |
| CLAUDE.md only | **6.8** | 31,500 |
| skill only | 5.0 | 17,930 |
| CLAUDE.md + skill | 6.2 | 34,210 |

What this showed:
- **Together, they scored lower than CLAUDE.md alone.** The kit flagged a conflict, and there was one: the skill said to ask users to “comment the word X and I’ll send you the link,” while the newer CLAUDE.md prohibits asking for a word or link. The skill was outdated, and nobody had noticed.
- **CLAUDE.md doubles input tokens** (15,000 → 31,000). For this task, it was worth the cost. For another task, it might not be, and that’s what the test is for.
- **A single round can mislead you.** In the first measurement, with 2 rounds, the same condition scored 4 once and 7 the other time. Use `--rep 3` or more before deciding.

## When the AI Refuses

The report counts refusals for each condition. If the AI refuses even without any instructions, the restriction comes from the model: frontier companies err on the side of caution to protect themselves from laws like the EU AI Act and the risk of lawsuits in the U.S. In that case, hand the mechanical step off to code or use an open model. If it refuses only with your instructions, the problem is in your configuration. See [docs/quando-a-ia-recusa.md](docs/quando-a-ia-recusa.md).

## The Process, From Start to Finish

| # | Step | Command | Who |
|---|---|---|---|
| 1 | Write the task (the same prompt for all 4) | `minha-tarefa.md` | 🧠 you |
| 2 | (Optional) Write the judge’s criteria | `criterios.md` | 🧠 you |
| 3 | Run the 4 conditions, each in its own folder | `python3 quatro.py --tarefa … --skill … --claudemd … --rep 3 --saida …` | ⚙️ script + 🤖 `claude -p` |
| 4 | Judge scores the responses blindly (A/B/C/D shuffled) | automatic, at the end of step 3 | 🤖 `codex exec` |
| 5 | Read the verdict and the reason for each score | `relatorio.md` | 🧠 you |
| 6 | Fix the skill or conflicting rule and run it again | step 3 | 🧠 you + ⚙️ script |
| 7 | Repeat for each new model | step 3 | 🧠 you |

## Options

| option | default | purpose |
|---|---|---|
| `--modelo` | `sonnet` | model that performs the task |
| `--juiz` | `codex` | `codex` (another company) or `claude` (Opus) |
| `--rep` | 1 | rounds per condition; use 3 or more to decide |
| `--pasta` | empty | working folder copied for each round (for tasks that modify files) |
| `--com-bash` | disabled | lets the AI run commands inside the copy |
| `--criterios` | 4 general criteria | what the judge should evaluate |
| `--condicoes` | all 4 | e.g.: `nada,skill` |

## How Isolation Works (and Its Limits)

Each round uses `claude -p --safe-mode --disable-slash-commands`, which disables your CLAUDE.md, skills, hooks, and MCP. Your subscription login remains active. The tested CLAUDE.md and skill are added as extra system text. This is an approximation: under normal use, the skill is loaded only when Claude decides to use it, while here it is included in full from the start. So the test measures whether **the skill’s content** helps, not whether its description prompts Claude to call it at the right time.

## Requirements

Python 3.8+, Claude Code logged in with a subscription (`claude`), and, for the default judge, the Codex CLI logged in (`codex`). Tests without a model: `python3 -m unittest discover testes`.

## License

MIT.