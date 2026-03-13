--牛客在线编程-sql必知必会96-100
select
    c.cust_name,
    o.order_num
from Customers c
inner join Orders o
    ON c.cust_id = o.cust_id
order by
    c.cust_name,
    o.order_num;

select
    cust_name,
    o1.order_num,
    quantity*item_price OrderTotal
from Customers c
inner join Orders o1
    on c.cust_id = o1.cust_id
inner join OrderItems o2
    on o1.order_num= o2.order_num
order by c.cust_name,o1.order_num;

--直接连接
select
    cust_id,
    order_date
from OrderItems o1
inner join Orders o2
    on o1.order_num=o2.order_num
where o1.prod_id='BR01'
order by order_date;
--子查询
select
    cust_id,
    order_date
from Orders
where order_num in
(select order_num
from OrderItems
where prod_id='BR01')
order by order_date;

select cust_email
from OrderItems o1
inner join Orders o2
    on o1.order_num=o2.order_num
inner join Customers c
    on c.cust_id=o2.cust_id
where o1.prod_id='BR01';

select
    cust_name,
    sum(item_price*quantity) total_price
from OrderItems o1
inner join Orders o2
    on o1.order_num=o2.order_num
inner join Customers c
    on c.cust_id=o2.cust_id
group by cust_name
having total_price>=1000
order by total_price;