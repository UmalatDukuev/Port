select * from port1.registration
where month(date_of_arrival) = '$input_month' and year(date_of_arrival) = '$input_year';