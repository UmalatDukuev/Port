select count(*) from reg_rep
where rep_month = '$in_month' and
       rep_year = '$in_year';