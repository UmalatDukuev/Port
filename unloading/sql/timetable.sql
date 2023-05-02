SELECT id_un, date_un, id_r,name FROM port.external_user
join port.team on id_em = em_id
join port.unloading using(id_un)
join port.registration using(id_r)
join port.ship using(id_sh)
where user_id = 1;