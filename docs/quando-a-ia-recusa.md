# Quando a IA de fronteira recusa uma tarefa normal

Você pede uma coisa comum, como um texto de venda, um ajuste num arquivo seu ou um passo repetitivo de uma automação, e o Claude, o ChatGPT ou o Gemini responde "não posso ajudar com isso". Muita gente acha que errou no pedido. Muitas vezes não errou.

## Por que isso acontece

As empresas que fazem as IAs de fronteira trabalham sob as leis dos países onde vendem. As principais são o AI Act da União Europeia, que entrou em vigor em 2024 com obrigações em etapas, e, nos Estados Unidos, leis estaduais e o risco de processo. Para se proteger, elas treinam o modelo para recusar na dúvida, e essa trava vale para o mundo inteiro, inclusive em países onde essas leis são questionadas ou nem se aplicam. O resultado é um modelo que às vezes recusa coisa legítima.

A recusa também muda de uma conversa para outra. Na mesma semana, o mesmo pedido pode ser recusado num projeto e aceito numa conversa nova. Contexto acumulado, instruções que confundem e mudanças de versão do modelo mexem nisso.

## Três saídas, da mais simples à mais forte

1. **Teste se a culpa é da sua configuração.** Rode o pedido nas quatro condições deste kit. O relatório conta as recusas de cada uma:
   - se recusa até em **nada** (sem CLAUDE.md e sem skill), a trava é do modelo;
   - se só recusa **com as suas instruções**, alguma regra sua está atrapalhando: ache e reescreva.
2. **Passe o passo mecânico para código.** Se a tarefa é sempre igual (tirar um campo, trocar um texto, mover arquivos, formatar), ela não precisa de IA a cada vez. Peça à IA para escrever **uma vez** um script que faz o passo e depois rode o script. O script não tem opinião, não recusa e custa zero por execução. A IA fica com a parte que precisa de julgamento.
3. **Use um modelo aberto, sem as travas da empresa.** Modelos de pesos abertos rodam na sua máquina e podem ser ajustados para recusar menos. O kit [Modelo do Seu Jeito](https://inematds.github.io/modelo-do-seu-jeito/guia/) mostra como fazer isso com o Heretic e como medir o antes e o depois. Bom para tarefas que o modelo fechado trava sem motivo, como texto, análise e conteúdo sensível porém legítimo.

## Lembrete

Tirar a trava do modelo não tira a sua responsabilidade: o que você publica continua respondendo às regras do lugar onde publica (a plataforma, o seu país).
