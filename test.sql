CREATE PROCEDURE sp_get_customer_orders
    @cust_id INT
AS
BEGIN
    SELECT order_id, order_date, amount
    FROM orders
    WHERE customer_id = @cust_id;
END;

CREATE PROCEDURE sp_get_customer_full_details
    @cust_id INT
AS
BEGIN
   
    SELECT customer_id, customer_name, email
    FROM customers
    WHERE customer_id = @cust_id;

    
    EXEC sp_get_customer_orders @cust_id;
END;


