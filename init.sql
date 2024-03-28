CREATE TABLE Products (
    SK_Product SERIAL PRIMARY key,
    ProductKey INTEGER,
    Product VARCHAR(100),
    StandardCost DECIMAL(10, 2),
    Color VARCHAR(20),
    Subcategory VARCHAR(50),
    Category VARCHAR(50),
    BackgroundColorFormat CHAR(7),
    LoadTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Target (
    SK_Target SERIAL PRIMARY KEY,
    EmployeeID INTEGER,
    Target DECIMAL(10,2),
    TargetMonth DATE,
    LoadTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
    


-- CREATE TABLE Sales (
--     SalesOrderNumber VARCHAR(20),
--     ProductKey INTEGER,
--     Quantity INTEGER,
--     UnitPrice DECIMAL(10, 2)
-- );

-- CREATE TABLE SalesOrder (
--     SalesOrderNumber VARCHAR(20),
--     OrderDate DATE,
--     ResellerKey INTEGER,
--     EmployeeKey INTEGER,
--     SalesTerritoryKey INTEGER
-- );

-- CREATE TABLE SalesPerson (
--     EmployeeKey INTEGER PRIMARY KEY,
--     EmployeeID VARCHAR(20),
--     Salesperson VARCHAR(100),
--     Title VARCHAR(100),
--     UPN VARCHAR(100)
-- );

-- CREATE TABLE Target (
--     SK_Employee SERIAL PRIMARY KEY,
--     EmployeeID INTEGER,
--     Target DECIMAL(10,2),
--     TargetMonth DATE,
--     Load_Time DATETIMESTAMP,
-- );