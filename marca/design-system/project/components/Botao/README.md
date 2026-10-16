# Botao
Pílula sólida com chip de seta pra ação principal e pílula de vidro pra secundária.

- **`eze-btn eze-btn--claro`**: ação principal. Fundo `cta`, texto `on-cta`, chip de 34px com seta que anda 3px no hover. Um por bloco.
- **`eze-btn eze-btn--vidro`**: ação secundária. Fundo `vidro`, borda `vidro-borda`; sob o cursor a borda vira `vidro-borda-hover` e um brilho de 120px (`vidro-brilho`) segue o mouse via `--mx`/`--my`. No claro vira contorno transparente.
- **`eze-btn--sm`**: 44px de altura, pro menu.

Altura mínima 46px (44px no `sm`), estado `:active` com escala .97 e foco com anel de 2px em `ink`.

**O consumidor fornece** o rótulo e, no claro, o `<span class="eze-chip">` com a seta; no vidro, o texto dentro de `<span>`.

**Texto do botão**: verbo que diz o que acontece. "Fazer o teste de 1 minuto", "Chamar no WhatsApp", "Quero o Ponto Digital". Quando a ação muda, o rótulo muda junto ("Mandar meu resultado no WhatsApp" só depois do teste respondido).

**Não faça**: ícone decorativo além da seta, dois botões claros lado a lado, cor de marca no botão da casa.
