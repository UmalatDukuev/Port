select id_em, prof, name from port.employee
left join (select * from port.team
join port.unloading using(id_un) where date_un = '$date_un' ) tab1 using(id_em)
where id_un is NULL;