#!/bin/sh
# Captura os prints de todas as referências do refs.json que ainda não têm capa.
# Uso: sh capturar-todas.sh [--refazer]
cd "$(dirname "$0")"
RAIZ="$(cd ../.. && pwd)"
node -e 'for (const r of require("./refs.json")) console.log(r.id + "\t" + (r.imagem ? "IMG:" + r.imagem : r.url))' | while IFS="$(printf '\t')" read -r id alvo; do
  [ "$1" != "--refazer" ] && [ -f "prints/$id.jpg" ] && continue
  case "$alvo" in IMG:*) alvo="$RAIZ/${alvo#IMG:}";; esac
  node capturar.js "$id" "$alvo" || echo "FALHOU $id"
done
