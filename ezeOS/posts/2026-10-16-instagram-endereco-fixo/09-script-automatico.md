# Script Automático

**Onde roda:** no direct do Instagram (ManyChat), disparado por quem comenta ou manda PONTO. O mesmo fluxo pode rodar no WhatsApp Business.

**Estrutura (8 blocos):** nome, promessa, o que não precisa, como funciona, os passos, a proposta, a qualificação, o fechamento.

**Objetivo:** substituir a primeira reunião. Quem chega no fim já sabe o que é o Ponto Digital, quanto custa e quanto tempo leva, e já me passou os dados pro diagnóstico das quatro portas. Eu só entro pra mandar o diagnóstico e a proposta.

**Relação com a Isca:** este fluxo engloba a resposta automática do `06-isca-diagnostico.md`. Os dados do diagnóstico (empresa, serviço, bairro) são pedidos no bloco 7. Sem ManyChat, usar a resposta simples da Isca.

**Tom:** direct é conversa minha, então vai em "tu". Sem emoji.

**Adaptação da skill:** o bloco 2 da skill promete "pelo menos R$ X por mês a mais no caixa". Sem número real de cliente, a promessa fica no que eu controlo: prazo e entrega.

---

## Bloco 1: nome

> Oi! Aqui é o Ezequiel, da ezeOS.
>
> Antes de tudo, me diz teu primeiro nome?

*[usuário digita]*

---

## Bloco 2: promessa

> [nome], direto ao ponto.
>
> Em 10 dias eu deixo a tua empresa encontrada em qualquer lugar onde o cliente procurar: no Google pelo nome, no Google pelo serviço com o bairro, no botão de site da tua ficha e no teu e-mail.
>
> Tudo no teu nome, ligado e funcionando.
>
> Quer ver como funciona?

**Botão:** Quero ver

---

## Bloco 3: o que não precisa

> Pra isso tu não precisa:
>
> · postar todo dia
> · gravar vídeo dançando
> · aprender ferramenta de anúncio
> · ficar respondendo WhatsApp de madrugada
>
> Nem precisa aparecer, se não quiser.
>
> Post, anúncio e conteúdo funcionam, e muita gente usa. Só que eles trabalham em cima de um endereço, e a maioria das empresas locais ainda não tem um. Eu começo por ele.

**Botão:** Faz sentido

---

## Bloco 4: como funciona

> O que eu instalo se chama Ponto Digital. São três frentes ligadas entre si:
>
> **Domínio e site.** Um site no teu domínio, registrado no teu CPF ou CNPJ, escrito pra aparecer na busca do teu bairro, com uma página só pro serviço que tu mais quer vender.
>
> **Ficha do Google.** Completa, com foto, serviço e horário, e com o site ligado no botão. É o que faz o Google ter o que mostrar quando alguém procura o que tu faz.
>
> **E-mail, WhatsApp e redes sociais.** E-mail no teu domínio, WhatsApp Business com catálogo e mensagem de ausência, Instagram e Facebook com o mesmo nome, a mesma foto e o mesmo link.
>
> Depois disso, todo anúncio e todo post que tu fizer têm pra onde mandar gente.

**Botão:** E como é o processo?

---

## Bloco 5: os passos

> **Primeiro passo:** uma conversa de 30 minutos por vídeo. Eu pergunto sobre a tua empresa e tu me manda logo, fotos e a lista de serviços. Dessa conversa sai o texto do site.
>
> **Segundo passo:** eu registro o domínio, crio o e-mail e configuro o WhatsApp Business contigo numa chamada de 20 minutos. Depois monto o site, a página do serviço e a ficha do Google.
>
> **Terceiro passo:** no dia 8 tu recebe o site pra aprovar e pede o que quiser ajustar. No dia 10 está tudo no ar, testado no celular, e tu recebe um vídeo mostrando onde fica cada coisa.
>
> Faz sentido pra ti?

**Botão:** Sim

---

## Bloco 6: a proposta

> Em resumo, eu vou:
>
> 1. Registrar o teu domínio e colocar o teu site no ar, ligado na ficha do Google
> 2. Completar a tua ficha do Google
> 3. Configurar o e-mail no domínio, o WhatsApp Business e as redes sociais
>
> Pra que quem procurar pelo teu serviço encontre a tua empresa pronta.
>
> São 10 dias corridos de entrega e 30 dias de suporte. O investimento é R$ 1.800, uma vez só: no Pix, metade pra começar e metade na entrega, ou no cartão em até 6x. Se eu atrasar, a segunda parcela cai pela metade.
>
> Antes de te mandar a proposta, vou fazer o diagnóstico das quatro portas da tua empresa. Pra isso preciso de umas respostas rápidas. Pode ser?

**Botão:** Pode ser

---

## Bloco 7: qualificação

> Qual o nome da tua empresa, do jeito que está no Google?

*[usuário digita]*

> Qual o teu serviço principal, o que tu mais quer vender?

*[usuário digita]*

> Em que bairro e cidade tu atende?

*[usuário digita]*

> Qual e-mail tu usa pra mandar proposta e orçamento?

*[usuário digita]*

> Hoje, de onde vem a maioria dos teus clientes novos?

**Botões:** Indicação · Instagram · Google · Anúncio · Não sei dizer

> Tua empresa já tem site?

**Botões:** Não tenho · Tenho, mas está velho · Tenho e funciona

> O investimento de R$ 1.800 (ou 6x no cartão) cabe pra ti agora?

**Botões:** Cabe · Cabe em mais de um mês · Agora não cabe

> Quantos clientes novos por mês tu atende hoje, mais ou menos? E quantos tu gostaria de atender?

*[usuário digita]*

---

## Bloco 8: fechamento

> Valeu, [nome]. Vou fazer o teste das quatro portas na [empresa] e te mando aqui os prints, um áudio explicando o que falta e a proposta.
>
> Digita só "Ok, aguardo!" pra eu ser avisado.

---

## O que eu faço com as respostas

| Resposta | O que fazer |
| --- | --- |
| "Tenho e funciona" no site | Diagnóstico normal. Se as portas estiverem abertas, oferecer o degrau seguinte (Movimento) e não o Ponto Digital |
| "Agora não cabe" | Mandar o diagnóstico mesmo assim, sem proposta. Marcar pra retomar em 30 dias com dado novo da ficha |
| "Cabe em mais de um mês" | Proposta com o cartão em 6x em destaque |
| "Cabe" | Diagnóstico + `/proposta-ponto` no mesmo dia |

A ficha do Google e o teste seguem o passo 0 do `ezeOS/ofertas/2026-10-16-ponto-digital/script-whatsapp.md`. A proposta sai com `/proposta-ponto`.
