create table visit_payment_copy like visit_payment;
insert into visit_payment_copy select * from visit_payment group by visit_id, paytime;
rename table visit_payment to visit_payment_orig, visit_payment_copy to visit_payment;

