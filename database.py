import psycopg2
import pandas as pd 
import streamlit as st
conn=psycopg2.connect(
    host="localhost",
    database="sales_analytics",
    user="postgres",
    password=*****,  # <-- replaced private password
    port=5432
)
cursor=conn.cursor()

#THIS FUNCTION LOADS THE DATAFRAME FROM THE USER TO THE DATABASE 
def load_data(data):

    try:
        with open("counter.txt", "r") as f:
            unq = int(f.read())
    except:
        with open("counter.txt", "w") as f:
            f.write("0")
            unq=0
    unq+=1
    name="sales_transaction" + str(unq)
    cursor.execute(f"""
                   CREATE TABLE {name} (
                    order_id INT,
                    order_date DATE,
                    customer_id INT,
                    customer_name TEXT,
                    product_name TEXT,
                    category TEXT,
                    region TEXT,
                    quantity INT,
                    unit_price NUMERIC,
                    discount NUMERIC,
                    sales_amount NUMERIC
                );
                   """)
    for index,row in data.iterrows(): 
        cursor.execute(f"""
                    INSERT INTO {name}(
                        order_id, order_date, customer_id, customer_name,
                        product_name, category, region, quantity,
                        unit_price, discount, sales_amount
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                        row['order_id'],
                        row['order_date'],
                        row['customer_id'],
                        row['customer_name'],
                        row['product_name'],
                        row['category'],
                        row['region'],
                        row['quantity'],
                        row['unit_price'],
                        row['discount'],
                        row['sales_amount']
                    ) )
    conn.commit()
    with open("counter.txt", "w") as f:
            f.write(f"{unq}") 
    return name 

# THIS FUNCTION EXECUTES A QUERY AND GIVES TOTAL REVENUE DATA
def total_revenue(name):
    cursor.execute(f"""
                SELECT SUM(sales_amount) AS total_revenue
                FROM {name};
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES THE REVENUE BY REGION
def revenue_by_region(name):
    cursor.execute(f"""
                SELECT region, SUM(sales_amount) AS total_revenue
                FROM {name}
                GROUP BY region
                ORDER BY total_revenue DESC
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES REVENUE BY CATEGORY
def revenue_by_category(name):
    cursor.execute(f"""
                SELECT category, SUM(sales_amount) AS total_revenue
                FROM {name}
                GROUP BY category
                ORDER BY total_revenue DESC;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES REVENUE BY PRODUCT
def revenue_by_product(name):
    cursor.execute(f"""
                SELECT product_name, SUM(sales_amount) AS total_revenue
                FROM {name}
                GROUP BY product_name
                ORDER BY total_revenue DESC;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

def revenue_over_time(name):
    cursor.execute(f"""
                SELECT EXTRACT(YEAR FROM order_date) AS year,
                       EXTRACT(MONTH FROM order_date) AS month,
                       SUM(sales_amount) AS total_revenue
                FROM {name}
                GROUP BY year, month
                ORDER BY year, month;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES TOTAL NUMBER OF ORDERS
def total_number_of_orders(name):
    cursor.execute(f"""
                SELECT COUNT(order_id) AS total_orders
                FROM {name};
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES AVERAGE ORDER VALUE
def average_order_value(name):
    cursor.execute(f"""
                SELECT ROUND(AVG(sales_amount), 2) AS avg_order_value
                FROM {name};
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES ORDERS OVER TIME
def orders_over_time(name):
    cursor.execute(f"""
                SELECT EXTRACT(YEAR FROM order_date) AS year,
                       EXTRACT(MONTH FROM order_date) AS month,
                       COUNT(order_id) AS total_orders
                FROM {name}
                GROUP BY year, month
                ORDER BY year, month;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES TOP 10 PRODUCTS BY REVENUE
def top_products_by_revenue(name):
    cursor.execute(f"""
                SELECT product_name, SUM(sales_amount) AS total_revenue
                FROM {name}
                GROUP BY product_name
                ORDER BY total_revenue DESC
                LIMIT 10;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES TOP 10 PRODUCTS BY QUANTITY SOLD
def top_products_by_quantity(name):
    cursor.execute(f"""
                SELECT product_name, SUM(quantity) AS total_quantity
                FROM {name}
                GROUP BY product_name
                ORDER BY total_quantity DESC
                LIMIT 10;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES WORST PERFORMING PRODUCTS
def worst_performing_products(name):
    cursor.execute(f"""
                SELECT product_name, SUM(sales_amount) AS total_revenue
                FROM {name}
                GROUP BY product_name
                ORDER BY total_revenue ASC
                LIMIT 5;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES TOP 10 CUSTOMERS BY REVENUE
def top_customers_by_revenue(name):
    cursor.execute(f"""
                SELECT customer_name, SUM(sales_amount) AS total_revenue
                FROM {name}
                GROUP BY customer_name
                ORDER BY total_revenue DESC
                LIMIT 10;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES AVERAGE SPEND PER CUSTOMER
def average_spend_per_customer(name):
    cursor.execute(f"""
                SELECT ROUND(AVG(sales_amount), 2) AS avg_spend
                FROM {name}
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES AVERAGE DISCOUNT BY CATEGORY
def average_discount_by_category(name):
    cursor.execute(f"""
                SELECT category, ROUND(AVG(discount), 2) AS avg_discount
                FROM {name}
                GROUP BY category
                ORDER BY avg_discount DESC;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

# THIS FUNCTION GIVES IMPACT OF DISCOUNT ON SALES AMOUNT
def discount_impact(name):
    cursor.execute(f"""
                SELECT discount,
                       ROUND(AVG(sales_amount), 2) AS avg_sales_amount,
                       COUNT(order_id) AS number_of_orders
                FROM {name}
                GROUP BY discount
                ORDER BY discount ASC;
                   """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data

def tables_in_database():
    cursor.execute(""" 
                  SELECT table_name 
                  FROM information_schema.tables 
                  WHERE table_schema = 'public';
                  """)
    data = cursor.fetchall()
    data = pd.DataFrame(data)
    return data















































def main():
    name = "sales_transaction8"
    
    

main()
    


    

    
        
                                    
