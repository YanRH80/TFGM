#!/usr/bin/env bash
# Resync figuras desde /figures raíz cuando Resultados.qmd regenere figuras.
# Uso: bash manuscrito/figuras/make_figs.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cp "$ROOT"/figures/*.png "$ROOT"/figures/*.md "$ROOT"/manuscrito/figuras/
echo "Resync OK → $ROOT/manuscrito/figuras/"
