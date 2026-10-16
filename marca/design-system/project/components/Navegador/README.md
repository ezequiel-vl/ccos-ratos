# Navegador
Painel de navegador que mostra a empresa do cliente instalada, com a barra de endereço e o status no ar.

Barra em `sunk` com três bolinhas `skel`, endereço em `endereco` dentro de uma pílula `raised`, e o status: ponto `dot` com `halo-no-ar` e o rótulo "no ar". Painel em `surface`, borda `line-2`, raio `radius-painel`. Leva lanterna por cima (`eze-luz eze-luz--sobre`).

**O consumidor fornece** o endereço (`suaempresa.com.br` no genérico, o domínio real num case) e o miolo da tela.

**No hero do site**: o painel se monta em perspectiva (rotateX 9°), digita o endereço letra por letra (70ms cada), acende o "no ar" e só então o miolo aparece. A montagem é CSS; o conteúdo existe sem JavaScript. Inclina com o cursor até 7°.

**Não use** logo ou print de empresa real sem autorização do cliente.
