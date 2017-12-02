set hive.support.concurrency=true;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.txn.manager=org.apache.hadoop.hive.ql.lockmgr.DbTxnManager;
set hive.compactor.initiator.on=true;
set hive.compactor.worker.threads=1;


set hivevar:cur_date = current_date();
set hivevar:pre_date = date_add(${hivevar:cur_date},-1);
set hivevar:max_date = cast('2200-01-01' as date)

--the customer_name is scd1(means directly change the field's old value to new value for the record)
--the customer_street_address is scd2(means do not change the old record,just add new one but need to change the old record to expire)
--set the delete/update old record expiry_date to expire  in the customer_dim
update customer_dim
	set expiry_date = ${hivevar:pre_date}
	where customer_dim.customer_sk in
	(select a.customer_sk
		from(select customer_sk,customer_number,customer_street_address
			from customer_dim where expiry_date = ${hivevar:max_date}) a left join
		rds.customer b on a.customer_number = b.customer_number
		where b.customer_number is null or a.customer_street_address <> b.customer_street_address)

--scd2:insert a new record for the update field customer_street_address(need generate a new sk and select the right records by inner join rds.customer
--and dw.customer_dim)
insert into customer_dim
	select row_number() over(order by t1.customer_number) + t2.sk_max,
	t1.customer_number,
	t1.customer_name,
	t1.customer_street_address,
	t1.customer_zip_code,
	t1.customer_city,
	t1.customer_state,
	t1.version,
	t1.effective_date,
	t1.expiry_date
	from(
		select t2.customer_number customer_number,
		t2.customer_name customer_name,
		t2.customer_street_address customer_street_address,
		t2.customer_zip_code,
		t2.customer_city,
		t2.customer_state,
		t1.version + 1 version,
		${hivevar:pre_date} effective_date,
		${hivevar:max_date} expiry_date
		from customer_dim t1
		inner join rds.customer t2
		on t1.customer_number = t2.customer_number
		and t1.expiry_date = ${hivevar:pre_date}
		where t1.customer_street_address <> t2.customer_street_address
		) t1
	cross join (select coalesce(max(customer_sk),0) sk_max from customer_dim) t2;

--scd1:change the old customer_name value to new value

drop table if exists tmp;
select a.customer_sk,a.customer_number,b.customer_name,a.customer_street_address,a.customer_zip_code,a.customer_city,a.customer_state
a.version,a.effective_date,a.expiry_date from customer_dim a,rds.customer b
where a.customer_number = b.customer_number and a.customer_name <> b.customer_name;

delete from customer_dim where customer_dim.customer_sk in (select customer_sk from tmp);
insert into customer_dim select * from tmp;
