select distinct id_reg, id_ship , ship.ship_name,
date_of_arrival, date_of_leaving, jetty.jet_name as jet
    from registration reg join ship
		using(id_ship) join jetty using(id_jet)
		where month(date_of_arrival) = '$in_month' and
		year(date_of_arrival)= '$in_year';
