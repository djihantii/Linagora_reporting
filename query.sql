
--**************CLIENT*******************
-- nom du contrat
select name from contract where customer_id = id


--*************CONTRAT******************
-- name, creation, description, strat end (contrat)
select creation_date from contract where customer_id = id
select start_date from contract where customer_id = id
select end_date from contract where customer_id = id
select description from contract where customer_id = id
select creation_date from contract where customer_id = id

--************SOFTWARE CONTRAT*************
software_id
select software_id from contract_software_version where contract_id = (select id from contract where customer_id = id);
critique ?
select critical from contract_software_version where contract_id = (select id from contract where customer_id = id);

--*******a partir du client trouver les infos sur ses logiciels
 select * from software where id = (select software_id from contract_software_version where contract_id = (select id from contract where customer_id = 2));

--*************LES TICKETS
--tickets ouverts dans ce mois pour un contrat_id

select * from statistic_ticket where (select extract (month from (select age(current_date , creation_date)))) = 0 and (select extract (year from (select age(current_date , creation_date)))) = 0 and contract_id = id;

==> stocké dans statMonth
--les tickets ouvert pour un contrat pendant les 3 derniers mois

select * from statistic_ticket where (select extract (year from (select age(current_date , creation_date)))) = 0 and (select extract (month from (select age( current_date , creation_date)))) <4 and contract_id = 12485;
==> stocké dans statThreeMonths
-- tickets suspendus
select waiting_for_customer from statistic_ticket where contract_id = id;

-- nombre de ticket de chaque type pour un contrat donné dans pour le mois en cours

select count(*) , issue_type  from statistic_ticket where (select extract (month from (select age(current_date , creation_date)))) = 0 and (select extract (year from (select age(current_date , creation_date)))) = 0 and contract_id = 316672 group by issue_type;

-- nombre de ticket de chaque type pour un contrat donné dans pour les 3 derniers mois


select count(*) , issue_type from statistic_ticket where (select extract (year from (select age(current_date , creation_date)))) = 0 and (select extract (month from (select age( current_date , creation_date)))) <4 and contract_id = 316672 group by issue_type;

-- nombre de demande d'information pour un contrat donné

select count(issue_type) from statistic_ticket where issue_type like '%information%' and contract_id=12485 and (select extract(month from current_date))=(select extract(month from creation_date)) and (select extract(year from current_date))=(select extract(year from creation_date));

-- aggréagation de tickets d'information==> pour trois mois

select issue_type,(select extract (month from (select age (current_date , creation_date)))) as mnth , select age (current_date , creation_date) as dt from statistic_ticket where issue_type like '%information%' and contract_id = 12485 and (select extract (month from (select age (current_date , creation_date))))<5;