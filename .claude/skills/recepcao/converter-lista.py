"""Converte a planilha de convidados (xlsx/csv) no TSV limpo que a Recepção lê: Nome, Mesa, Obs.

Uso:
  python converter-lista.py <planilha> <saida.tsv> [--aba "Lista dia"]

- Sem --aba: usa a primeira aba que tenha colunas de nome (NOME/CONVIDADO) e MESA.
- Linha "NÃO CONFIRMADOS": quem vem depois entra sem mesa, com obs "Não confirmado".
- Mesa "não vem": pula a pessoa (e avisa).
- Coluna ACOMPANHANTE preenchida: vira outra linha, mesma mesa.
- Colunas de observação/restrição: vão pra Obs.
- Nome TODO EM MAIÚSCULA vira "Nome Normal".
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


def achar_cabecalho(linhas):
    for i, r in enumerate(linhas[:15]):
        h = [norm(c) for c in r]
        nome = next((j for j, c in enumerate(h) if re.match(r'^(nome|convidad)', c)), None)
        mesa = next((j for j, c in enumerate(h) if c == 'mesa'), None)
        if mesa is None:
            mesa = next((j for j, c in enumerate(h) if c.startswith('mesa')), None)
        if nome is not None and mesa is not None:
            obs = [j for j, c in enumerate(h) if re.match(r'^(obs|observa|restri|nota)', c)]
            acomp = next((j for j, c in enumerate(h) if c.startswith('acompanhante')), None)
            return i, nome, mesa, obs, acomp
    return None


def bonito(nome):
    nome = re.sub(r'\s+', ' ', nome).strip()
    if nome.upper() != nome:
        return nome
    minus = {'da', 'de', 'do', 'das', 'dos', 'e'}
    return ' '.join(w.lower() if w.lower() in minus else w.capitalize() for w in nome.split())


def mesa_limpa(v):
    v = str(v or '').strip()
    v = re.sub(r'^mesa\s*', '', v, flags=re.I)
    if re.fullmatch(r'\d+(\.0)?', v):  # "4.0" do Excel, "02" -> "2"
        return str(int(float(v)))
    return v


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
    if not escolha:
        sys.exit(f'Nenhuma aba com colunas NOME/CONVIDADO e MESA. Abas: {", ".join(abas)}')
    nome_aba, (hi, iNome, iMesa, iObs, iAcomp) = escolha

    out, pulados, nao_conf = [], [], False
    for r in abas[nome_aba][hi + 1:]:
        cel = lambda j: (r[j] if j is not None and j < len(r) else '') or ''
        nome = bonito(cel(iNome))
        if not nome:
            continue
        if re.match(r'^n[aã]o confirmad', norm(nome)):
            nao_conf = True
            continue
        mesa = mesa_limpa(cel(iMesa))
        if 'nao vem' in norm(mesa):
            pulados.append(nome)
            continue
        obs = [str(cel(j)).strip() for j in iObs if str(cel(j)).strip() and norm(cel(j)) not in ('sem', 'nao', '-')]
        if nao_conf:
            mesa, obs = '', ['Não confirmado'] + obs
        out.append((nome, mesa, ' · '.join(obs)))
        acomp = bonito(cel(iAcomp))
        if acomp:
            out.append((acomp, mesa, f'Acompanhante de {nome}'))

    with open(saida, 'w', encoding='utf-8', newline='\n') as f:
        f.write('Nome\tMesa\tObs\n')
        for linha in out:
            f.write('\t'.join(linha) + '\n')

    por_mesa = {}
    for _, m, _ in out:
        por_mesa[m or 'sem mesa'] = por_mesa.get(m or 'sem mesa', 0) + 1
    ordem = sorted(por_mesa, key=lambda m: (m == 'sem mesa', int(m) if m.isdigit() else 10**6, m))
    print(f'Aba: {nome_aba}')
    print(f'Convidados: {len(out)}')
    print('Por mesa: ' + ' · '.join(f'{m}: {por_mesa[m]}' for m in ordem))
    if pulados:
        print('Pulados ("não vem"): ' + ', '.join(pulados))
    dup = sorted({n for n, _, _ in out if sum(1 for x, _, _ in out if norm(x) == norm(n)) > 1})
    if dup:
        print('ATENÇÃO nomes repetidos: ' + ', '.join(dup))


if __name__ == '__main__':
    main()
