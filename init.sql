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
    
CREATE TABLE Sales (
    SK_Sales SERIAL PRIMARY KEY,
    SalesOrderNumber VARCHAR(15),
    ProductKey VARCHAR(20),
    Quantity INTEGER,
    UnitPrice DECIMAL(10, 2),
    Cost DECIMAL(10, 2),
    LoadTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SalesOrder (
    SK_SalesOrder SERIAL PRIMARY KEY,
    SalesOrderNumber VARCHAR(15),
    OrderDate DATE,
    ResellerKey INTEGER,
    EmployeeKey INTEGER,
    SalesTerritoryKey INTEGER,
    LoadTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SalesPerson (
    SK_SalesPerson SERIAL PRIMARY KEY,
    EmployeeKey INTEGER,
    EmployeeID INTEGER,
    Salesperson VARCHAR(100),
    Title VARCHAR(50),
    UPN CHAR(320),
    LoadTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
