# site-stageshow

Teste do site da ezeOS com o hero feito pela skill Stageshow (benjitaylor/skills). O oficial continua em `../site/` e no ar em ezeos.com.br; esta pasta é só a versão de comparação, com `noindex`.

O que muda em relação ao oficial: o painel "relevo" do hero (navegador montando com o endereço digitado) saiu e no lugar entrou uma demo animada: a clínica aparece na busca, o cursor abre o site, toca em "Agendar pelo WhatsApp" e a mensagem chega no celular do dono. Todo o resto é igual.

- Fonte da demo: `_src/hero/` (componente React), `_src/kit/` (kit da Stageshow copiado)
- Gerar de novo depois de mexer: `node _src/build.mjs` (usa o node_modules da skill em `~/.claude/skills/stageshow`, nada instala aqui)
- Saída: `assets/demo.js`, `assets/kit/stageshow.css`, `assets/demo-ezeos.css`
- Publicar: copiar `index.html`, `favicon.ico` e `assets/` pra `_publicado/ezeos-stageshow/` e rodar o deploy da `/publicar-site`
- Notas do ensaio: `_src/hero/REHEARSAL.md`
