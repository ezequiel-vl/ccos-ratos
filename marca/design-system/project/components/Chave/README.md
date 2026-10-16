# Chave
Interruptor de liga e desliga pra incluir um adicional.

Desligada: trilho `raised` com borda `line-2` e bolinha `faint`. Ligada: trilho `cta` e bolinha `on-cta`, que corre 20px. A área de clique passa dos 46 × 26px visíveis por um pseudo-elemento de 10px em volta.

**O consumidor fornece** um `<button>` com `aria-pressed` e um `aria-label` que diz o que liga ("Incluir Manutenção do Ponto"), e o texto do lado explicando o adicional e o preço.

**Use** pra adicional que soma no total. **Não use** pra escolha entre opções (isso é Seletor ou Escolha).
