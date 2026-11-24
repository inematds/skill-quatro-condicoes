# Prueba de la Skill (skill en 4 condiciones)

[![Skill en 4 condiciones](guia/assets/banner-es.jpg)](https://inematds.github.io/skill-quatro-condicoes/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Escribiste reglas en el CLAUDE.md y creaste skills, pero no sabes si ayudan o perjudican a la IA. Este kit resuelve la duda con una prueba: la misma tarea se ejecuta en **cuatro condiciones**: sin nada, solo con el CLAUDE.md, solo con la skill y con ambos. Después, un juez de **otra empresa** (Codex) califica las cuatro respuestas **sin saber cuál es cuál**. Al final se genera un informe con la calificación, el tiempo, los tokens utilizados y los rechazos de cada condición, además de un veredicto: si la skill ayuda, no cambia nada o perjudica, y si el CLAUDE.md y la skill entran en conflicto. Funciona con tu suscripción de Claude Code y Codex, sin clave de API.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/skill-quatro-condicoes/guia/es/**

## Cómo empezar, sin programar

Abre Claude Code (o Codex) en tu carpeta de trabajo y pega esta solicitud. La IA lee el kit, te muestra el plan y solo lo ejecuta cuando le digas que sí.

```text
Lee el kit "Prueba de la Skill" en https://github.com/inematds/skill-quatro-condicoes (el README explica todo, incluida la instalación).
Después revisa mis skills y mi CLAUDE.md y respóndeme en español sencillo:
1. ¿Qué skill uso más y qué tarea real sirve para probarla?
2. ¿Qué criterios debe usar el juez para decidir si la respuesta quedó bien?
3. ¿Cuánto tiempo llevará la prueba con 3 rondas por condición?
No ejecutes nada todavía. Muéstrame el plan y espera a que te diga que sí. Después de ejecutarla, explícame el veredicto y qué debería cambiar.
```

---

## Instalación técnica

### Empieza con tres comandos

```bash
git clone https://github.com/inematds/skill-quatro-condicoes ~/skill-quatro-condicoes
cd ~/skill-quatro-condicoes
python3 quatro.py --tarefa minha-tarefa.md --skill ~/.claude/skills/minha-skill/SKILL.md \
  --claudemd ~/.claude/CLAUDE.md --rep 3 --saida ~/quatro-$(date +%F)
```

Abre `~/quatro-<data>/relatorio.md`.

## Qué medimos realmente

Probamos una skill real para escribir guiones de Reels con el CLAUDE.md real de quien la usa. Fueron 3 rondas por condición, con Sonnet escribiendo y Codex calificando a ciegas ([informe completo](exemplos/roteirista/resultado/relatorio.md)):

| condición | calificación promedio (0–10) | tokens de entrada |
|---|---|---|
| nada | 4,3 | 15.212 |
| solo el CLAUDE.md | **6,8** | 31.500 |
| solo la skill | 5,0 | 17.930 |
| CLAUDE.md + skill | 6,2 | 34.210 |

Lo que esto mostró:
- **Juntos quedaron por debajo del CLAUDE.md por sí solo.** El kit señaló un conflicto, y sí lo había: la skill indicaba pedir «comenta la palabra X y te envío el enlace», mientras que el CLAUDE.md, más reciente, prohíbe pedir una palabra o un enlace. La skill había quedado desactualizada y nadie se había dado cuenta.
- **El CLAUDE.md duplica los tokens de entrada** (15 mil → 31 mil). Para esta tarea valió la pena. Para otra, quizá no, y para eso sirve la prueba.
- **Una sola ronda puede engañar.** En la primera medición, con 2 rondas, la misma condición obtuvo 4 en una y 7 en la otra. Usa `--rep 3` o más antes de decidir.

## Cuando la IA rechaza

El informe cuenta los rechazos de cada condición. Si la IA rechaza incluso sin instrucciones, el bloqueo viene del modelo: las empresas líderes del sector prefieren bloquear cuando tienen dudas para protegerse de leyes como el AI Act europeo y del riesgo de demandas en EE. UU. En ese caso, pasa el paso mecánico a código o usa un modelo abierto. Si solo rechaza con tus instrucciones, el problema está en tu configuración. Consulta [docs/quando-a-ia-recusa.md](docs/quando-a-ia-recusa.md).

## El proceso, de principio a fin

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Escribir la tarea (la misma solicitud para las 4) | `minha-tarefa.md` | 🧠 tú |
| 2 | (Opcional) escribir los criterios del juez | `criterios.md` | 🧠 tú |
| 3 | Ejecutar las 4 condiciones, cada una en su propia carpeta | `python3 quatro.py --tarefa … --skill … --claudemd … --rep 3 --saida …` | ⚙️ script + 🤖 `claude -p` |
| 4 | El juez califica a ciegas (A/B/C/D mezcladas) | automático, al final del paso 3 | 🤖 `codex exec` |
| 5 | Leer el veredicto y el motivo de cada calificación | `relatorio.md` | 🧠 tú |
| 6 | Corregir la skill o la regla que entra en conflicto y volver a ejecutar | paso 3 | 🧠 tú + ⚙️ script |
| 7 | Repetir con cada modelo nuevo | paso 3 | 🧠 tú |

## Opciones

| opción | predeterminado | para qué |
|---|---|---|
| `--modelo` | `sonnet` | modelo que ejecuta la tarea |
| `--juiz` | `codex` | `codex` (otra empresa) o `claude` (Opus) |
| `--rep` | 1 | rondas por condición; 3 o más para decidir |
| `--pasta` | vacía | carpeta de trabajo copiada para cada ronda (tareas que modifican archivos) |
| `--com-bash` | desactivado | permite que la IA ejecute comandos dentro de la copia |
| `--criterios` | 4 criterios generales | qué debe revisar el juez |
| `--condicoes` | las 4 | ej.: `nada,skill` |

## Cómo funciona el aislamiento (y cuál es su límite)

Cada ronda usa `claude -p --safe-mode --disable-slash-commands`, que desactiva tu CLAUDE.md, tus skills, hooks y MCP. El inicio de sesión de la suscripción sigue activo. El CLAUDE.md y la skill que se prueban se agregan como texto adicional del sistema. Es una aproximación: en el uso normal la skill solo se carga cuando Claude decide usarla, mientras que aquí se incluye completa desde el principio. Por eso, la prueba mide si **el contenido** de la skill ayuda, no si su descripción hace que Claude la invoque en el momento adecuado.

## Requisitos

Python 3.8+, Claude Code con sesión iniciada en la suscripción (`claude`) y, para el juez predeterminado, Codex CLI con sesión iniciada (`codex`). Pruebas sin modelo: `python3 -m unittest discover testes`.

## Licencia

MIT.