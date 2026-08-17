#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 test_relatorios_comissao.py
python3 test_relatorios_endpoints.py
