
-- Gasto por mes
SELECT
	d.ano,
	d.mes,
	ROUND(SUM(f.valor_brl), 2) AS total_gasto_brl
FROM fato_transacao f
JOIN dim_data d ON d.id_data = f.id_data
GROUP BY d.ano, d.mes
ORDER BY d.ano, d.mes;

-- Top categorias
SELECT
	c.nome_categoria,
	ROUND(SUM(f.valor_brl), 2) AS total_gasto_brl
FROM fato_transacao f
JOIN dim_categoria c ON c.id_categoria = f.id_categoria
GROUP BY c.nome_categoria
ORDER BY total_gasto_brl DESC;

-- Gasto por titular
SELECT
	t.nome_titular,
	t.final_cartao,
	ROUND(SUM(f.valor_brl), 2) AS total_gasto_brl
FROM fato_transacao f
JOIN dim_titular t ON t.id_titular = f.id_titular
GROUP BY t.nome_titular, t.final_cartao
ORDER BY total_gasto_brl DESC;
