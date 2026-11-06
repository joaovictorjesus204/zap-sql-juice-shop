"""Lê o relatório JSON do OWASP ZAP e reprova se houver alerta de risco alto.

Os alertas de risco médio e baixo do Juice Shop são conhecidos (o app é vulnerável de propósito)
e ficam documentados no relatório. Um alerta alto novo indica regressão de segurança.
Uso: python zap/verificar_alertas.py report_json.json
"""
import json
import sys
from collections import Counter

RISCO = {"3": "Alto", "2": "Médio", "1": "Baixo", "0": "Informativo"}

relatorio = json.load(open(sys.argv[1], encoding="utf-8"))
alertas = [a for site in relatorio.get("site", []) for a in site.get("alerts", [])]
contagem = Counter(RISCO.get(a["riskcode"], a["riskcode"]) for a in alertas)

print(f"Tipos de alerta encontrados: {len(alertas)}")
for nivel in ["Alto", "Médio", "Baixo", "Informativo"]:
    print(f"  {nivel}: {contagem.get(nivel, 0)}")
for a in sorted(alertas, key=lambda a: -int(a["riskcode"])):
    print(f"  [{RISCO.get(a['riskcode'])}] {a['alert']} ({a.get('count', '?')} ocorrência(s))")

altos = [a["alert"] for a in alertas if a["riskcode"] == "3"]
if altos:
    sys.exit(f"Reprovado: {len(altos)} alerta(s) de risco alto: {', '.join(altos)}")
print("Aprovado: nenhum alerta de risco alto.")
