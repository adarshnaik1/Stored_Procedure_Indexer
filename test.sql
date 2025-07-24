CREATE PROCEDURE sp_get_customer
    @cust_id INT
AS
BEGIN
    SELECT name, email
    FROM customer
    WHERE id = @cust_id;

    EXEC sp_get_address @cust_id;

    UPDATE customer
    SET last_accessed = GETDATE()
    WHERE id = @cust_id;

    INSERT INTO access_log (cust_id, access_time)
    VALUES (@cust_id, GETDATE());

    DELETE FROM temp_session
    WHERE cust_id = @cust_id;
END
GO

