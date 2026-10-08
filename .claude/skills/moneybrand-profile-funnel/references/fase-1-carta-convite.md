# Carta 3 · Carta Convite

Objetivo da parte: o aluno sai com a carta convite escrita e a chamada definida.

Ideia da carta: o número que mais move vendas é quantas pessoas viram a oferta. O dinheiro do perfil é proporcional aos caminhos que levam até ela. 3 jeitos de perder dinheiro: perfil sem oferta, aplicação e call no meio do caminho, produto barato na bio esperando que a pessoa suba pro caro.

## Parada 7 · A carta convite

Aqui você escreve o rascunho, usando só o que o aluno decidiu nas partes 1 e 2 e o que ele responder nesta parada.

A carta tem 2 versões. As duas usam os mesmos 7 blocos, na mesma ordem. A diferença é o material dentro deles.

- **Curta**, de 350 a 500 palavras: afirma a ideia e convida. Funciona quando a pessoa já confia no aluno ou quando a decisão é pequena. Referência: `fase-1-carta-curta.md`.
- **Longa**, de 700 a 900 palavras: mostra, além de afirmar. Abre com uma cena, conta de onde veio a ideia, dá um exemplo do método em ação e diz o que acontece depois do clique. Faz o trabalho que uma call de venda faria. Referência: `fase-1-carta-longa.md`.

### Passo 1 · Perguntas comuns

Pergunte, uma por vez:

- Texto ou vídeo?
- Consultoria ou mentoria (chamada pro WhatsApp, sem preço) ou infoproduto (chamada pra compra, com link)?
- Se for consultoria ou mentoria: qual palavra a pessoa manda no WhatsApp? Curta, fácil de digitar e ligada ao nome do mecanismo.
- Quem vai ler essa carta, na maior parte: gente que já conhece o seu trabalho (clientes, contatos, seguidores antigos) ou gente que vai te descobrir pelo perfil?

### Passo 2 · Sugerir a versão

Antes de perguntar qual versão ele quer, sugira uma, com o motivo em uma frase. Use o que já está na ficha e a última resposta.

| Sinal | Aponta pra curta | Aponta pra longa |
|---|---|---|
| Preço | Abaixo de R$ 3 mil, ou infoproduto de entrada | R$ 3 mil ou mais |
| Quem lê | Já conhece o trabalho do aluno | Vai descobrir o aluno pela carta |
| Bandeira | Confirma algo que a pessoa já desconfia | Contraria de frente o que a pessoa acredita |

Como decidir a sugestão:

- O preço pesa mais. De R$ 3 mil pra cima, sugira a longa, mesmo que os outros sinais apontem pra curta. Quanto mais caro, mais a carta precisa carregar sozinha.
- Abaixo de R$ 3 mil, sugira a longa só se os outros 2 sinais apontarem pra ela. Senão, sugira a curta.
- Se faltar dado pra decidir, sugira a longa. Cortar cena, origem e exemplo transforma a longa em curta em minutos. O contrário obriga a voltar e fazer as perguntas que faltaram.

Exemplo de sugestão: "Pelo preço de R$ 4.800 e porque a maioria vai te descobrir pelo perfil, eu sugiro a longa. Quer seguir com ela ou prefere a curta?"

O aluno decide. Se ele escolher a curta com preço de R$ 3 mil ou mais, avise uma vez que a carta vai ficar mais afirmativa do que o preço pede, e respeite a escolha.

Se ele quiser as duas, faça a longa primeiro e corte pra chegar na curta. A longa fica no perfil. A curta serve pras mensagens da parada 8, pra quem já conhece o trabalho dele.

### Passo 3 · Montar

Leia a referência da versão escolhida e siga as perguntas e os blocos dela.

### Tom, pras duas versões

Escreva como convite privado pra algo exclusivo, não como página de vendas. Parágrafos curtos, uma ideia por linha. Sem exagero, sem urgência falsa, sem caixa alta gritando. Não coloque FAQ, garantia, lista de bônus nem contador. Isso transforma carta em página de vendas. Abra falando com a pessoa, como numa carta ("E aí, [nome] aqui.").

### Conferência, pras duas versões

Confira com o aluno e mostre o resultado de cada item, junto com os itens da referência da versão:

- Os 7 blocos estão na ordem?
- Tudo veio do que ele decidiu ou respondeu, sem nada inventado?
- O tamanho está na faixa da versão?
- Entre ler a carta e chegar na conversa existe só um clique, sem aplicação, espera ou call?
- Se for consultoria ou mentoria, está sem preço?
- Fala com a pessoa dele, não com uma categoria?

Ajuste um bloco por vez, se ele pedir.

## Onde a carta mora

Uma página simples, com cara de documento: fundo branco, uma coluna, título, a carta e a chamada no fim. Nada de contador, pop-up ou botão piscando. Se for vídeo: o vídeo no topo, 2 ou 3 linhas de texto e a chamada. A página vai ao ar na Fase 3. Use o script `scripts/montar_carta_convite.py` pra gerar a página.

Como os blocos entram no JSON do script:

- `pre_headline` e `headline`: blocos 1 e 2.
- `abertura`: a saudação e a apresentação em uma ou duas linhas.
- `secoes`, nesta ordem: o problema (sem título), a solução (sem título, benefícios em `lista`) e o método (título "O método: [Nome]", em `passos`). Na longa, entra mais uma seção depois do método: o exemplo (título curto, em `paragrafos`).
- `provas`: bloco 6. Vazio mostra o espaço reservado pras provas que vão chegar.
- `chamada_paragrafos`, `chamada_botao` e `chamada_link`: bloco 7. O link do WhatsApp pode levar a palavra pronta: `https://wa.me/55DDDNUMERO?text=PALAVRA`.
