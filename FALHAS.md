# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-11-23 | Pages: `deploy-pages` falhou 4× com "No artifacts named github-pages" (o artifact existia; build e deploy no mesmo job) | build e deploy em jobs separados (`needs: build`) | infra |
