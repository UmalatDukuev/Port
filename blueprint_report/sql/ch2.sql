select id_u, date_of_unload, id_reg, count(team.id_u), ship.ship_name from unload
		join registration using(id_reg)
		join ship using(id_ship)
		left join team using(id_u)
		where month(date_of_unload)='$in_month' and year(date_of_unload) = '$in_year'
		group by team.id_u;