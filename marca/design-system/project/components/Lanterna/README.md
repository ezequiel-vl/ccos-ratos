# Lanterna
Luz radial de 420px que segue o cursor dentro do card e acende quando o mouse entra.

Ponha `eze-luz` no card. Um único `pointermove` delegado no documento grava `--lx` e `--ly` (a posição do cursor dentro do card); o CSS faz o resto. Cor `luz`.

- **Atrás do texto** (padrão): o card ilumina e a leitura não perde contraste.
- **Por cima** (`eze-luz--sobre`): só em ilustração, como o painel do navegador, onde vira reflexo no vidro.

**O consumidor fornece** um card com borda e superfície, e o script de posição (abaixo).

```js
if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.addEventListener('pointermove', e => {
    const el = e.target.closest && e.target.closest('.eze-luz'); if (!el) return;
    const r = el.getBoundingClientRect();
    el.style.setProperty('--lx', (e.clientX - r.left) + 'px');
    el.style.setProperty('--ly', (e.clientY - r.top) + 'px');
  }, { passive: true });
}
```

**Faça**: painel, card de pergunta, card de preço, card de lista. Em peça estática (carrossel, slide), deixe a luz fixa sobre o número ou a frase principal.

**Não faça**: em botão (ele tem o próprio brilho), em bloco sem borda, ou com a luz acima do texto em card de leitura. Em celular não aparece, porque não há cursor.
