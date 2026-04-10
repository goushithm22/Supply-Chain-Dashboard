import pandas as pd 
from faker import Faker
import random 
from datetime import timedelta

fake = Faker()
random.seed(42)

# Table 1 : SUPPLIER'S TABLE

SuppliersData = [
  ("SUP001", "FastShip Logistics",  "Mumbai",   "India",   4.2, 95),
    ("SUP002", "GlobalParts Co",      "Shanghai", "China",   3.8, 88),
    ("SUP003", "QuickDeliver Ltd",    "Dubai",    "UAE",     4.5, 97),
    ("SUP004", "MegaSupply Inc",      "New York", "USA",     4.0, 91),
    ("SUP005", "EuroGoods GmbH",      "Berlin",   "Germany", 4.7, 99),
]

Suppliersdf = pd.DataFrame(SuppliersData, columns=[
  "SuppliersId", "SuppliersName", "SuppliersState", "SupplierCountry", "SupplierRating", "OnTimeDeliverypct"
])

# Table 2 : PRODUCTS

ProductsTable = [
  ("PRD001", "Wireless Earbuds",   "Electronics",    "SUP002", 450,  1200),
    ("PRD002", "Running Shoes",      "Apparel",        "SUP001", 900,  2800),
    ("PRD003", "Coffee Maker",       "Home & Kitchen", "SUP004", 1200, 3500),
    ("PRD004", "Yoga Mat",           "Sports",         "SUP001", 250,  800),
    ("PRD005", "Sunscreen SPF50",    "Beauty",         "SUP003", 180,  550),
    ("PRD006", "Bluetooth Speaker",  "Electronics",    "SUP002", 600,  1800),
    ("PRD007", "Denim Jacket",       "Apparel",        "SUP005", 1100, 3200),
    ("PRD008", "Air Fryer",          "Home & Kitchen", "SUP004", 2000, 5500),
    ("PRD009", "Tennis Racket",      "Sports",         "SUP003", 700,  2200),
    ("PRD010", "Face Moisturizer",   "Beauty",         "SUP005", 300,  950),
]

Productsdf = pd.DataFrame(ProductsTable, columns=[
  "ProductId", "ProductName", "category", "SupplierId", "UnitCost", "UnitPrice"
])

# Table 3 : ORDERS

Orders = []


for i in range(1, 501):  # generate 500 orders
    order_id   = f"ORD{i:04d}"                              # ORD0001, ORD0002...
    product    = random.choice(ProductsTable)               # pick a random product
    product_id = product[0]
    quantity   = random.randint(1, 50)
    unitPrice = product[5]
    unitCost  = product[4]
    revenue    = quantity * unitPrice
    cost       = quantity * unitCost
    profit     = revenue - cost
    orderDate = fake.date_between(start_date="-2y", end_date="today")
    region     = random.choice(["North", "South", "East", "West"])
    status     = random.choices(
        ["Completed", "Pending", "Cancelled"],
        weights=[75, 15, 10]   # 75% completed, 15% pending, 10% cancelled
    )[0]
    
    Orders.append([
        order_id, product_id, quantity, unitPrice,
        unitCost, revenue, cost, profit,
        orderDate, region, status
    ])
    
Ordersdf = pd.DataFrame(Orders, columns=[
    "order_id", "product_id", "quantity", "unitPrice",
    "unitCost", "revenue", "cost", "profit",
    "orderDate", "region", "status"
])


# TABLE 4 : SHIPMENTS

Shipments = []
for _, order in Ordersdf.iterrows():
   ship_date    = pd.to_datetime(order["orderDate"]) + timedelta(days=random.randint(1, 3))
   promised     = random.randint(5, 10)
   actual       = promised + random.choices(
        [-1, 0, 1, 2, 3, 5],
        weights=[10, 40, 20, 15, 10, 5]  # mostly on time, sometimes late
    )[0]
   is_late      = actual > promised
   carrier      = random.choice(["DHL", "FedEx", "BlueDart", "Aramex", "UPS"])

   Shipments.append([
        f"SHP{_+1:04d}",
        order["order_id"],
        ship_date.strftime("%Y-%m-%d"),
        promised,
        actual,
        is_late,
        carrier
    ])
   
Shipmentsdf = pd.DataFrame(Shipments, columns=[
  "shipment_id", "order_id", "shipDate",
    "promisedDays", "actualDays", "isLate", "carrier"
])

# SAVING ALL FILES IN THE DATA FOLDER

Suppliersdf.to_csv("../data/suppliers.csv", index=False)
Productsdf.to_csv("../data/products.csv", index=False)
Ordersdf.to_csv("../data/orders.csv", index=False)
Shipmentsdf.to_csv("../data/shipment.csv", index=False)

print("suppliers.csv  →", len(Suppliersdf),  "rows")
print("products.csv   →", len(Productsdf),   "rows")
print("orders.csv     →", len(Ordersdf),     "rows")
print("shipments.csv  →", len(Shipmentsdf),  "rows")
print("\nAll files saved to /data folder.")