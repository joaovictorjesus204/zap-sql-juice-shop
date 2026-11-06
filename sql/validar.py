"""Executa sql/consultas.sql no banco do Juice Shop e valida o resultado esperado de cada consulta.

Uso: python sql/validar.py caminho/juiceshop.sqlite [reports/sql.html]
Termina com erro se alguma consulta "nenhuma linha" devolver registros.
"""
import html
import pathlib
import re
import sqlite3
import sys

BLOCO = re.compile(
    r"--\s*\[(?P<id>SQL-\d+)\]\s*(?P<nome>.+?)\n--\s*esperado:\s*(?P<esperado>[^\n]+)\n(?P<sql>.*?;)",
    re.S,
)


def carregar(arquivo: pathlib.Path):
    return [m.groupdict() for m in BLOCO.finditer(arquivo.read_text(encoding="utf-8"))]


def main():
    banco = sys.argv[1]
    saida = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "reports/sql.html")
    consultas = carregar(pathlib.Path(__file__).with_name("consultas.sql"))
    conexao = sqlite3.connect(f"file:{banco}?mode=ro", uri=True)

    falhas, linhas_html = 0, []
    for c in consultas:
        cursor = conexao.execute(c["sql"])
        colunas = [d[0] for d in cursor.description]
        registros = cursor.fetchall()
        esperado = c["esperado"].strip()

        if esperado == "nenhuma linha":
            situacao = "PASSOU" if not registros else "FALHOU"
            falhas += situacao == "FALHOU"
        elif esperado == "achado":
            situacao = "ACHADO" if registros else "NÃO REPRODUZIDO"
        else:
            situacao = "INFORMATIVO"

        print(f"{c['id']} {situacao:16} {len(registros):4} linha(s)  {c['nome']}")
        tabela = "".join(
            "<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in r) + "</tr>" for r in registros[:20]
        )
        linhas_html.append(
            f"<section><h2>{c['id']} · {html.escape(c['nome'])} <span class='{situacao.split()[0].lower()}'>{situacao}</span></h2>"
            f"<p>Esperado: {html.escape(esperado)} · Retornou {len(registros)} linha(s)</p>"
            f"<pre>{html.escape(c['sql'].strip())}</pre>"
            + (f"<table><tr>{''.join(f'<th>{html.escape(x)}</th>' for x in colunas)}</tr>{tabela}</table>" if registros else "")
            + "</section>"
        )

    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(
        "<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Validação SQL | Juice Shop</title><style>"
        "body{font-family:system-ui,sans-serif;max-width:960px;margin:0 auto;padding:24px 16px;background:#fafafa;color:#1d2330}"
        "section{background:#fff;border:1px solid #e2e5ea;border-radius:8px;padding:12px 16px;margin:12px 0}"
        "h2{font-size:1rem}pre{background:#f3f4f6;padding:8px;overflow-x:auto}table{border-collapse:collapse;font-size:.85rem}"
        "td,th{border:1px solid #e2e5ea;padding:4px 8px;text-align:left}"
        ".passou{color:#1a7f37}.falhou{color:#cf222e}.achado{color:#9a6700}.informativo,.não{color:#57606a}"
        "</style></head><body><h1>Validação de dados com SQL</h1>"
        f"<p>Banco: juiceshop.sqlite · {len(consultas)} consultas · {falhas} falha(s) de integridade</p>"
        + "".join(linhas_html) + "</body></html>",
        encoding="utf-8",
    )
    print(f"\nRelatório: {saida}")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
