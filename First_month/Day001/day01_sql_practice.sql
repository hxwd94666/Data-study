--牛客-在线编程-sql必知必会练手
select cust_id from Customers;

select distinct(prod_id) from OrderItems;

select cust_id,cust_name from Customers;

select cust_name
from Customers
order by cust_name desc;

select cust_id,order_num
from Orders
order by cust_id asc,order_date desc;

select quantity,item_price
from OrderItems
order by quantity desc,item_price desc;
