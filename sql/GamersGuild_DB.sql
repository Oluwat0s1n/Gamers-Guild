-- DATABASE CREATION
CREATE DATABASE IF NOT EXISTS GamersGuildDB;
USE GamersGuildDB;

-- TABLE: Admin
CREATE TABLE Admin (
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL -- store SHA-256 or other hashed value from Python
);

-- TABLE: Customer
CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Address VARCHAR(120),
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL, -- hashed
    RegisteredDate DATE DEFAULT CURRENT_DATE,
    ActiveStatus VARCHAR(20) DEFAULT 'Active'
);

-- TABLE: Game
CREATE TABLE Game (
    GameID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    Genre VARCHAR(50),
    Price DECIMAL(10,2) NOT NULL,
    Type ENUM('Physical', 'Digital') NOT NULL,
    AdminID INT,
    Stock VARCHAR(10),
    ImagePath VARCHAR(255),
    FOREIGN KEY (AdminID) REFERENCES Admin(AdminID)
        ON DELETE SET NULL
);

-- TABLE: Inventory
CREATE TABLE Inventory (
    InventoryID INT AUTO_INCREMENT PRIMARY KEY,
    GameID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
        ON DELETE CASCADE
);

-- TABLE: Cart
CREATE TABLE Cart (
    CartID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    GameTitle VARCHAR(255),
    Price DECIMAL(10,2),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
        ON DELETE CASCADE
);

-- TABLE: Cart_Details
CREATE TABLE Cart_Details (
    CartDetailID INT AUTO_INCREMENT PRIMARY KEY,
    CartID INT NOT NULL,
    GameID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (CartID) REFERENCES Cart(CartID)
        ON DELETE CASCADE,
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
        ON DELETE CASCADE
);

-- TABLE: Order
CREATE TABLE `Order` (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATE DEFAULT CURRENT_DATE,
    Status VARCHAR(50) DEFAULT 'Pending',
    TotalAmount DECIMAL(10,2),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
        ON DELETE CASCADE
);

-- TABLE: OrderItems
CREATE TABLE OrderItems (
    OrderItemID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    GameID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID)
        ON DELETE CASCADE,
    FOREIGN KEY (GameID) REFERENCES Game(GameID)
        ON DELETE CASCADE
);

-- TABLE: Payment
CREATE TABLE Payment (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    PaymentDate DATE DEFAULT CURRENT_DATE,
    Method ENUM('Card', 'Cash', 'Crypto') DEFAULT 'Card',
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID)
        ON DELETE CASCADE
);

-- TABLE: Library
CREATE TABLE Library (
    LibraryID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    GameTitle VARCHAR(255),
    PurchaseDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
        ON DELETE CASCADE
);

-- TABLE: Community
CREATE TABLE Community (
    PostID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    Title VARCHAR(100) NOT NULL,
    Content TEXT,
    PostDate DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
        ON DELETE CASCADE
);
