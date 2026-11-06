# Casos de teste | OWASP Juice Shop

Projetados com as técnicas do [plano de teste](plano-de-teste.md). Execução manual em **05/11/2026**, na instância pública (demo.owasp-juice.shop), no Chrome: os 7 casos **P1 passaram**. Os 8 casos P2 estão projetados e ainda **não executados**.

| ID | Funcionalidade | Título | Prioridade | Técnica | Status |
|---|---|---|---|---|---|
| CT-01 | Cadastro | Cadastrar cliente com dados válidos | P1 | Partição de equivalência | Passou |
| CT-02 | Cadastro | Senha com 4 caracteres é recusada | P1 | Valor limite | Passou |
| CT-03 | Cadastro | Senha com 5 caracteres é aceita | P2 | Valor limite | Não executado |
| CT-04 | Cadastro | Senha com 40 caracteres é aceita | P2 | Valor limite | Não executado |
| CT-05 | Cadastro | Senha com 41 caracteres é recusada | P2 | Valor limite | Não executado |
| CT-06 | Cadastro | Confirmação de senha diferente | P1 | Partição de equivalência | Passou |
| CT-07 | Cadastro | E-mail em formato inválido | P2 | Partição de equivalência | Não executado |
| CT-08 | Login | E-mail e senha corretos | P1 | Tabela de decisão | Passou |
| CT-09 | Login | E-mail correto e senha errada | P1 | Tabela de decisão | Passou |
| CT-10 | Login | E-mail não cadastrado | P2 | Tabela de decisão | Não executado |
| CT-11 | Busca | Busca com resultado | P1 | Partição de equivalência | Passou |
| CT-12 | Busca | Busca sem resultado | P2 | Partição de equivalência | Não executado |
| CT-13 | Carrinho | Adicionar, aumentar e remover item | P1 | Transição de estado | Passou |
| CT-14 | Avaliação | Comentário com 160 caracteres é aceito | P2 | Valor limite | Não executado |
| CT-15 | Avaliação | Comentário com 161 caracteres é recusado | P2 | Valor limite | Não executado |

---

## CT-01 · Cadastrar cliente com dados válidos

**Funcionalidade:** Cadastro · **Prioridade:** P1 · **Técnica:** Partição de equivalência · **Status:** Passou (05/11/2026)

**Pré-condição:** Tela de cadastro aberta (Account > Login > Not yet a customer?)

**Passos:**

1. Informar e-mail novo válido
2. Senha com 8 caracteres e a mesma na confirmação
3. Escolher uma pergunta de segurança e responder
4. Clicar em Register

**Resultado esperado:** Mensagem de cadastro concluído e redirecionamento para o login

## CT-02 · Senha com 4 caracteres é recusada

**Funcionalidade:** Cadastro · **Prioridade:** P1 · **Técnica:** Valor limite · **Status:** Passou (05/11/2026)

**Pré-condição:** Tela de cadastro aberta

**Passos:**

1. Preencher os campos válidos
2. Informar senha com 4 caracteres

**Resultado esperado:** Aviso de que a senha deve ter de 5 a 40 caracteres e botão Register desabilitado

## CT-03 · Senha com 5 caracteres é aceita

**Funcionalidade:** Cadastro · **Prioridade:** P2 · **Técnica:** Valor limite · **Status:** Não executado

**Pré-condição:** Tela de cadastro aberta

**Passos:**

1. Preencher os campos válidos
2. Informar senha com 5 caracteres

**Resultado esperado:** Nenhum aviso de tamanho; botão Register habilitado

## CT-04 · Senha com 40 caracteres é aceita

**Funcionalidade:** Cadastro · **Prioridade:** P2 · **Técnica:** Valor limite · **Status:** Não executado

**Pré-condição:** Tela de cadastro aberta

**Passos:**

1. Preencher os campos válidos
2. Informar senha com 40 caracteres

**Resultado esperado:** Nenhum aviso de tamanho; botão Register habilitado

## CT-05 · Senha com 41 caracteres é recusada

**Funcionalidade:** Cadastro · **Prioridade:** P2 · **Técnica:** Valor limite · **Status:** Não executado

**Pré-condição:** Tela de cadastro aberta

**Passos:**

1. Preencher os campos válidos
2. Informar senha com 41 caracteres

**Resultado esperado:** Aviso de tamanho e botão Register desabilitado

## CT-06 · Confirmação de senha diferente

**Funcionalidade:** Cadastro · **Prioridade:** P1 · **Técnica:** Partição de equivalência · **Status:** Passou (05/11/2026)

**Pré-condição:** Tela de cadastro aberta

**Passos:**

1. Senha válida
2. Confirmação diferente

**Resultado esperado:** Aviso de que as senhas não conferem; botão Register desabilitado

## CT-07 · E-mail em formato inválido

**Funcionalidade:** Cadastro · **Prioridade:** P2 · **Técnica:** Partição de equivalência · **Status:** Não executado

**Pré-condição:** Tela de cadastro aberta

**Passos:**

1. Informar 'cliente.sem.arroba'

**Resultado esperado:** Aviso de e-mail inválido; botão Register desabilitado

## CT-08 · E-mail e senha corretos

**Funcionalidade:** Login · **Prioridade:** P1 · **Técnica:** Tabela de decisão · **Status:** Passou (05/11/2026)

**Pré-condição:** Cliente do CT-01 cadastrado

**Passos:**

1. Informar e-mail e senha do CT-01
2. Clicar em Log in

**Resultado esperado:** Acesso à loja logado; e-mail do cliente aparece no menu Account

## CT-09 · E-mail correto e senha errada

**Funcionalidade:** Login · **Prioridade:** P1 · **Técnica:** Tabela de decisão · **Status:** Passou (05/11/2026)

**Pré-condição:** Cliente do CT-01 cadastrado

**Passos:**

1. E-mail do CT-01
2. Senha diferente

**Resultado esperado:** Mensagem genérica de e-mail ou senha inválidos, sem dizer qual dos dois está errado

## CT-10 · E-mail não cadastrado

**Funcionalidade:** Login · **Prioridade:** P2 · **Técnica:** Tabela de decisão · **Status:** Não executado

**Pré-condição:** Nenhuma

**Passos:**

1. E-mail que não existe
2. Qualquer senha

**Resultado esperado:** A mesma mensagem genérica do CT-09

## CT-11 · Busca com resultado

**Funcionalidade:** Busca · **Prioridade:** P1 · **Técnica:** Partição de equivalência · **Status:** Passou (05/11/2026)

**Pré-condição:** Página inicial

**Passos:**

1. Pesquisar 'apple'

**Resultado esperado:** Lista só com produtos que têm 'apple' no nome ou na descrição

## CT-12 · Busca sem resultado

**Funcionalidade:** Busca · **Prioridade:** P2 · **Técnica:** Partição de equivalência · **Status:** Não executado

**Pré-condição:** Página inicial

**Passos:**

1. Pesquisar 'xyzxyz'

**Resultado esperado:** Mensagem de nenhum resultado e nenhum produto listado

## CT-13 · Adicionar, aumentar e remover item

**Funcionalidade:** Carrinho · **Prioridade:** P1 · **Técnica:** Transição de estado · **Status:** Passou (05/11/2026)

**Pré-condição:** Cliente logado com carrinho vazio

**Passos:**

1. Adicionar um produto
2. Abrir o carrinho
3. Aumentar a quantidade para 2
4. Remover o item

**Resultado esperado:** Total atualizado a cada passo e carrinho vazio no final

## CT-14 · Comentário com 160 caracteres é aceito

**Funcionalidade:** Avaliação · **Prioridade:** P2 · **Técnica:** Valor limite · **Status:** Não executado

**Pré-condição:** Tela Customer Feedback aberta

**Passos:**

1. Comentário com 160 caracteres
2. Nota 4
3. Resolver o CAPTCHA
4. Enviar

**Resultado esperado:** Mensagem de agradecimento

## CT-15 · Comentário com 161 caracteres é recusado

**Funcionalidade:** Avaliação · **Prioridade:** P2 · **Técnica:** Valor limite · **Status:** Não executado

**Pré-condição:** Tela Customer Feedback aberta

**Passos:**

1. Digitar 161 caracteres no comentário

**Resultado esperado:** O campo para em 160 caracteres ou mostra aviso; não é possível enviar 161
