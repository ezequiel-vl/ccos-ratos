---
name: proposta-ponto
description: >
  Gera e publica a proposta do Ponto Digital pra uma clínica da lista quente (GMN feito pela
  ezeOS, sem site): recebe o nome da clínica e os números da ficha do Google, preenche o modelo
  com o diagnóstico das quatro portas, publica no Cloudflare e devolve o link com a mensagem de
  WhatsApp pronta. Use quando o usuário disser "proposta do ponto", "proposta pra [clínica]",
  "manda proposta do Ponto Digital", "/proposta-ponto", ou passar números de uma ficha do Google
  pedindo proposta.
---

# /proposta-ponto: proposta do Ponto Digital em link

Entrada: clínica + números da ficha + resultado do teste das quatro portas.
Saída: link `https://ezeos-publicacoes.pages.dev/proposta-<clinica>/` e a mensagem pra mandar.

Fontes (não duplicar conteúdo aqui, ler de lá):
- Modelo: `ezeOS/ofertas/2026-10-16-ponto-digital/proposta-modelo.html`
- Escopo, preço, pagamento, garantia: `ezeOS/ofertas/2026-10-16-ponto-digital/oferta.md`
- Como levantar os números e o que dizer: `ezeOS/ofertas/2026-10-16-ponto-digital/script-whatsapp.md`
- Preenchimento: `preencher.py`, nesta pasta

## Regra que não se negocia

Número nenhum é inventado. Visualizações, concorrente e resultado das portas vêm do Ezequiel, tirados do painel e do teste no celular. Se faltar, pergunta. Sem o número de visualizações, não gera.

## 1. Coletar os dados

Se a clínica tiver pasta em `clientes/`, ler o `briefing.md` pra puxar nome, serviço principal e bairro antes de perguntar.

Perguntar numa mensagem só o que faltar:

| Campo | O que é | Exemplo |
| --- | --- | --- |
| `clinica` | nome como ela usa | Dra. Carina Cerveira |
| `nome` | quem decide (opcional, usado na mensagem) | Carina |
| `visualizacoes` | visualizações do perfil no painel | 1284 |
| `periodo` | período desse número | setembro de 2026 |
| `servico` | serviço mais caro ou que mais quer vender, em minúscula | harmonização facial |
| `bairro` | bairro usado na busca, em minúscula | jardim esplanada |
| `portas` | resultado das 4 portas: `nome`, `busca`, `site`, `email`, cada uma `ok` ou `falhou` | |
| `concorrente` | quem aparece antes na busca (obrigatório se `busca` falhou) | OdontoVida |
| `concorrente_tem_site` | se a concorrente tem site na ficha (padrão `true`) | |
| `email_provedor` | se a porta do e-mail falhou e não for @gmail | @hotmail |
| `dominio` | domínio sugerido, livre no Registro.br | dracarinacerveira.com.br |

Se o Ezequiel mandar só o print do painel, ler o número da imagem e confirmar com ele antes de usar.

Domínio: sugerir o nome da clínica sem acento e sem espaço + `.com.br`, e lembrar o Ezequiel de checar se está livre em registro.br antes de mandar. Não afirmar que está livre.

Se a porta do site passou (a clínica já tem site ligado), parar: essa proposta não serve. Avisar e perguntar como ele quer seguir.

## 2. Gerar

Salvar os dados em `propostas/<AAAA-MM-DD>-ponto-digital-<slug>.json` (pasta fora do git, é dado de cliente) e rodar:

```bash
python .claude/skills/proposta-ponto/preencher.py propostas/<arquivo>.json propostas/<AAAA-MM-DD>-ponto-digital-<slug>.html
```

O script calcula data e validade (7 dias), monta as frases das portas, escapa o HTML e recusa se sobrar campo sem trocar. Ele imprime o slug de publicação (`proposta-<clinica>`).

Se der erro, mostrar a mensagem e pedir o dado que falta. Não editar o HTML gerado à mão pra contornar: corrigir o JSON e rodar de novo. Se o texto do modelo precisar mudar, mudar no modelo (vale pra todas as próximas).

## 3. Conferir antes de publicar

Ler o trecho do diagnóstico no HTML gerado (o número, a frase da busca, as quatro portas) e conferir se bate com o que o Ezequiel passou. Mostrar pra ele em 3 linhas:

> Visualizações: 1.284 (setembro de 2026)
> Portas: nome ok, busca falhou (OdontoVida na frente), site falhou, e-mail falhou
> Domínio sugerido: sorrisoecia.com.br (confere no registro.br)

Publicar só depois do ok dele.

## 4. Publicar

Seguir a skill `/publicar-site` com o HTML gerado e o slug que o script imprimiu. A página já sai com `noindex`.

## 5. Entregar

Devolver o link e a mensagem pronta, no tom do script:

> Pronto, [NOME]. Montei a proposta com os números da tua ficha, o que entra, o prazo e o investimento:
> https://ezeos-publicacoes.pages.dev/proposta-<clinica>/
>
> Dá uma olhada com calma. Qualquer dúvida me chama que eu explico por áudio.

E lembrar do follow-up do script: dia 2, dia 5 (com print novo da busca) e dia 12.

## Regras

- Tom, preço, escopo e garantia vêm do modelo e do `oferta.md`. A skill não reescreve nada disso por cliente
- "Redes sociais", nunca só "redes"
- Proposta de cliente fica em `propostas/`, que é ignorada pelo git. O modelo e a skill ficam versionados
