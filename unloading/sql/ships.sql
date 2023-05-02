select id_r, ship.name from registration
join ship using(id_sh)
where date_unl is NULL;