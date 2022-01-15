SELECT s.nombre_silla, SUM(cantidad_ped) FROM pedido p
INNER JOIN tipo_silla s ON (p.id_silla = s.id_silla)
WHERE fecha_ped = "2022-01-09" 
GROUP BY p.id_silla