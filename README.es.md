# Skill en 4 condiciones

[![Skill en 4 condiciones](guia/assets/banner.jpg)](https://inematds.github.io/skill-quatro-condicoes/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Escribiste reglas en el CLAUDE.md y creaste skills, pero no sabes si ayudan o perjudican a la IA. Este kit despeja la duda con una prueba: la misma tarea se ejecuta en **cuatro condiciones**: sin nada, solo con el CLAUDE.md, solo con la skill y con ambos. Después, un juez de **otra empresa** (Codex) califica las cuatro respuestas **sin saber cuál es cuál**. Al final se genera un informe con la calificación, el tiempo, los tokens utilizados y las negativas de cada condición, además de un veredicto: la skill ayuda, no cambia nada o perjudica, y si el CLAUDE.md y la skill entran en conflicto. Funciona con tu suscripción de Claude Code y Codex, sin clave de API.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/skill-quatro-condicoes/guia/**

## Empieza con tres comandos

```bash
git clone https://github.com/inematds/skill-quatro-condicoes ~/skill-quatro-condicoes
cd ~/skill-quatro-condicoes
python3 quatro.py --tarefa minha-tarefa.md --skill ~/.claude/skills/minha-skill/SKILL.md \
  --claudemd ~/.claude/CLAUDE.md --rep 3 --saida ~/quatro-$(date +%F)
```

Abre `~/quatro-<data>/relatorio.md`.

## Lo que medimos de verdad

Probamos una skill real para escribir guiones de Reels con el CLAUDE.md real de quien la usa. Se hicieron 3 rondas por condición, con Sonnet escribiendo y Codex evaluando a ciegas ([informe completo](exemplos/roteirista/resultado/relatorio.md)):

| condición | calificación promedio (0–10) | tokens de entrada |
|---|---|---|
| nada | 4,3 | 15.212 |
| solo el CLAUDE.md | **6,8** | 31.500 |
| solo la skill | 5,0 | 17.930 |
| CLAUDE.md + skill | 6,2 | 34.210 |

Lo que mostró:
- **Juntos quedaron por debajo del CLAUDE.md por sí solo.** El kit detectó un conflicto, y sí lo había: la skill indicaba pedir «comenta la palabra X y te envío el enlace», mientras que el CLAUDE.md, más reciente, prohíbe pedir palabras o enlaces. La skill había quedado desactualizada y nadie lo había notado.
- **El CLAUDE.md duplica los tokens de entrada** (15 mil → 31 mil). En esta tarea valió la pena. En otra puede que no, y para eso sirve la prueba.
- **Una sola ronda puede engañar.** En la primera medición, con 2 rondas, la misma condición obtuvo 4 en una y 7 en la otra. Usa `--rep 3` o más antes de decidir.

## Cuando la IA se niega

El informe cuenta las negativas de cada condición. Si la IA se niega incluso sin instrucciones, el bloqueo viene del modelo: las empresas líderes del sector tienden a bloquear ante la duda para protegerse de leyes como el AI Act europeo y del riesgo de demandas en EE. UU. En ese caso, pasa el paso mecánico al código o usa un modelo abierto. Consulta [docs/quando-a-ia-recusa.md](docs/quando-a-ia-recusa.md).

## El proceso, de principio a fin

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Escribir la tarea (el mismo pedido para las 4) | `minha-tarefa.md` | 🧠 tú |
| 2 | (Opcional) escribir los criterios del juez | `criterios.md` | 🧠 tú |
| 3 | Ejecutar las 4 condiciones, cada una en su propia carpeta | `python3 quatro.py --tarefa … --skill … --claudemd … --rep 3 --saida …` | ⚙️ script + 🤖 `claude -p` |
| 4 | El juez califica a ciegas (A/B/C/D en orden aleatorio) | automático, al final del paso 3 | 🤖 `codex exec` |
| 5 | Leer el veredicto y el motivo de cada calificación | `relatorio.md` | 🧠 tú |
| 6 | Corregir la skill o la regla en conflicto y volver a ejecutar | paso 3 | 🧠 tú + ⚙️ script |
| 7 | Repetir con cada modelo nuevo | paso 3 | 🧠 tú |

## Opciones

| opción | predeterminado | para qué |
|---|---|---|
| `--modelo` | `sonnet` | modelo que ejecuta la tarea |
| `--juiz` | `codex` | `codex` (otra empresa) o `claude` (Opus) |
| `--rep` | 1 | rondas por condición; 3 o más para decidir |
| `--pasta` | vacía | carpeta de trabajo copiada para cada ronda (tareas que modifican archivos) |
| `--com-bash` | desactivado | permite que la IA ejecute comandos dentro de la copia |
| `--criterios` | 4 criterios generales | qué debe evaluar el juez |
| `--condicoes` | las 4 | ej.: `nada,skill` |

## Cómo funciona el aislamiento (y cuál es su límite)

Cada ronda usa `claude -p --safe-mode --disable-slash-commands`, que desactiva tu CLAUDE.md, tus skills, hooks y MCP. El inicio de sesión de la suscripción sigue activo. El CLAUDE.md y la skill que se están probando se agregan como texto extra del sistema. Es una aproximación: en el uso normal, la skill solo se carga cuando Claude decide usarla, pero aquí se incluye completa desde el principio. Por eso, la prueba mide si **el contenido** de la skill ayuda, no si su descripción hace que Claude la invoque en el momento adecuado.

## Requisitos

Python 3.8+, Claude Code con la sesión iniciada mediante la suscripción (`claude`) y, para el juez predeterminado, Codex CLI con la sesión iniciada (`codex`). Pruebas sin modelo: `python3 -m unittest discover testes`.

## Licencia

MIT.