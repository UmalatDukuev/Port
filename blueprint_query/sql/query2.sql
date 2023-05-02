select id_ship, ship_name, count(sl.id_ship)
from ship  left join (select id_ship from registration
where date_of_arrival < "$input_end" and date_of_arrival > "$input_start") sl
using(id_ship)
group by id_ship, ship_name ;