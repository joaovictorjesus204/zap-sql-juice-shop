-- Consultas de validação de dados no banco SQLite do OWASP Juice Shop (data/juiceshop.sqlite).
-- Cada bloco tem um id, um nome e o resultado esperado:
--   esperado: nenhuma linha     -> qualquer linha devolvida é um defeito de integridade
--   esperado: achado            -> documenta uma vulnerabilidade conhecida (não reprova)
--   esperado: informativo       -> consulta de apoio para análise (não reprova)
-- O script sql/validar.py executa todas e gera o relatório.

-- [SQL-01] E-mails duplicados entre usuários
-- esperado: nenhuma linha
SELECT email, COUNT(*) AS quantidade
FROM Users
GROUP BY LOWER(email)
HAVING COUNT(*) > 1;

-- [SQL-02] Usuários com e-mail sem @
-- Achado na primeira execução: o usuário "demo" é criado com o e-mail "demo". A tela de cadastro
-- exige e-mail válido, mas o banco não tem essa regra: um dado fora do formato entra por outro caminho.
-- esperado: achado
SELECT id, email
FROM Users
WHERE email NOT LIKE '%_@_%';

-- [SQL-03] Produtos sem preço ou com preço menor ou igual a zero
-- esperado: nenhuma linha
SELECT id, name, price
FROM Products
WHERE price IS NULL OR price <= 0;

-- [SQL-04] Estoque negativo
-- esperado: nenhuma linha
SELECT q.id, p.name, q.quantity
FROM Quantities q
JOIN Products p ON p.id = q.ProductId
WHERE q.quantity < 0;

-- [SQL-05] Itens de cesta com quantidade menor que 1
-- esperado: nenhuma linha
SELECT id, BasketId, ProductId, quantity
FROM BasketItems
WHERE quantity < 1;

-- [SQL-06] Itens de cesta apontando para produto inexistente (registro órfão)
-- esperado: nenhuma linha
SELECT bi.id, bi.ProductId
FROM BasketItems bi
LEFT JOIN Products p ON p.id = bi.ProductId
WHERE p.id IS NULL;

-- [SQL-07] Cestas de usuário inexistente (registro órfão)
-- esperado: nenhuma linha
SELECT b.id, b.UserId
FROM Baskets b
LEFT JOIN Users u ON u.id = b.UserId
WHERE b.UserId IS NOT NULL AND u.id IS NULL;

-- [SQL-08] Avaliações com nota fora da escala de 1 a 5
-- esperado: nenhuma linha
SELECT id, UserId, rating
FROM Feedbacks
WHERE rating < 1 OR rating > 5;

-- [SQL-09] Senhas guardadas como MD5 sem sal (32 caracteres hexadecimais)
-- esperado: achado
SELECT id, email, LENGTH(password) AS tamanho
FROM Users
WHERE LENGTH(password) = 32
  AND LOWER(password) NOT GLOB '*[^0-9a-f]*';

-- [SQL-10] Usuários por perfil de acesso
-- esperado: informativo
SELECT role AS perfil, COUNT(*) AS usuarios
FROM Users
GROUP BY role
ORDER BY usuarios DESC;

-- [SQL-11] Produtos que mais aparecem nas cestas
-- esperado: informativo
SELECT p.name AS produto, SUM(bi.quantity) AS unidades, COUNT(DISTINCT bi.BasketId) AS cestas
FROM BasketItems bi
JOIN Products p ON p.id = bi.ProductId
GROUP BY p.id
ORDER BY unidades DESC
LIMIT 5;
