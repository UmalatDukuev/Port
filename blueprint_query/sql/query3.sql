select id_e, surnamee, count(id_u), sum(hours)
from port1.employee
left join port1.team using(id_e)
left join port1.card using(id_e)
group by id_e, surnamee;