# HCC2

go directly to config.py
change all the database settings according to ur PC.
dont touch mail configs
.

protocol to be strictly followed in pharma:
--> All batch numbers of the SAME drug must be kept on the SAME RACK! (no excuses)


#List of possible bugs
1) if pharmacist selects a batch_no which has say 20 qty left , and the requirement was 25
2) batch_numbers whose qty has gone below 0 , are not yet deleted i guess (I GUESS).



#--backup
# mysql code to create view.
# needs to be modified later on to see to it that the view doesnt get too too too big with time, as the total number of prescriptions keep on increasing. What you gotta do is to inner join with Notification_buffer table and include only those prescriptions whose STATUS is not ACK!
create view View_prescription_drugs_available_batches AS SELECT map.prescription_id,drug.trade_name,map.drug_id,map.qty as quantity_specified,  drug.rack_id, batch.batch_no, batch.qty as quantity_available, batch.exp_date FROM Drug as drug INNER JOIN Batch as batch INNER JOIN Prescription_drug_map as map ON drug.drug_id=batch.drug_id and map.drug_id=batch.drug_id;
