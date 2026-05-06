create view dbsk_donorvw (id, first_name, last_name, addr1, addr2, city, state, zip, active, processed_date, amount)
as
select dbsk_donor.id,
       first_name,
       last_name,
       addr1,
       addr2,
       city,
       state,
       zip,
       active,
       processed_date,
       amount
from dbsk_donor
         inner join dbsk_donation on dbsk_donation.donor_id = dbsk_donor.id
;