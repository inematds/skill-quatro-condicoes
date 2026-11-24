# Skill Proof (skill in 4 conditions)

[![Skill Under Four Conditions](guia/assets/banner-en.jpg)](https://inematds.github.io/skill-quatro-condicoes/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

You wrote rules in CLAUDE.md and created skills, but you don’t know whether they help or hinder the AI. This kit answers that with a test: the same task runs under **four conditions**: no instructions, CLAUDE.md only, the skill only, and both together. Then a judge from **another company** (Codex) scores the four responses **without knowing which is which**. The final report shows each condition’s score, time, tokens used, and refusals, plus a verdict: whether the skill helps, makes no difference, or gets in the way, and whether CLAUDE.md and the skill conflict. It works with your Claude Code and Codex subscriptions, without an API key.

## 📖 User guide

Complete guide (landing page + walkthrough): **https://inematds.github.io/skill-quatro-condicoes/guia/en/**

## How to get started without coding

Open Claude Code (or Codex) in your working folder and paste this request. The AI reads the kit, shows you the plan, and runs it only after you say yes.

```text
Read the "Skill Proof" kit at https://github.com/inematds/skill-quatro-condicoes (the README explains everything, including installation).
Then look at my skills and CLAUDE.md and answer me in plain English:
1. Which skill do I use most, and what real task could test it?
2. What criteria should the judge use to decide whether the response is good?
3. How long will the proof take with 3 rounds per condition?
Don’t run anything yet. Show me the plan and wait for me to say yes. After running it, explain the verdict and what I should change.
```

---

## Technical installation

### Start with three commands

```bash
git clone https://github.com/inematds/skill-quatro-condicoes ~/skill-quatro-condicoes
cd ~/skill-quatro-condicoes
python3 quatro.py --tarefa minha-tarefa.md --skill ~/.claude/skills/minha-skill/SKILL.md \
  --claudemd ~/.claude/CLAUDE.md --rep 3 --saida ~/quatro-$(date +%F)
```

Open `~/quatro-<data>/relatorio.md`.

## What we actually measured

We tested a real Reels scriptwriting skill with the real CLAUDE.md of the person using it. There were 3 rounds per condition, with Sonnet writing and Codex judging blindly ([full report](exemplos/roteirista/resultado/relatorio.md)):

| condition | average score (0–10) | input tokens |
|---|---|---|
| none | 4.3 | 15.212 |
| CLAUDE.md only | **6.8** | 31.500 |
| skill only | 5.0 | 17.930 |
| CLAUDE.md + skill | 6.2 | 34.210 |

What this showed:
- **Together, they scored lower than CLAUDE.md alone.** The kit flagged a conflict, and there was one: the skill said to ask people to “comment the word X and I’ll send you the link,” while the newer CLAUDE.md prohibits asking for a word or a link. The skill was outdated, and no one had noticed.
- **CLAUDE.md doubles the input tokens** (15,000 → 31,000). For this task, it was worth the cost. For another task, it may not be, and that’s what the test is for.
- **One round can mislead you.** In the first measurement, with 2 rounds, the same condition scored 4 in one round and 7 in the other. Use `--rep 3` or more before deciding.

## When the AI refuses

The report counts refusals for each condition. If the AI refuses even without any instructions, the restriction comes from the model: frontier companies err on the side of refusing to protect themselves from laws like the European AI Act and the risk of lawsuits in the US. In that case, move the mechanical step to code or use an open model. See [docs/quando-a-ia-recusa.md](docs/quando-a-ia-recusa.md).

## The process from start to finish

| # | Step | Command | Who |
|---|---|---|---|
| 1 | Write the task (the same request for all 4) | `minha-tarefa.md` | 🧠 you |
| 2 | (Optional) Write the judge’s criteria | `criterios.md` | 🧠 you |
| 3 | Run the 4 conditions, each in its own folder | `python3 quatro.py --tarefa … --skill … --claudemd … --rep 3 --saida …` | ⚙️ script + 🤖 `claude -p` |
| 4 | Judge scores blindly (A/B/C/D shuffled) | automatic, at the end of step 3 | 🤖 `codex exec` |
| 5 | Read the verdict and the reason for each score | `relatorio.md` | 🧠 you |
| 6 | Fix the skill or conflicting rule and run again | step 3 | 🧠 you + ⚙️ script |
| 7 | Repeat with each new model | step 3 | 🧠 you |

## Options

| option | default | purpose |
|---|---|---|
| `--modelo` | `sonnet` | model that performs the task |
| `--juiz` | `codex` | `codex` (another company) or `claude` (Opus) |
| `--rep` | 1 | rounds per condition; use 3 or more to decide |
| `--pasta` | empty | working folder copied for each round (for tasks that modify files) |
| `--com-bash` | off | lets the AI run commands inside the copy |
| `--criterios` | 4 general criteria | what the judge should evaluate |
| `--condicoes` | all 4 | e.g.: `nada,skill` |

## How isolation works (and its limits)

Each round uses `claude -p --safe-mode --disable-slash-commands`, which disables your CLAUDE.md, skills, hooks, and MCP. Your subscription login remains active. The tested CLAUDE.md and skill are added as extra system text. This is an approximation: in normal use, a skill is loaded only when Claude decides to use it; here, it is included in full from the start. That’s why the test measures whether **the skill’s content** helps, not whether its description makes Claude call it at the right time.

## Requirements

Python 3.8+, Claude Code logged in with a subscription (`claude`) and, for the default judge, Codex CLI logged in (`codex`). Tests without a model: `python3 -m unittest discover testes`.

## License

MIT.