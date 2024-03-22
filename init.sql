CREATE TABLE Products (
    ProductKey SERIAL PRIMARY KEY,
    Product VARCHAR(100),
    StandardCost DECIMAL(10, 2),
    Color VARCHAR(50),
    Subcategory VARCHAR(50),
    Category VARCHAR(50),
    BackgroundColorFormat VARCHAR(10),
    FontColorFormat VARCHAR(10)
);

CREATE TABLE Sales (
    SalesOrderNumber VARCHAR(20),
    ProductKey INTEGER,
    Quantity INTEGER,
    UnitPrice DECIMAL(10, 2)
);

CREATE TABLE SalesOrder (
    SalesOrderNumber VARCHAR(20),
    OrderDate DATE,
    ResellerKey INTEGER,
    EmployeeKey INTEGER,
    SalesTerritoryKey INTEGER
);

CREATE TABLE SalesPerson (
    EmployeeKey INTEGER PRIMARY KEY,
    EmployeeID VARCHAR(20),
    Salesperson VARCHAR(100),
    Title VARCHAR(100),
    UPN VARCHAR(100)
);

CREATE TABLE Target (
    EmployeeID VARCHAR(20),
    Target MONEY,
    TargetMonth DATE
);