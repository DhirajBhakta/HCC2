# HCC2

go directly to config.py
change all the database settings according to ur PC.
dont touch mail configs
.

protocol to be strictly followed in pharma:
--> All batch numbers of the SAME drug must be kept on the SAME RACK! (no excuses)


#TODOs
1) clean up css
2) try to separate all CSS into maybe one-two separate globally accessible files...or put everything in base2.html
3) clean up JS. make it more readable
4) clean up models.py.  too many redundancy currently. Think of better SQL queries than current ones. try to incorporate business logic within sql queries rather than extracting raw data and doing it in python.
5) VIEWS.PY  creating conn, and cursor way too much. think of alternatives, reusable conn, cursors (see if they can actually be re-used. permitted or not?)
6) create separate config files for DEV, TEST, and PRODUCTION
7) go through entire models.py and fix security issues.
8) client side security issues.
9) back button after logging in.


#List of possible bugs
1) if pharmacist selects a batch_no which has say 20 qty left , and the requirement was 25
2) batch_numbers whose qty has gone below 0 , are not yet deleted i guess (I GUESS).



#--backup
# mysql code to create view.
# needs to be modified later on to see to it that the view doesnt get too too too big with time, as the total number of prescriptions keep on increasing. What you gotta do is to inner join with Notification_buffer table and include only those prescriptions whose STATUS is not ACK!
create view View_prescription_drugs_available_batches AS SELECT map.prescription_id,drug.trade_name,map.drug_id,map.qty as quantity_specified,  drug.rack_id, batch.batch_no, batch.qty as quantity_available, batch.exp_date FROM Drug as drug INNER JOIN Batch as batch INNER JOIN Prescription_drug_map as map ON drug.drug_id=batch.drug_id and map.drug_id=batch.drug_id;
