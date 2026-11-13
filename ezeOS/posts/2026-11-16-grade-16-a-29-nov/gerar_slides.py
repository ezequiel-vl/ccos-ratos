"""Gera os HTMLs dos carrosséis da grade 16 a 29/11 a partir dos textos abaixo.

  python gerar_slides.py            # escreve <carrossel>/instagram/slide-XX.html
Depois renderiza: node .claude/skills/carrossel/scripts/render-motion.js <pasta absoluta>/instagram all png
"""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SETA = '<span class="chip empurra"><svg viewBox="0 0 16 16"><path d="M3 8h10M9 4l4 4-4 4"/></svg></span>'
PT = '<span class="pt">.</span>'


def pagina(n, total, corpo, dur=6500, estilo="", capa=False):
    prog = "".join('<i class="on"></i>' if i == n else "<i></i>" for i in range(1, total + 1))
    topo = ('<div class="topo"><img class="fade" src="../../_base/assets/logo-branco.png" alt="ezeOS">'
            + ('<span class="handle fade" style="--d:100">@agenciaezeos</span>' if capa else "") + "</div>")
    base = "" if capa else (f'<div class="base"><span class="handle fade" style="--d:100">@agenciaezeos</span>'
                            f'<div class="prog fade" style="--d:100">{prog}</div></div>')
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>{n:02d}</title>
<link rel="stylesheet" href="../../_base/slides.css">
<style>{estilo}</style></head>
<body data-duracao="{dur}"><div class="slide">
  {topo}
  <div class="miolo">
{corpo}
  </div>
  {base}
</div>
<script src="../../_base/slides.js"></script>
</body></html>
"""


def bloco(rotulo, texto, d):
    return f'    <div class="bloco in" style="--d:{d}"><span class="rotulo">{rotulo}</span><p>{texto}</p></div>'


def cta(pergunta, apoio, n, total):
    corpo = f"""    <p class="frase" data-palavras="300" data-passo="130" style="font-size:96px">{pergunta}</p>
    <p class="corpo in" style="--d:1700">{apoio}</p>
    <span class="pilula grande in" style="--d:2300; align-self:flex-start">Comente PONTO{SETA}</span>"""
    return pagina(n, total, corpo, 6000, ".miolo{gap:40px}")


def ficha(site_cls="site", d=2000, extra=""):
    return f"""    <div class="ficha card luz luz--anda sobe" style="--d:{d}{extra}">
      <b class="nome">Sua Clínica</b>
      <div style="display:flex; gap:14px; align-items:center"><span class="estrelas"><i></i><i></i><i></i><i></i><i></i></span><small>Aberto agora · no seu bairro</small></div>
      <div class="bts"><span class="{site_cls} in" style="--d:{d + 600}">Site</span><span>Rotas</span><span>Ligar</span><span>WhatsApp</span></div>
    </div>"""


# ------------------------------------------------------------ 01 · seg 16/11 · botão Site
def botao_site():
    T = 8
    s = {}
    s[1] = pagina(1, T, f"""    <h1 class="frase" data-palavras="200" data-passo="110">Pra onde vai o botão "Site" da sua ficha do Google?</h1>
    <p class="lead ink in" style="--d:1500">Quem toca ali já decidiu procurar você. O que acontece depois decide se ele chama ou desiste.</p>
{ficha(d=2300, extra="; position:absolute; left:88px; right:88px; bottom:96px")}""",
                  7000, ".miolo{justify-content:flex-start; padding-top:80px; gap:30px} .frase{font-size:88px}", capa=True)
    s[2] = pagina(2, T, f"""    <p class="lead in" style="--d:200">Existem três destinos possíveis:</p>
    <ul class="linhas">
      <li class="in" style="--d:700"><i class="bola acende" style="--d:900"></i><span><b>Lugar nenhum.</b> O botão nem aparece.</span></li>
      <li class="in" style="--d:1200"><i class="bola acende" style="--d:1400"></i><span><b>O seu Instagram.</b> O mais comum.</span></li>
      <li class="in" style="--d:1700"><i class="bola acende" style="--d:1900"></i><span><b>Uma página sua.</b> O único que trabalha por você.</span></li>
    </ul>
    <p class="corpo in" style="--d:2500">Vamos ver o que o paciente encontra em cada um.</p>""", 6500)
    s[3] = pagina(3, T, f"""    <span class="rotulo in" style="--d:150">Destino 1</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">O botão não existe{PT}</h2>
    <div class="linha risca" style="--d:900"></div>
{bloco("O que acontece", "Sem site, a ficha mostra Ligar, Rotas e WhatsApp. Quem queria entender o procedimento antes de chamar não tem onde ler.", 1200)}
{bloco("O resultado", "A pessoa volta pra busca e toca no próximo da lista. Que normalmente tem site.", 1900)}""", 7000)
    s[4] = pagina(4, T, f"""    <span class="rotulo in" style="--d:150">Destino 2</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">O seu Instagram{PT}</h2>
    <div class="linha risca" style="--d:900"></div>
{bloco("O que acontece", "A pessoa cai num feed. Pra achar procedimento, valor e endereço, precisa rolar, abrir destaque, ler legenda.", 1200)}
{bloco("O resultado", "No celular, com pressa, ela fecha. O Instagram foi feito pra quem já te segue, não pra quem acabou de te achar.", 1900)}""", 7000)
    s[5] = pagina(5, T, f"""    <span class="rotulo in" style="--d:150">Destino 3</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">Uma página sua{PT}</h2>
    <div class="linha risca" style="--d:900"></div>
{bloco("O que acontece", "Em poucos segundos ela vê o que você faz, onde fica, como é o atendimento e como agendar.", 1200)}
{bloco("O resultado", "O botão do WhatsApp já abre com a mensagem escrita. Ela chama sabendo o que quer.", 1900)}""", 7000)
    s[6] = pagina(6, T, f"""    <p class="frase" data-palavras="200" data-passo="120" style="font-size:84px">Quem procura você no Google já está decidindo{PT}</p>
    <div class="linha risca" style="--d:1600"></div>
    <p class="sub in" style="--d:1900">Quem vê o seu post ainda está rolando o feed.</p>
    <p class="corpo in" style="--d:2500">Por isso o destino do botão "Site" pesa mais do que parece.</p>""", 6500, ".miolo{gap:36px}")
    s[7] = pagina(7, T, f"""    <span class="rotulo in" style="--d:150">Faça o teste agora</span>
    <ul class="linhas" style="gap:26px">
      <li class="in" style="--d:600"><i class="bola acende" style="--d:800"></i><span>Busque o nome da sua clínica no Google, pelo celular.</span></li>
      <li class="in" style="--d:1100"><i class="bola acende" style="--d:1300"></i><span>Toque em "Site".</span></li>
      <li class="in" style="--d:1600"><i class="bola acende" style="--d:1800"></i><span>Conte quantos toques até descobrir como agendar.</span></li>
    </ul>
    <p class="titulo" data-palavras="2400" data-passo="110" style="margin-top:20px">Mais de dois já é demais{PT}</p>""", 7000, ".miolo{gap:40px} .linhas li{font-size:38px}")
    s[8] = cta("Quer que eu faça esse teste por você?",
               "Eu olho a sua ficha do jeito que o seu paciente olha e te mando os prints no direct.", 8, T)
    return s


# ------------------------------------------------------------ 03 · qui 19/11 · 5 respostas
def cinco_respostas():
    T = 7
    s = {}
    s[1] = pagina(1, T, f"""    <h1 class="frase" data-palavras="200" data-passo="110">Antes de chamar no WhatsApp, o paciente procura 5 respostas{PT}</h1>
    <p class="lead ink in" style="--d:1600">Se ele não acha, a dúvida vira mensagem. E mensagem sem resposta rápida vira desistência.</p>
    <div style="display:flex; gap:22px; margin-top:20px"><i class="bola acende" style="--d:2200"></i><i class="bola acende" style="--d:2400"></i><i class="bola acende" style="--d:2600"></i><i class="bola acende" style="--d:2800"></i><i class="bola acende" style="--d:3000"></i></div>""",
                  7000, ".miolo{gap:40px} .frase{font-size:96px} .bola{width:22px; height:22px}", capa=True)
    itens = [
        ("1", "O procedimento explicado", "O que é, pra quem é indicado, quanto tempo dura o resultado. Em palavras de paciente, não de congresso."),
        ("2", "Quem vai atender", "Foto, formação, registro do conselho. É o rosto que faz alguém confiar o próprio rosto a você."),
        ("3", "Onde fica", "Endereço, mapa, se tem onde estacionar. Parece óbvio até alguém desistir porque não sabia como chegar."),
        ("4", "Como é o processo", "Avaliação, procedimento, retorno. Saber o caminho tira o medo da primeira vez."),
        ("5", "Como agendar", "Um botão. WhatsApp com a mensagem já escrita. Nada de formulário com doze campos."),
    ]
    for i, (num, tit, txt) in enumerate(itens, start=2):
        s[i] = pagina(i, T, f"""    <span class="rotulo in" style="--d:150">Resposta {num} de 5</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">{tit}{PT}</h2>
    <div class="linha risca" style="--d:1000"></div>
    <p class="lead ink in" style="--d:1300; font-size:44px; line-height:1.35">{txt}</p>""", 6500, ".miolo{gap:36px}")
    s[7] = cta("O seu Instagram responde as 5 em dez segundos?",
               "Se não, a sua página precisa responder. Eu te mostro onde estão os buracos.", 7, T)
    return s


# ------------------------------------------------------------ 05 · seg 23/11 · case Renata (autorizado em 13/11)
TELA = ".tela{width:100%; height:560px; border-radius:24px; overflow:hidden; border:1px solid var(--line-2)} .tela img{width:100%; height:100%; object-fit:cover; object-position:top}"


def tela(img, d, altura=560):
    return f'    <div class="tela sobe" style="--d:{d}; height:{altura}px"><img src="../img/{img}.jpg" alt=""></div>'


NAV = (".nav{border-radius:22px; overflow:hidden; border:1px solid var(--line-2); background:#1C1C1C; box-shadow:0 40px 80px -30px rgba(0,0,0,.7)}"
       " .nav .barra{height:46px; display:flex; align-items:center; gap:9px; padding:0 18px}"
       " .nav .barra i{width:12px; height:12px; border-radius:50%; background:#3A3A3A}"
       " .nav .barra span{margin-left:14px; flex:1; height:28px; border-radius:999px; background:#111; color:var(--mute); font:500 17px/28px var(--mono); padding:0 16px}"
       " .nav img{display:block; width:100%}")


def navegador(img, d, extra=""):
    return (f'    <div class="nav sobe" style="--d:{d}{extra}"><div class="barra"><i></i><i></i><i></i>'
            f'<span>drarenataoliveira.com.br</span></div><img src="../img/{img}.jpg" alt=""></div>')


def tela_site(n, T, texto, img):
    return pagina(n, T, f"""    <p class="lead ink in" style="--d:200; font-size:40px; line-height:1.3">{texto}</p>
{navegador(img, 700)}""", 6500, ".miolo{gap:44px} " + NAV)


def case_renata():
    T = 10
    s = {}
    s[1] = pagina(1, T, f"""    <span class="rotulo in" style="--d:150">Case real</span>
    <h1 class="frase" data-palavras="300" data-passo="110">A clínica que só tinha Instagram{PT}</h1>
    <p class="lead ink in" style="--d:1400">Como ficou a Dra. Renata Oliveira, de São Sebastião do Caí, depois de ganhar um endereço próprio.</p>
{navegador("d-hero", 1900, "; margin-top:16px")}""", 7000, ".miolo{gap:28px; justify-content:flex-start; padding-top:40px} .frase{font-size:88px} " + NAV, capa=True)
    s[2] = pagina(2, T, f"""    <span class="rotulo in" style="--d:150">Antes</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">Tudo dependia do feed{PT}</h2>
    <div class="linha risca" style="--d:900"></div>
    <ul class="linhas">
      <li class="in" style="--d:1200"><i class="bola"></i><span>A ficha do Google não tinha botão de site.</span></li>
      <li class="in" style="--d:1600"><i class="bola"></i><span>O link da bio levava direto pro WhatsApp.</span></li>
      <li class="in" style="--d:2000"><i class="bola"></i><span>Procedimento e resultado, só rolando o feed.</span></li>
    </ul>""", 6500, ".miolo{gap:36px} .linhas{gap:28px} .linhas li{font-size:40px}")
    s[3] = pagina(3, T, f"""    <span class="rotulo in" style="--d:150">O que foi feito</span>
    <ul class="linhas" style="gap:26px">
      <li class="in" style="--d:500"><i class="bola acende" style="--d:700"></i><span><b>Domínio no nome dela:</b> drarenataoliveira.com.br</span></li>
      <li class="in" style="--d:1000"><i class="bola acende" style="--d:1200"></i><span><b>Site com a identidade do Instagram,</b> as mesmas cores, fotos e jeito de falar.</span></li>
      <li class="in" style="--d:1500"><i class="bola acende" style="--d:1700"></i><span><b>Ficha do Google ligada ao site,</b> com o botão "Site" levando pra casa dela.</span></li>
    </ul>""", 6500, ".miolo{gap:36px} .linhas li{font-size:40px}")
    s[4] = tela_site(4, T, "Ela se apresenta do jeito dela: foto, história e o que acredita sobre beleza.", "d-sobre")
    s[5] = tela_site(5, T, "Quem é a Renata, contado com as fotos e o jeito dela, antes da primeira mensagem.", "d-bento")
    s[6] = tela_site(6, T, "Cada procedimento explicado. A paciente marca o que quer e isso já vai junto na mensagem.", "d-proced")
    s[7] = tela_site(7, T, "Os resultados organizados por área, fora do feed e com autorização das pacientes.", "d-result")
    s[8] = tela_site(8, T, "A paciente escolhe o que quer melhorar e a mensagem do WhatsApp já sai escrita.", "d-conversa")
    s[9] = tela_site(9, T, "Endereço, mapa e horário. E o botão \"Site\" da ficha do Google agora leva pra cá.", "d-visita")
    s[10] = cta("Quer ver como ficaria a sua clínica?",
                "Eu olho o seu Instagram e a sua ficha do Google e te mostro o que entraria no seu site.", 10, T)
    return s


# ------------------------------------------------------------ 07 · qui 26/11 · o que entra num site de clínica
def o_que_entra():
    T = 8
    s = {}
    s[1] = pagina(1, T, f"""    <h1 class="frase" data-palavras="200" data-passo="110">O que entra num site de clínica{PT}</h1>
    <p class="sub in" style="--d:1300">E o que é enfeite.</p>
    <p class="lead ink in" style="--d:1800">Site bom de clínica é curto, claro e leva pro WhatsApp. O resto atrasa a paciente.</p>""",
                  6500, ".miolo{gap:36px} .frase{font-size:100px}", capa=True)
    entra = [
        ("Entra", "Uma primeira tela que responde tudo", "Quem atende, onde fica e como agendar, antes de rolar."),
        ("Entra", "Uma seção por procedimento", "O que é, pra quem é, quanto tempo dura. Em palavra de paciente."),
        ("Entra", "Resultados reais", "Antes e depois organizados por área, sempre com autorização da paciente."),
        ("Entra", "O caminho até você", "WhatsApp com a mensagem pronta, mapa e a ficha do Google ligada no botão \"Site\"."),
    ]
    for i, (rot, tit, txt) in enumerate(entra, start=2):
        s[i] = pagina(i, T, f"""    <span class="rotulo in" style="--d:150">{rot}</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">{tit}{PT}</h2>
    <div class="linha risca" style="--d:1000"></div>
    <p class="lead ink in" style="--d:1300; font-size:44px; line-height:1.35">{txt}</p>""", 6500, ".miolo{gap:36px}")
    s[6] = pagina(6, T, f"""    <span class="rotulo in" style="--d:150">Não precisa</span>
    <ul class="linhas">
      <li class="in" style="--d:600"><i class="bola"></i><span><b class="riscado" style="--d:2200">Blog que ninguém atualiza.</b></span></li>
      <li class="in" style="--d:900"><i class="bola"></i><span><b class="riscado" style="--d:2500">Animação que pesa no celular.</b></span></li>
      <li class="in" style="--d:1200"><i class="bola"></i><span><b class="riscado" style="--d:2800">Dez páginas dizendo a mesma coisa.</b></span></li>
      <li class="in" style="--d:1500"><i class="bola"></i><span><b class="riscado" style="--d:3100">Formulário com doze campos.</b></span></li>
    </ul>
    <p class="corpo in" style="--d:3500">Cada item desses é um motivo a mais pra paciente fechar a aba.</p>""", 7000, ".miolo{gap:36px} .linhas{gap:26px} .linhas li{font-size:42px} .corpo{font-size:34px}")
    s[7] = pagina(7, T, f"""    <span class="rotulo in" style="--d:150">E o mais importante</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">Tudo no seu nome{PT}</h2>
    <div class="linha risca" style="--d:1000"></div>
    <p class="lead ink in" style="--d:1300; font-size:44px; line-height:1.35">Domínio, hospedagem e acesso registrados no seu nome desde o primeiro dia. Se um dia você trocar de fornecedor, o site vai junto.</p>""", 6500, ".miolo{gap:36px}")
    s[8] = cta("Quer uma proposta pra sua clínica?",
               "Eu olho a sua presença hoje e te mando o que entraria no seu site, no direct.", 8, T)
    return s


# ------------------------------------------------------------ 02b · versão carrossel do Reel da Renata (slide 1 = vídeo das abas, Remotion)
CEL = (".duo{display:grid; grid-template-columns:1fr 440px; gap:48px; align-items:center}"
       " .cel{width:440px; height:900px; border-radius:58px; padding:14px; background:#050505; border:2px solid var(--line-2); box-shadow:0 50px 90px -30px rgba(0,0,0,.8)}"
       " .cel div{width:100%; height:100%; border-radius:46px; overflow:hidden; background:#F4F1EC}"
       " .cel img{width:100%; display:block}")


def cel_slide(n, T, rotulo, titulo, texto, img):
    return pagina(n, T, f"""    <div class="duo">
      <div style="display:grid; gap:28px">
        <span class="rotulo in" style="--d:150">{rotulo}</span>
        <h2 class="titulo" data-palavras="300" data-passo="100" style="font-size:64px">{titulo}{PT}</h2>
        <p class="lead ink in" style="--d:1100; font-size:36px; line-height:1.35">{texto}</p>
      </div>
      <div class="cel sobe" style="--d:500"><div><img src="../img/{img}.jpg" alt=""></div></div>
    </div>""", 6500, CEL)


def carrossel_renata():
    T = 9
    s = {}
    s[2] = pagina(2, T, f"""    <span class="rotulo in" style="--d:150">Antes</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">Uma ficha sem pra onde mandar{PT}</h2>
{ficha(d=900)}
    <p class="lead ink in" style="--d:1800; font-size:40px; line-height:1.35">Sem botão de site. Quem queria ver os procedimentos antes de chamar só tinha o feed do Instagram.</p>""",
                  6500, ".miolo{gap:40px}").replace("Sua Clínica", "Renata Oliveira Estética").replace(
        '<span class="site in" style="--d:1500">Site</span><span>Rotas</span><span>Ligar</span><span>WhatsApp</span>',
        '<span>Rotas</span><span>Ligar</span><span>WhatsApp</span>')
    s[3] = cel_slide(3, T, "Depois", "Um endereço no nome dela", "No celular, que é onde a paciente procura. A primeira tela já diz quem atende, onde e como agendar.", "1-hero")
    s[4] = cel_slide(4, T, "Identidade", "Com a cara do Instagram dela", "As mesmas fotos, as mesmas cores e o mesmo jeito de falar. A paciente reconhece na hora.", "2-naturalidade")
    s[5] = cel_slide(5, T, "Procedimentos", "Cada um explicado", "A paciente abre a aba, entende o procedimento e a escolha já vai junto na mensagem.", "5-procedimentos")
    s[6] = cel_slide(6, T, "Resultados", "Fora do feed", "Antes e depois organizados por área, com autorização das pacientes.", "6-resultados")
    s[7] = cel_slide(7, T, "Contato", "O WhatsApp a um toque", "Um botão que já abre a conversa com a mensagem escrita. Sem formulário, sem rolar o feed.", "4-avaliacao")
    s[8] = pagina(8, T, f"""    <span class="rotulo in" style="--d:150">E no Google</span>
    <h2 class="titulo" data-palavras="300" data-passo="100">O botão "Site" agora leva pro site dela{PT}</h2>
{ficha(d=1000)}
    <p class="lead ink in" style="--d:1800; font-family:var(--mono); font-size:38px">drarenataoliveira.com.br</p>""",
                  6500, ".miolo{gap:40px}").replace("Sua Clínica", "Renata Oliveira Estética")
    s[9] = cta("Quer ver como ficaria a sua clínica?",
               "Eu olho o seu Instagram e a sua ficha do Google e te mostro o que entraria no seu site.", 9, T)
    return s


def escrever(pasta, slides):
    destino = os.path.join(AQUI, pasta, "instagram")
    os.makedirs(destino, exist_ok=True)
    for n, html in slides.items():
        with open(os.path.join(destino, f"slide-{n:02d}.html"), "w", encoding="utf-8") as f:
            f.write(html)
    print(f"{pasta}: {len(slides)} slides")


if __name__ == "__main__":
    escrever("01-botao-site", botao_site())
    escrever("03-cinco-respostas", cinco_respostas())
    escrever("05-case-renata", case_renata())
    escrever("07-o-que-entra", o_que_entra())
    escrever("02b-carrossel-renata", carrossel_renata())
