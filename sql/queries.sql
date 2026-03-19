
-- Gasto por mês
SELECT mes, SUM(valor_brl)
FROM fato_transacao
GROUP BY mes;

-- Top categorias
SELECT nome_categoria, SUM(valor_brl)
FROM fato_transacao
JOIN dim_categoria USING(id_categoria)
GROUP BY nome_categoria
ORDER BY SUM(valor_brl) DESC;

-- Gasto por titular
SELECT nome_titular, SUM(valor_brl)
FROM fato_transacao
JOIN dim_titular USING(id_titular)
GROUP BY nome_titular;
