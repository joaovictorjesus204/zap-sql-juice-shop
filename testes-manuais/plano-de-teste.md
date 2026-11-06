# Plano de teste | OWASP Juice Shop

## 1. Objetivo
Verificar as funções principais da loja (cadastro, login, busca, carrinho e avaliação) e as regras de validação dos formulários, com casos de teste projetados por técnica.

## 2. Escopo

| Dentro do escopo | Fora do escopo |
|---|---|
| Cadastro de cliente | Pagamento real e entrega |
| Login e logout | Área administrativa |
| Busca de produtos | Desafios de segurança do placar (Score Board) |
| Carrinho de compras | Desempenho e carga |
| Formulário de avaliação (Customer Feedback) | Aplicativo mobile |

## 3. Abordagem

| Técnica | Onde é usada |
|---|---|
| Partição de equivalência | E-mail válido e inválido, busca com e sem resultado |
| Análise de valor limite | Tamanho da senha (5 a 40) e do comentário (até 160) |
| Tabela de decisão | Login: combinações de e-mail e senha corretos ou incorretos |
| Transição de estado | Carrinho: vazio, com item, quantidade alterada, item removido |
| Teste exploratório guiado | Mensagens de erro e textos refletidos na tela |

## 4. Ambiente
- Aplicação: OWASP Juice Shop, instância de demonstração pública (https://demo.owasp-juice.shop) ou local (`docker run -p 3000:3000 bkimminich/juice-shop`).
- Navegadores: Chrome e Firefox, versões atuais.
- Dados: usuário criado no próprio teste de cadastro (CT-01).

## 5. Critérios
- **Entrada:** aplicação acessível e casos de teste revisados.
- **Saída:** todos os casos P1 executados, nenhum defeito crítico aberto.
- **Suspensão:** aplicação fora do ar ou defeito que impeça o login.

## 6. Riscos

| Risco | Mitigação |
|---|---|
| A instância pública é reiniciada e perde os dados | Cada caso cria os próprios dados |
| O Juice Shop tem falhas de propósito | Comportamento inseguro é registrado como achado, com referência à OWASP |

## 7. Entregáveis
- Casos de teste: `casos-de-teste.md` e `casos-de-teste.csv` (importável no Jira/Xray, TestRail e Azure Test Plans).
- Modelo de relato de defeito: `modelo-de-defeito.md`.
