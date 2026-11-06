"""Lê o relatório JSON do OWASP ZAP e reprova se houver alerta de risco alto NOVO.

O Juice Shop é vulnerável de propósito: os alertas altos já analisados ficam em
zap/alertas-conhecidos.txt, com a explicação no README. Um alerta alto fora da lista indica
regressão de segurança e reprova o pipeline.
Uso: python zap/verificar_alertas.py report_json.json
"""
import json
import pathlib
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

arquivo = pathlib.Path(__file__).with_name("alertas-conhecidos.txt")
conhecidos = {
    linha.strip() for linha in arquivo.read_text(encoding="utf-8").splitlines()
    if linha.strip() and not linha.startswith("#")
}
altos = [a["alert"] for a in alertas if a["riskcode"] == "3"]
novos = [nome for nome in altos if nome not in conhecidos]
for nome in altos:
    print(f"Alerta alto {'NOVO' if nome in novos else 'conhecido (documentado no README)'}: {nome}")
if novos:
    sys.exit(f"Reprovado: {len(novos)} alerta(s) de risco alto novo(s): {', '.join(novos)}")
print("Aprovado: nenhum alerta de risco alto novo.")
