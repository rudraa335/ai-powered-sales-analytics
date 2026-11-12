import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('aisales.csv')
print(df.head(10))
#convert into date
df['Order_Date']=pd.to_datetime(df['Order_Date'],format="%d-%m-%Y")
#calculate monthly sales
monthly_sales=df.groupby(df['Order_Date'].dt.to_period("M"))['Sales'].sum()
print(monthly_sales)

#convert month into text
monthly_sales.index=monthly_sales.index.astype(str)

#create chart for monthly sales trend
"""plt.figure(figsize=(12,6))
plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)
plt.title("monthly sales trend")
plt.xlabel("Month")
plt.ylabel("total sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True,alpha=0.3)
plt.show()"""

#sales by category
"""category_sales=df.groupby("Category")['Sales'].sum()
plt.figure(figsize=(8,5))
plt.bar(category_sales.index,category_sales.values)
plt.title("sales by category")
plt.xlabel("category")
plt.ylabel("total sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

# category by profit
"""catgeory_profit=df.groupby("Category")['Profit'].sum()
plt.figure(figsize=(10,5))
plt.bar(catgeory_profit.index,catgeory_profit.values)
plt.title("profit by category")
plt.xlabel("category")
plt.ylabel("total profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

#top 10 products by sales
"""product_sales=df.groupby("Product")['Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
plt.barh(product_sales.index,product_sales.values)
plt.title("Products By Sales")
plt.xlabel("Products")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()"""

#top 10 products by profit
"""product_sales=df.groupby("Product")['Profit'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
plt.barh(product_sales.index,product_sales.values)
plt.title("Products By Profit")
plt.xlabel("Products")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()"""

#sales vs profit category
"""category_data=df.groupby("Category")[["Sales","Profit"]].sum()
category_data.plot(kind="bar",figsize=(10,7))
plt.title("sales vs profit by cartegory")
plt.xlabel("category")
plt.ylabel("amount")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()"""

#sales by region
"""region_sales=df.groupby("Region")['Sales'].sum()
plt.figure(figsize=(10,5))
plt.bar(region_sales.index,region_sales.values)
plt.title("sales by region")
plt.xlabel("region")
plt.ylabel("sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

#profit by region
"""region_sales=df.groupby("Region")['Profit'].sum()
plt.figure(figsize=(10,5))
plt.bar(region_sales.index,region_sales.values)
plt.title("Profit by region")
plt.xlabel("region")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""   

#discount vs profit
"""discount_profit=df.groupby("Discount")['Profit'].sum()
plt.figure(figsize=(10,6))
plt.plot(discount_profit.index,discount_profit.values,marker="o")
plt.title("discount vs profit")
plt.xlabel("discount")
plt.ylabel("profit")
plt.grid(True)
plt.show()"""

#shipping_cost vs profit
#shipping_profit=df.groupby("Shipping_Cost")['Profit'].sum()
"""plt.figure(figsize=(10,6))
plt.scatter(df['Shipping_Cost'],df['Profit'],alpha=0.3,s=15)
plt.title("shipping_cost vs profit")
plt.xlabel("Shipping_Cost")
plt.ylabel("Profit")
plt.grid(True,alpha=0.3)
plt.show()"""

#analysis
#best sales month vs worst sales month
best_month=monthly_sales.idxmax()
best_sales=monthly_sales.max()
worst_month=monthly_sales.idxmin()
worst_sales=monthly_sales.min()
best_month=pd.to_datetime(best_month)
worst_month=pd.to_datetime(worst_month)
print("best sales month:",best_month.strftime("%B %Y"))
print(best_sales)
print("worst sales month:",worst_month.strftime("%B %Y"))
print(worst_sales)


#visulaization
"""months=[best_month,worst_month]
sales=[best_sales,worst_sales]
plt.bar([best_month.strftime("%B %Y"),worst_month.strftime("%B %Y")],
sales 
)
plt.title("best month vs worst month")
plt.xlabel(" month")
plt.ylabel("sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

#MONTHLY PROFIT
"""monthly_profit=df.groupby(
    df['Order_Date'].dt.to_period("M"))['Profit'].sum()
plt.figure(figsize=(10,7))
plt.plot(monthly_profit.index.astype(str),monthly_profit.values,marker="o")
plt.title("monthly profit trend")
plt.xlabel("month")
plt.ylabel=("profit")
plt.xticks(rotation=45)
plt.grid=True
plt.tight_layout()
plt.show()"""
#top 10 products by quantity
product_quantity=(df.groupby("Product")['Quantity']).sum().sort_values(ascending=False).head(10)
"""plt.figure(figsize=(10,7))
plt.barh(product_quantity.index,product_quantity.values)
plt.title("top 10 products by quantity")
plt.xlabel("quantity sold")
plt.ylabel("product")
plt.gca().invert_yaxis()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

#profit margin by category
"""profit_margin=df.groupby("Category")[['Sales','Profit']].sum()
profit_analysis=(profit_margin['Profit']/profit_margin['Sales']*100).sort_values(ascending=False)
plt.figure(figsize=(10,7))
plt.bar(profit_analysis.index,profit_analysis.values)
plt.title("profit margin by category")
plt.xlabel("category")
plt.ylabel("profit margin by category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

#customer profit
"""customer_analysis=df.groupby("Customer_Segment")['Profit'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,7))
plt.bar(customer_analysis.index,customer_analysis.values)
plt.title("customer segment profit analysis")
plt.xlabel("customer")
plt.ylabel("profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""

#city sales
"""city_analysis=df.groupby("City")['Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,7))
plt.barh(city_analysis.index,city_analysis.values)
plt.title("city sales analysis")
plt.xlabel("profit")
plt.ylabel("city")
plt.gca().invert_yaxis()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""
"""city_analysis=df.groupby("City")['Profit'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,7))
plt.barh(city_analysis.index,city_analysis.values)
plt.title("city profit analysis")
plt.xlabel("profit")
plt.ylabel("city")
plt.gca().invert_yaxis()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""
#sales by customer segment
"""customer_analysis=df.groupby("Customer_Segment")['Sales'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,7))
plt.bar(customer_analysis.index,customer_analysis.values)
plt.title("customer segment sales analysis")
plt.xlabel("customer")
plt.ylabel("sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""
#salesman sales
"""salesman_sale=df.groupby("Salesperson")['Sales'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,7))
plt.barh(salesman_sale.index,salesman_sale.values)
plt.title("salesman sale analysis")
plt.xlabel("sales")
plt.ylabel("salesperson")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()"""

#salesperson profit
"""salesman_sale=df.groupby("Salesperson")['Profit'].sum().sort_values(ascending=False)
plt.figure(figsize=(10,7))
plt.barh(salesman_sale.index,salesman_sale.values)
plt.title("salesman profit analysis")
plt.xlabel("profit")
plt.ylabel("salesperson")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()"""
#profit margin by discount
"""discount_data=df.groupby("Discount")[['Sales','Profit']].sum()
discount_anlysis=(discount_data['Profit']/discount_data['Sales']*100)
plt.figure(figsize=(10,7))
plt.plot(discount_anlysis.index*100,discount_anlysis.values,marker="o")
plt.title("discount vs profit margin")
plt.xlabel("discount(%)")
plt.ylabel("profit margin(%)")
plt.xticks(discount_anlysis.index*100)
plt.grid(True,alpha=0.3)
plt.show()"""

