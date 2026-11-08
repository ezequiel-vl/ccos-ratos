"""Converte a planilha de convidados (xlsx/csv) no TSV limpo que a Recepção lê: Nome, Mesa, Obs.

Uso:
  python converter-lista.py <planilha> <saida.tsv> [--aba "Lista dia"]

- Sem --aba: usa a primeira aba que tenha colunas de nome (NOME/CONVIDADO) e MESA.
- Linha "NÃO CONFIRMADOS": quem vem depois entra sem mesa, com obs "Não confirmado".
- Mesa "não vem": pula a pessoa (e avisa).
- Coluna ACOMPANHANTE preenchida: vira outra linha, mesma mesa.
- Colunas de observação/restrição: vão pra Obs.
- Nome TODO EM MAIÚSCULA vira "Nome Normal"; palavra começando em minúscula ganha maiúscula (menos da/de/dos).
- Tira caracteres invisíveis colados do WhatsApp (ex.: U+2060), que impediam a busca de achar o nome.
- Lista simples (corporativo, sem mesa nem CRM): o nome pode estar em qualquer coluna (NOME/CONVIDADO);
  GRUPO (ou INSTITUIÇÃO/EMPRESA, se não tiver grupo) vira o agrupamento e o resto (instituição, cargo,
  status) vai pra Obs. Status de confirmado (ok, confirmou presença) não entra; "não vem" pula a pessoa.
  Planilha com várias abas: sem --aba, fica a aba simples com mais nomes.
Não precisa de biblioteca externa (lê o xlsx direto do zip).
"""
import csv, io, re, sys, unicodedata, zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def norm(s):
    s = unicodedata.normalize('NFD', str(s or '')).encode('ascii', 'ignore').decode()
    return re.sub(r'\s+', ' ', s).strip().lower()


def col_idx(ref):
    n = 0
    for ch in re.sub(r'\d', '', ref):
        n = n * 26 + ord(ch) - 64
    return n - 1


def ler_xlsx(path):
    z = zipfile.ZipFile(path)
    ss = []
    if 'xl/sharedStrings.xml' in z.namelist():
        ss = [''.join(t.text or '' for t in si.iter(NS + 't')) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).iter(NS + 'si')]
    rels = {r.get('Id'): r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    abas = {}
    for s in ET.fromstring(z.read('xl/workbook.xml')).iter(NS + 'sheet'):
        alvo = rels[s.get(REL + 'id')].lstrip('/')
        alvo = alvo if alvo.startswith('xl/') else 'xl/' + alvo
        linhas = []
        for row in ET.fromstring(z.read(alvo)).iter(NS + 'row'):
            vals = {}
            for c in row.iter(NS + 'c'):
                v = c.find(NS + 'v')
                t = c.get('t')
                if t == 's' and v is not None:
                    val = ss[int(v.text)]
                elif t == 'inlineStr':
                    val = ''.join(x.text or '' for x in c.iter(NS + 't'))
                else:
                    val = v.text if v is not None else ''
                vals[col_idx(c.get('r'))] = val
            linhas.append([vals.get(i, '') for i in range(max(vals) + 1)] if vals else [])
        abas[s.get('name')] = linhas
    return abas


def ler_csv(path):
    raw = open(path, 'rb').read()
    try:
        txt = raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        txt = raw.decode('latin-1')
    dialect = csv.Sniffer().sniff(txt[:4000], delimiters='\t;,')
    return {'csv': list(csv.reader(io.StringIO(txt), dialect))}


def achar_cabecalho(linhas, simples=False):
    """Linha de cabeçalho com NOME e (MESA ou CRM). Evento sem mesa marcada usa CRM/Especialidade.
    simples=True aceita só a coluna de nome (lista corporativa sem mesa nem CRM)."""
    for i, r in enumerate(linhas[:15]):
        h = [norm(c).rstrip(':').strip() for c in r]
        nome = next((j for j, c in enumerate(h) if re.match(r'^(nome|convidad)', c)), None)
        mesa = next((j for j, c in enumerate(h) if c == 'mesa'), None)
        if mesa is None:
            mesa = next((j for j, c in enumerate(h) if c.startswith('mesa')), None)
        crm = next((j for j, c in enumerate(h) if c.startswith('crm')), None)
        esp = next((j for j, c in enumerate(h) if c.startswith('especial')), None)
        if nome is not None and (simples or mesa is not None or crm is not None or esp is not None):
            obs = [j for j, c in enumerate(h) if re.match(r'^(obs|observa|restri|nota)', c)]
            acomp = next((j for j, c in enumerate(h) if c.startswith('acompanhante')), None)
            return i, nome, mesa, obs, acomp, crm, esp
    return None


# Nomes colados do WhatsApp ou da web trazem caracteres invisíveis (ex.: U+2060 no começo) que quebram a busca
INVIS = re.compile('[­​-‏‪-‮⁠-⁤⁦-⁩﻿]')
ESPACOS = re.compile('[  -   　]')
PARTICULAS = {'da', 'de', 'do', 'das', 'dos', 'e', 'del', 'van', 'von', 'der'}


def bonito(nome):
    """Limpa invisíveis e pontuação solta e ajusta a caixa (mesma regra do app e do painel)."""
    nome = ESPACOS.sub(' ', INVIS.sub('', str(nome or '')))
    nome = re.sub(r'[,;.]+$', '', re.sub(r'\s+', ' ', nome).strip()).strip()
    tudo_maius = nome.upper() == nome
    out = []
    for i, w in enumerate(nome.split(' ')):
        if i > 0 and w.lower() in PARTICULAS:
            out.append(w.lower())
        elif tudo_maius:
            out.append(w[:1] + w[1:].lower())
        else:
            out.append(w[:1].upper() + w[1:])
    return ' '.join(out)


def mesa_limpa(v):
    v = str(v or '').strip()
    v = re.sub(r'^mesa\s*', '', v, flags=re.I)
    if re.fullmatch(r'\d+(\.0)?', v):  # "4.0" do Excel, "02" -> "2"
        return str(int(float(v)))
    return v


CONFIRMADO = {'ok', 'sim', 'confirmado', 'confirmada', 'confirmou', 'confirmou presenca', 'presenca confirmada', 'x', 'sem', 'nao', '-'}


def lista_simples(nome_aba, linhas, hi, iNome, saida):
    """Lista sem mesa nem CRM: Nome + agrupamento (Grupo, senão Instituição) + Obs com o resto."""
    h = [norm(c).rstrip(':').strip() for c in linhas[hi]]
    achar = lambda *pref: next((j for j, c in enumerate(h) if j != iNome and c.startswith(pref)), None)
    iGrupo = achar('grupo', 'categoria', 'segmento', 'setor')
    iInst = achar('institui', 'empresa', 'organiza', 'entidade')
    iGrp = iGrupo if iGrupo is not None else iInst
    largura = max(len(r) for r in linhas[hi:])
    outras = [j for j in range(largura) if j not in (iNome, iGrp)]
    out, pulados, unico, juntados, vagas = [], [], {}, [], {}
    for r in linhas[hi + 1:]:
        cel = lambda j: re.sub(r'\s+', ' ', ESPACOS.sub(' ', INVIS.sub('', str(r[j] if j is not None and j < len(r) else '')))).strip()
        nome = bonito(cel(iNome))
        if not nome:
            continue
        if any(norm(cel(j)) == 'nao vem' for j in outras):
            pulados.append(nome)
            continue
        # convite reservado ainda sem nome (ex.: "Cota Ouro" de patrocinador): não é pessoa, quem vier é adicionado na hora
        if any('convite disponivel' in norm(cel(j)) or norm(cel(j)) == 'a definir' for j in outras):
            inst = cel(iInst) if iInst is not None else nome
            vagas[inst] = vagas.get(inst, 0) + 1
            continue
        grp = cel(iGrp)
        grp = grp[:1].upper() + grp[1:]
        obs = [cel(j) for j in outras if cel(j) and norm(cel(j)) not in CONFIRMADO]
        k = norm(nome)
        if k in unico:  # mesmo nome duas vezes: uma linha só, juntando o que for diferente
            u = unico[k]
            u[2] = ' · '.join(dict.fromkeys(filter(None, u[2].split(' · ') + obs)))
            u[4] = u[4] or grp
            juntados.append(nome)
            continue
        unico[k] = [nome, '', ' · '.join(obs), '', grp]
        out.append(unico[k])

    # "Fornecedor" e "Fornecedores" viram um grupo só (fica o mais usado)
    cont = {}
    for l in out:
        cont[l[4]] = cont.get(l[4], 0) + 1
    for g in list(cont):
        par = next((o for o in cont if o != g and re.sub(r'e?s$', '', norm(o)) == re.sub(r'e?s$', '', norm(g))), None)
        if par and cont[par] >= cont[g]:
            for l in out:
                if l[4] == g:
                    l[4] = par

    with open(saida, 'w', encoding='utf-8', newline='\n') as f:
        f.write('Nome\tMesa\tObs\tCRM\tEspecialidade\n')
        for linha in out:
            f.write('\t'.join(linha) + '\n')

    print(f'Aba: {nome_aba} (lista simples: sem mesa e sem CRM)')
    print(f'Convidados: {len(out)}')
    print(f'Nome na coluna {iNome + 1} ("{linhas[hi][iNome].strip()}") · agrupado por '
          + (f'"{linhas[hi][iGrp].strip()}"' if iGrp is not None else 'nada (sem coluna de grupo)'))
    por = {}
    for l in out:
        por[l[4] or 'sem grupo'] = por.get(l[4] or 'sem grupo', 0) + 1
    print('Por grupo: ' + ' · '.join(f'{k}: {v}' for k, v in sorted(por.items(), key=lambda x: -x[1])))
    st = {}
    for l in out:
        for o in l[2].split(' · '):
            if norm(o) in ('sem retorno', 'nao confirmado', 'pendente', 'talvez') or 'patrocinador' in norm(o):
                st[o] = st.get(o, 0) + 1
    if st:
        print('Status que ficou na Obs: ' + ' · '.join(f'{k}: {v}' for k, v in st.items()))
    if vagas:
        print(f'Convites reservados ainda sem nome (fora da lista, adicionar na hora): {sum(vagas.values())} · '
              + ' · '.join(f'{k}: {v}' for k, v in vagas.items()))
    if juntados:
        print('Nomes repetidos juntados numa linha: ' + ', '.join(juntados))
    if pulados:
        print('Pulados ("não vem"): ' + ', '.join(pulados))


def main():
    args = sys.argv[1:]
    aba = None
    if '--aba' in args:
        k = args.index('--aba')
        aba = args[k + 1]
        del args[k:k + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    entrada, saida = args
    abas = ler_xlsx(entrada) if entrada.lower().endswith(('.xlsx', '.xlsm')) else ler_csv(entrada)

    if aba:
        if aba not in abas:
            sys.exit(f'Aba "{aba}" não existe. Abas: {", ".join(abas)}')
        candidatas = [aba]
    else:
        candidatas = list(abas)
    escolha = None
    for nome_aba in candidatas:
        cab = achar_cabecalho(abas[nome_aba])
        if cab:
            escolha = (nome_aba, cab)
            break
    modo_simples = False
    if not escolha:
        # sem mesa nem CRM em nenhuma aba: lista simples, fica a aba com mais nomes
        simples = []
        for nome_aba in candidatas:
            cab = achar_cabecalho(abas[nome_aba], simples=True)
            if cab:
                hi_, iN_ = cab[0], cab[1]
                n = sum(1 for r in abas[nome_aba][hi_ + 1:] if iN_ < len(r) and bonito(r[iN_]))
                simples.append((n, nome_aba, cab))
        if simples:
            n, nome_aba, cab = max(simples, key=lambda x: x[0])
            escolha, modo_simples = (nome_aba, cab), True
            if len(simples) > 1:
                print('Outras abas com nomes: ' + ' · '.join(f'{a}: {m}' for m, a, _ in simples if a != nome_aba))
    if not escolha:
        sys.exit(f'Nenhuma aba com coluna NOME/CONVIDADO. Abas: {", ".join(abas)}')
    if modo_simples:
        return lista_simples(nome_aba, abas[nome_aba], escolha[1][0], escolha[1][1], saida)
    nome_aba, (hi, iNome, iMesa, iObs, iAcomp, iCrm, iEsp) = escolha
    modo_crm = iMesa is None

    out, pulados, nao_conf = [], [], False
    for r in abas[nome_aba][hi + 1:]:
        cel = lambda j: (r[j] if j is not None and j < len(r) else '') or ''
        nome = bonito(cel(iNome))
        if not nome:
            continue
        if re.match(r'^n[aã]o confirmad', norm(nome)):
            nao_conf = True
            continue
        mesa = mesa_limpa(cel(iMesa)) if iMesa is not None else ''
        if 'nao vem' in norm(mesa):
            pulados.append(nome)
            continue
        obs = [str(cel(j)).strip() for j in iObs if str(cel(j)).strip() and norm(cel(j)) not in ('sem', 'nao', '-')]
        if nao_conf:
            mesa, obs = '', ['Não confirmado'] + obs
        crm = re.sub(r'\.0$', '', str(cel(iCrm)).strip())
        esp = re.sub(r'\s+', ' ', str(cel(iEsp))).strip()
        esp = esp[:1].upper() + esp[1:]
        out.append([nome, mesa, ' · '.join(obs), crm, esp])
        acomp = bonito(cel(iAcomp))
        if acomp:
            out.append([acomp, mesa, f'Acompanhante de {nome}', '', ''])

    # evento com CRM: mesmo nome duas vezes é inscrição duplicada; junta numa linha só
    juntados = []
    if modo_crm:
        unico = {}
        for linha in out:
            k = norm(linha[0])
            if k not in unico:
                unico[k] = linha
                continue
            u = unico[k]
            if linha[3] and linha[3] != u[3]:
                u[3] = f'{u[3]} / {linha[3]}' if u[3] else linha[3]
            if not u[4] and linha[4]:
                u[4] = linha[4]
            juntados.append(u[0])
        out = list(unico.values())

    with open(saida, 'w', encoding='utf-8', newline='\n') as f:
        f.write('Nome\tMesa\tObs\tCRM\tEspecialidade\n')
        for linha in out:
            f.write('\t'.join(linha) + '\n')

    print(f'Aba: {nome_aba}')
    print(f'Convidados: {len(out)}')
    if modo_crm:
        por = {}
        for l in out:
            k = l[4] or 'sem especialidade'
            por[k] = por.get(k, 0) + 1
        print('Sem mesa marcada. Por especialidade: ' + ' · '.join(f'{k}: {v}' for k, v in sorted(por.items(), key=lambda x: -x[1])))
        print(f'Sem CRM: {sum(1 for l in out if not l[3])} · sem especialidade: {sum(1 for l in out if not l[4])} (completar na hora pela tela)')
        if juntados:
            print('Inscrições duplicadas juntadas: ' + ', '.join(juntados))
        diverg = [l[0] for l in out if ' / ' in l[3]]
        if diverg:
            print('ATENÇÃO CRM diferente entre as inscrições (ficaram os dois): ' + ', '.join(diverg))
    else:
        por_mesa = {}
        for l in out:
            por_mesa[l[1] or 'sem mesa'] = por_mesa.get(l[1] or 'sem mesa', 0) + 1
        ordem = sorted(por_mesa, key=lambda m: (m == 'sem mesa', int(m) if m.isdigit() else 10**6, m))
        print('Por mesa: ' + ' · '.join(f'{m}: {por_mesa[m]}' for m in ordem))
    if pulados:
        print('Pulados ("não vem"): ' + ', '.join(pulados))
    dup = sorted({l[0] for l in out if sum(1 for x in out if norm(x[0]) == norm(l[0])) > 1})
    if dup:
        print('ATENÇÃO nomes repetidos: ' + ', '.join(dup))


if __name__ == '__main__':
    main()
