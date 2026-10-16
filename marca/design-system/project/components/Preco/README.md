# Preco
Valor grande com algarismos que rolam até o preço quando a oferta muda.

`R$` em `mute`, valor no estilo `preco` com algarismos tabulares. Cada dígito é uma tira de 0 a 9 que desliza por `transform` em 1s.

**O consumidor fornece** o preço no formato `0.000` (todos os da escada têm 5 caracteres: 1.800, 5.000, 6.000) e um `aria-label` com o valor por extenso no container, porque os dígitos visuais ficam `aria-hidden`. Escreva o valor estático no HTML: o script só substitui.

**Use** no card de preço. **Não use** pra métrica de resultado de cliente: número inventado queima a marca.
