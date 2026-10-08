import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("data.sqlite")

# 1. test_join_and_filter
df_boston = pd.read_sql(
    """
    SELECT e.firstName, e.lastName
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
    """,
    conn,
)

df_zero_emp = pd.read_sql(
    """
    SELECT o.officeCode, o.city
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL;
    """,
    conn,
)

# 2. test_type_of_join
df_employee = pd.read_sql(
    """
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName ASC, e.lastName ASC;
    """,
    conn,
)

df_contacts = pd.read_sql(
    """
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName ASC;
    """,
    conn,
)

# 3. test_builtin_function
df_payment = pd.read_sql(
    """
    SELECT c.contactFirstName, c.contactLastName, p.paymentDate, p.amount
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC;
    """,
    conn,
)

# 4. test_joining_and_grouping
df_credit = pd.read_sql(
    """
    SELECT e.employeeNumber,
           e.firstName,
           e.lastName,
           COUNT(c.customerNumber) AS num_customers
    FROM employees e
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC
    LIMIT 4;
    """,
    conn,
)

df_product_sold = pd.read_sql(
    """
    SELECT p.productName,
           COUNT(od.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
    ORDER BY totalunits DESC;
    """,
    conn,
)

# 5. test_multiple_joins
df_total_customers = pd.read_sql(
    """
    SELECT p.productName,
           p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY p.productCode, p.productName
    ORDER BY numpurchasers DESC;
    """,
    conn,
)

df_customers = pd.read_sql(
    """
    SELECT COUNT(c.customerNumber) AS n_customers,
           o.officeCode,
           o.city
    FROM offices o
    JOIN employees e
        ON o.officeCode = e.officeCode
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city;
    """,
    conn,
)

# 6. test_subquery
# STEP 10
df_under_20 = pd.read_sql("""
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT od2.productCode
    FROM orderdetails od2
    JOIN orders o2 ON od2.orderNumber = o2.orderNumber
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT o2.customerNumber) < 20
)
ORDER BY e.lastName;
""", 
conn,
)

# Close database connection
conn.close()