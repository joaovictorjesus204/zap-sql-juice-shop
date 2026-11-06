# OWASP ZAP + SQL + Testes manuais | OWASP Juice Shop

[![Segurança e dados](https://github.com/joaovictorjesus204/zap-sql-juice-shop/actions/workflows/seguranca.yml/badge.svg)](https://github.com/joaovictorjesus204/zap-sql-juice-shop/actions/workflows/seguranca.yml)

**📊 Relatórios da última execução:** https://joaovictorjesus204.github.io/zap-sql-juice-shop/

Três frentes de QA na mesma aplicação, o **[OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)**, loja virtual mantida pela OWASP para treino e validação de testes de segurança:

| Frente | Ferramenta | O que entrega |
|---|---|---|
| **Segurança** | OWASP ZAP | Varredura automática no CI, com critério de aceite: nenhum alerta de risco alto |
| **Dados** | SQL (SQLite) | 11 consultas no banco do próprio app: integridade, registros órfãos e armazenamento de senha |
| **Testes manuais** | Plano e casos de teste | 15 casos projetados por técnica, 7 executados (todos passaram), em Markdown e CSV importável |

Autor: João Victor de Jesus

---

## Por que o Juice Shop

Fazer varredura de segurança em sistema de terceiros sem autorização é crime no Brasil (Lei 12.737/2012). O Juice Shop foi criado pela OWASP justamente para isso. No CI, ele roda dentro do próprio servidor do GitHub Actions: a varredura nunca sai para a internet.

---

## Segurança com OWASP ZAP

| | |
|---|---|
| Tipo de varredura | Baseline (passiva): o ZAP navega pelo app e analisa as respostas sem atacar |
| Navegação | Spider tradicional e spider AJAX, porque o Juice Shop é uma SPA em Angular |
| Critério de aceite | O pipeline reprova se aparecer alerta de risco **alto** (`zap/verificar_alertas.py`) |
| Relatório | HTML do ZAP com risco, evidência, URL afetada e recomendação de correção |

Os alertas médios e baixos do Juice Shop são conhecidos, porque o app é vulnerável de propósito, e ficam documentados no relatório. Um alerta alto novo indica regressão de segurança.

## Dados com SQL

O CI copia o banco SQLite do Juice Shop (`data/juiceshop.sqlite`) e roda as consultas de [`sql/consultas.sql`](sql/consultas.sql). Cada consulta declara o resultado esperado:

| ID | Consulta | Esperado |
|---|---|---|
| SQL-01 | E-mails duplicados entre usuários | nenhuma linha |
| SQL-02 | Usuários com e-mail sem @ | nenhuma linha |
| SQL-03 | Produtos sem preço ou com preço ≤ 0 | nenhuma linha |
| SQL-04 | Estoque negativo | nenhuma linha |
| SQL-05 | Itens de cesta com quantidade < 1 | nenhuma linha |
| SQL-06 | Itens de cesta apontando para produto inexistente (`LEFT JOIN`) | nenhuma linha |
| SQL-07 | Cestas de usuário inexistente | nenhuma linha |
| SQL-08 | Avaliações com nota fora de 1 a 5 | nenhuma linha |
| SQL-09 | Senhas guardadas como MD5 sem sal | **achado de segurança** |
| SQL-10 | Usuários por perfil de acesso (`GROUP BY`) | informativo |
| SQL-11 | Produtos que mais aparecem nas cestas (`JOIN`, `SUM`, `COUNT DISTINCT`) | informativo |

Para rodar no computador com um banco baixado do artefato do CI:

```bash
python sql/validar.py caminho/juiceshop.sqlite
```

## Testes manuais

| Arquivo | Conteúdo |
|---|---|
| [`plano-de-teste.md`](testes-manuais/plano-de-teste.md) | Objetivo, escopo, técnicas, ambiente, critérios de entrada e saída, riscos |
| [`casos-de-teste.md`](testes-manuais/casos-de-teste.md) | 15 casos com pré-condição, passos e resultado esperado |
| [`casos-de-teste.csv`](testes-manuais/casos-de-teste.csv) | Os mesmos casos, prontos para importar no Jira/Xray, TestRail ou Azure Test Plans |
| [`modelo-de-defeito.md`](testes-manuais/modelo-de-defeito.md) | Modelo de relato de defeito, com severidade e prioridade separadas |

| Técnica | Casos |
|---|---|
| Análise de valor limite | Senha com 4, 5, 40 e 41 caracteres; comentário com 160 e 161 caracteres |
| Partição de equivalência | Cadastro válido, e-mail inválido, senhas diferentes, busca com e sem resultado |
| Tabela de decisão | Login com as combinações de e-mail e senha corretos ou errados |
| Transição de estado | Carrinho: vazio, com item, quantidade alterada, item removido |

Os 7 casos de prioridade P1 (CT-01, CT-02, CT-06, CT-08, CT-09, CT-11 e CT-13) foram executados manualmente em 05/11/2026, na instância pública, no Chrome, e todos passaram. Os 8 casos P2 estão projetados e ainda não executados. O status, a data e o ambiente de cada caso estão no CSV.

---

## Estrutura

```
testes-manuais/               plano, casos de teste (Markdown e CSV) e modelo de defeito
zap/verificar_alertas.py      critério de aceite de segurança sobre o relatório do ZAP
sql/consultas.sql             consultas de validação, cada uma com o resultado esperado
sql/validar.py                executa as consultas e gera o relatório HTML
pages/index.html              página inicial dos relatórios
.github/workflows/            Juice Shop em contêiner, ZAP, SQL e publicação no GitHub Pages
```

## Decisões técnicas

| Decisão | Por quê |
|---|---|
| **Varredura passiva no CI** | Rápida e segura para rodar toda semana. A varredura ativa (ataques) fica para um ambiente dedicado |
| **Critério de aceite só para risco alto** | O app tem falhas médias de propósito. Reprovar em qualquer alerta deixaria o pipeline sempre vermelho e sem informação nova |
| **SQL no banco real do app** | As consultas rodam nos dados que o próprio Juice Shop cria, e não numa base inventada |
| **Resultado esperado escrito junto da consulta** | `consultas.sql` é legível por quem não programa e é a mesma fonte que o script executa |
| **Banco aberto só para leitura** (`mode=ro`) | A validação nunca altera os dados |
| **Casos de teste também em CSV** | Ferramentas de gestão de testes importam CSV direto |

## Próximos passos

- Varredura ativa do ZAP numa execução manual separada.
- Executar os casos P2 e anexar prints como evidência de execução.
- Testes de API do Juice Shop autenticados com o token do login.
