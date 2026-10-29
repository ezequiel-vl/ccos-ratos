#!/bin/sh
# Sobe arquivos da dist/ pro swipe.ezeos.com.br por TUS (upload da Hostinger).
# As credenciais vêm de hosting_files_generate-upload-url (domínio ezeos.com.br),
# valem algumas horas e entram por variável de ambiente, nunca no arquivo:
#   TUS_URL=... TUS_AUTH=... TUS_REST=... sh subir.sh [arquivo ...]
# Sem argumentos sobe tudo, com o .htaccess primeiro pra pasta nunca ficar aberta.
cd "$(dirname "$0")/dist" || exit 1
: "${TUS_URL:?falta TUS_URL}" "${TUS_AUTH:?falta TUS_AUTH}" "${TUS_REST:?falta TUS_REST}"

if [ $# -eq 0 ]; then
  set -- .htaccess $( [ -f .htpasswd ] && echo .htpasswd ) robots.txt index.html $(ls prints/* 2>/dev/null)
fi

falhas=0
for f in "$@"; do
  tam=$(wc -c < "$f" | tr -d ' ')
  alvo="$TUS_URL/swipe/$f?override=true"
  c1=$(curl -sS -o /dev/null -w "%{http_code}" -X POST "$alvo" \
    -H "X-Auth: $TUS_AUTH" -H "X-Auth-Rest: $TUS_REST" -H "Tus-Resumable: 1.0.0" \
    -H "Upload-Length: $tam" -H "Upload-Offset: 0")
  off=$(curl -sS -D - -o /dev/null -X PATCH "$alvo" \
    -H "X-Auth: $TUS_AUTH" -H "X-Auth-Rest: $TUS_REST" -H "Tus-Resumable: 1.0.0" \
    -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
    --data-binary "@$f" | tr -d '\r' | sed -n 's/^[Uu]pload-[Oo]ffset: //p')
  if [ "$c1" = "201" ] && [ "$off" = "$tam" ]; then echo "ok    $f"; else echo "FALHA $f (post $c1, offset $off de $tam)"; falhas=$((falhas+1)); fi
done
[ $falhas -eq 0 ] || exit 1
