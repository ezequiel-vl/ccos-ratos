# Seletor
Trilho de abas em pílula com um indicador que desliza até a opção escolhida.

O trilho é `sunk` com borda `line`; o indicador é `cta` e se move por `clip-path` (sem animar largura, que força layout). A aba ativa fica em `on-cta`, as outras em `mute`. Cada aba tem 44px de altura.

**O consumidor fornece** os botões com `role="tab"` e `aria-selected`, e o script que grava `--l` e `--r` (distância do indicador até as bordas) no `.eze-seletor__ind`. Abaixo de 520px use rótulos curtos ("Ponto", "Demanda", "Completo").

**Use** pra trocar entre ofertas no card de preço. **Não use** pra navegação de página nem com mais de 4 opções. Sem JavaScript, pinte a aba ativa com `cta` direto, senão o texto some.
