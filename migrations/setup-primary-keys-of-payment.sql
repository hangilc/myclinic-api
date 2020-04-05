drop index visit_id on visit_payment;
alter table visit_payment add primary key (visit_id, paytime);
