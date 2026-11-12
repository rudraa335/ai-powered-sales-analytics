import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv("aisales.csv")
print(df)
print(df.head(10))
print(df.columns.to_list())
print(df.dtypes)
print(df.isnull().sum())
print("\n duplicated")
print(df.duplicated().sum())
print(df.drop_duplicates)
print(df.dtypes)
#convert the date
df['Order_Date']=pd.to_datetime(df['Order_Date'],format="%d-%m-%Y")
df['Ship_Date']=pd.to_datetime(df['Ship_Date'],format="%d-%m-%Y")
print(df[['Order_Date','Ship_Date']].dtypes)
print(df.dtypes)
print(df[['Quantity','Unit_Price','Shipping_Cost','Sales','Discount','Profit']].dtypes)
#filling missing value
df['Salesperson']=df['Salesperson'].fillna("unknown")
df['Payment_Method']=df['Payment_Method'].fillna("unknown")
print(df.isnull().sum())
#checking if there is anything negative
print("negative sales:",(df['Sales']<0).sum())
print("negative quantity:",(df['Quantity']<0).sum())
print("negative unit_price:",(df['Unit_Price']<0).sum())
print("negative discount:",(df['Discount']<0).sum())
print("negative profit:",(df['Profit']<0).sum())
print("negative shipping_cost",(df['Shipping_Cost']<0).sum())
#businness metrics means total sales,order,profit
total_sales=df['Sales'].sum()
total_profit=df['Profit'].sum()
total_quantity=df['Quantity'].sum()
total_orders=len(df)
print("Total sales :",total_sales)
print("Total profit :",total_profit)
print("Total quantity:",total_quantity)
print("Total orders :",total_orders)
#sales&profit by category
category_analysis=df.groupby("Category").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity",sum)
).sort_values("total_sales",ascending=False)

print(category_analysis)
#find most profitable category
most_profitable=category_analysis["total_profit"].idxmax()
least_profitable=category_analysis["total_profit"].idxmin()

print("most profitable",most_profitable)
print("least profitable:",least_profitable)

#reason of product underperfoming
category_analysis=df.groupby("Category").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum"),
    avg_discount=("Discount","mean"),
    avg_shiipping_cost=("Shipping_Cost","mean")
)
print(category_analysis)

#product analysis
product_analysis=df.groupby("Product").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    quantity_sold=("Quantity","sum"),
    avg_dsicount=("Discount","mean")
).sort_values("total_profit")

print(product_analysis.head(10))
#lowest product nalysis
notebook=df[df["Product"]=="Notebook Pack"]
print(notebook[[
    "Sales",
    "Profit",
    "Quantity",
    "Discount",
    "Shipping_Cost"
]].describe())

product_margin=df.groupby("Product").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum")
)
product_margin["profit_margin"]=(product_margin["total_profit"]/
 product_margin["total_sales"])*100
print(product_margin.sort_values("profit_margin").head(10))
#lowest margib product
tablet=df[df["Product"]=="Tablet"]
print(tablet[[
    "Sales",
    "Profit",
    "Quantity",
    "Discount",
    "Shipping_Cost"
]].describe())
#highest margin
bookshelf=df[df["Product"]=="Bookshelf"]
print(bookshelf[[
    "Sales",
    "Profit",
    "Quantity",
    "Discount",
    "Shipping_Cost"
]].describe())

#comparision betwen highest margin vs lowest
comparision=df[df["Product"].isin(["Tablet","Bookshelf"])].groupby("Product").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum"),
    avg_discount=("Discount","mean"),
    avg_shipping_cost=("Shipping_Cost","mean")
)
comparision["profit_margin"]=(comparision["total_profit"]/comparision["total_sales"])*100

print(comparision)

#now monthly sales analysis
df['Order_Date']=pd.to_datetime(df['Order_Date'])

monthly_sales=df.groupby(df["Order_Date"].dt.to_period("M")).agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum"),
    avg_discount=("Discount","mean"),
    avg_shipping_cost=("Shipping_Cost","mean")
)
print("\n monthlty sales")
#worst sales
worst_month_sales=monthly_sales['total_sales'].idxmin()
print(worst_month_sales)
best_month_sales=monthly_sales['total_sales'].idxmax()
print(best_month_sales)
sales_diffrence=("sales diffrence:",monthly_sales.loc[best_month_sales,'total_sales']-monthly_sales.loc[worst_month_sales,'total_sales'])
print("sales diff:",sales_diffrence)
#best profit
best_month_profit=monthly_sales['total_profit'].idxmax()
print(best_month_profit)
worst_month_profit=monthly_sales['total_profit'].idxmin()
print(worst_month_profit)
profit_diffrence=(monthly_sales.loc[best_month_profit,'total_profit']-monthly_sales.loc[worst_month_profit,'total_profit'])
print("profit diff:",profit_diffrence)
#quantity 
quantity_diffrence=(monthly_sales.loc[best_month_sales,'total_quantity']-monthly_sales.loc[worst_month_sales,'total_quantity'])
print("quantity diffrence:",quantity_diffrence)

#sale and profit percentage diffrence
"""sales_percentage_diffrence=(sales_diffrence/monthly_sales.loc[worst_month,'total_sales'])*100

profit_percentage_diffrence=(profit_diffrence/monthly_sales.loc[best_month,'total_sales'])*100

print("percentage diff\n")
print("sales diffrence %",sales_percentage_diffrence)
print("profit diffrence %",profit_percentage_diffrence)"""

#category comparision in month
best_month=df[df['Order_Date'].dt.to_period("M")==best_month_sales]
worst_month=df[df['Order_Date'].dt.to_period("M")==worst_month_sales]
best_category=best_month.groupby("Category").agg(
    sales=("Sales","sum"),
    profit=("Profit","sum"),
    quantity=("Quantity","sum")
)
worst_category=worst_month.groupby("Category").agg(
    sales=("Sales","sum"),
    profit=("Profit","sum"),
    quantity=("Quantity","sum")

)
category_compare=best_category-worst_category
print("category comparision:",category_compare)

#product comparision
#best electronic product
best_electronic_product=best_month[best_month["Category"]=="Electronics"].groupby("Product").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
).sort_values("total_sales",ascending=False)

worst_electronic_product=worst_month[worst_month['Category']=="Electronics"].groupby("Product").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
)  
print("--\n electronic best product--\n")
print(best_electronic_product)
print("\n --- worst product--\n")
print(worst_electronic_product)

#product diffrence
product_diffrence=best_electronic_product['total_sales']-worst_electronic_product['total_sales'].sort_values(ascending=False)
print("\n --- product diffrence ---\n")
print(product_diffrence)

#profuct ontribution 
product_contributtion=(product_diffrence/product_diffrence.sum())*100
print("\n--- prduct contribution to electronic sales---\n")
print(product_contributtion.sort_values(ascending=False))

#customer analysis
#top customer by sales
customer_analysis=df.groupby("Customer_Name").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
).sort_values("total_sales",ascending=False)
print("--\n top 10 customer order by sales")
print(customer_analysis.head(10))
#top customer by profit
top_profit_customer=customer_analysis.sort_values("total_profit",ascending=False)
print("\n---top 10 customer by profit--\n")
print(top_profit_customer.head(10))
#sales leader vs profit leader
sales_leader=customer_analysis['total_sales'].idxmax()
profit_leader=customer_analysis['total_profit'].idxmax()

print("\n top customer by sales:",sales_leader)
print(" sales:",customer_analysis.loc[sales_leader,'total_sales'])
print("\n top customer by profit:",profit_leader)
print("profit:",customer_analysis.loc[profit_leader,'total_profit'])

# cusomer margin
customer_analysis['profit_margin']=(customer_analysis['total_profit']/customer_analysis['total_sales'])*100
top_margin_customer=customer_analysis.sort_values('profit_margin',ascending=False)
print("\n-- top margin customers--\n")
print(top_margin_customer.head(10))

#customer segment
segment_analysis=df.groupby("Customer_Segment").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
)
segment_analysis['profit_margin']=(segment_analysis['total_profit']/segment_analysis['total_sales'])*100
print("\n--- customer segment analysis---\n")
print(segment_analysis)
#customer loosing money
loss_customer=customer_analysis.sort_values("total_profit",ascending=True)
print("\n--- customer with lowest profit--\n")
print(loss_customer.head(10))
#why these customer loosing money
loss_customer=df[df['Customer_Name']=="Customer 4592"]
print(loss_customer[[
    "Sales",
    "Profit",
    "Quantity",
    "Product",
    "Discount",
    "Shipping_Cost"
]])
#investigate product into more deeper
laptop_air=df[df['Product']=='Laptop Air 13']
print(laptop_air[['Sales','Profit','Quantity','Discount','Shipping_Cost']].sort_values("Profit").head(10))

#now regional analysis
regional_anlysis=df.groupby('Region').agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
)
top_region_sales=regional_anlysis['total_sales'].idxmax()
low_region_sales=regional_anlysis['total_sales'].idxmin()
print("--top region in sales--")
print(top_region_sales)
print("\n--worst region in sales--\n")
print(low_region_sales)
#region margin
regional_anlysis['profit_margin']=(regional_anlysis['total_profit']/regional_anlysis['total_sales'])*100
print("\n---regional analysis---\n")
print(regional_anlysis.sort_values("total_sales",ascending=False)) 
#city analysis
city_analysis=df.groupby("City").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
)
city_analysis['profit_margin']=(city_analysis['total_profit']/city_analysis['total_sales'])*100
print("\n---city anlysis ---\n")
print(city_analysis.sort_values('total_sales',ascending=False))
print("\n---bottom 10 cities by sales---")
print(city_analysis.sort_values("total_sales",ascending=True))

#why delhi has lowest margin among all 
delhi_analysis=df[df['City']=='Delhi'].agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum"),
    avg_discount=("Discount","mean"),
    avg_shiiping_cost=("Shipping_Cost","mean")
)
print("\n---delhi analysis---\n")
print(delhi_analysis)
#compare overall businesss analysis vs delhi analysis
overall_analysis=df.agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum"),
    avg_discount=("Discount","mean"),
    avg_shiiping_cost=("Shipping_Cost","mean")
)
print("---overall analysis---\n")
print(overall_analysis)
print(delhi_analysis.columns)
print("\n---delhi vs overall---\n")
print("delhi discount:",delhi_analysis["Discount"])
print("overall discount:",overall_analysis["Discount"])

print("delhi shipping cost:",delhi_analysis["Shipping_Cost"])
print("overall shipping cost:",overall_analysis["Shipping_Cost"])

print(df.columns)
#now salesperson analysis
salesperson_analysis=df.groupby("Salesperson").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
)
salesperson_analysis['profit_margin']=(salesperson_analysis['total_profit']/salesperson_analysis['total_sales'])*100
print("\n--sales person analysis--\n")
print(salesperson_analysis)
top_margin_salesperson=salesperson_analysis.sort_values("profit_margin",ascending=False)
print("\n --- top sales person by margin---\n")
print(top_margin_salesperson.head(10))

#sales person by quantity
salesperson_quantity=salesperson_analysis.sort_values('total_quantity',ascending=False)
print("\n--sales person by quantity--\n")
print(salesperson_quantity.head(10))

#average sales per quantity
salesperson_analysis['sales_per_unit']=(salesperson_analysis['total_sales']/salesperson_analysis['total_quantity'])
print("\n--sales per unit--\n")
print(salesperson_analysis.sort_values("sales_per_unit",ascending=False))

#discount vs profit
discount_analysis=df.groupby("Discount").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
)
discount_analysis['profit_margin']=(discount_analysis['total_profit']/discount_analysis['total_sales'])*100
print("\n--discount vs profit---\n")
print(discount_analysis)

#shipping cost vs profit
shipping_analysis=df.groupby(pd.qcut(df['Shipping_Cost'],5,duplicates="drop")).agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_quantity=("Quantity","sum")
)
shipping_analysis['profit_margin']=(shipping_analysis['total_profit']/shipping_analysis['total_sales'])*100
print("\n--shipping vs profit--\n")
print(shipping_analysis)

#product  profitability
product_analysis['profit_margin']=(product_analysis['total_profit']/product_analysis['total_sales'])*100
print(product_analysis.sort_values("total_sales",ascending=False))

#high sales + low margin product
high_sales_low_margin=product_analysis[product_analysis['total_sales']>product_analysis['total_sales'].median()].sort_values('profit_margin')
print("\n--high sales + low margin--\n")
print(high_sales_low_margin)

high_margin_product=product_analysis.sort_values("profit_margin",ascending=False)
print("\n-- top 10 product by margin--\n")
print(high_margin_product.head(10))

#category analysis
category_analysis['profit_margin']=(category_analysis['total_profit']/category_analysis['total_sales'])*100
print(category_analysis.sort_values('total_profit',ascending=False))

#bussiness important insightss
#print(overall_analysis.columns)
#overall margib
overall_profit_margin=(overall_analysis.loc['total_profit'].iloc[1]/overall_analysis.loc['total_sales'].iloc[0]*100)
print("\n---overall profit margin---\n")
print(overall_profit_margin)
#best and worst category by profit
category_profit=df.groupby("Category")['Profit'].sum()
best_category=category_profit.idxmax()
worst_category=category_profit.idxmin()
print("\n--- best and worst category by profit--\n")
print("best category:",best_category)
print("worst category:",worst_category)

#best and worst product by profit
product_profit=df.groupby("Product")['Profit'].sum()
best_product=product_profit.idxmax()
worst_product=product_profit.idxmin()
print("\n--- best and worst product by profit--\n")
print("best product:",best_product)
print("worst product:",worst_product)

#best nad worst sales by month
monthly_sales=df.groupby(df['Order_Date'].dt.to_period("M"))['Sales'].sum()
best_month=monthly_sales.idxmax()
worst_month=monthly_sales.idxmin()
print("\n-- best and worst months--\n")
print("best sales month:",best_month)
print("worst sales month:",worst_month)

#best and worst region by profit
region_profit=df.groupby("Region")['Profit'].sum()
best_region=region_profit.idxmax()
worst_region=region_profit.idxmin()
print("\n best and worst region\n")
print("best region by profit is:",best_region)
print("worst region by profit is:",worst_region)

#best and worst customer segment by profit
customer_profit=df.groupby("Customer_Segment")['Profit'].sum()
best_customer=customer_profit.idxmax()
worst_customer=customer_profit.idxmin()
print("\n--- best and worst customer segment ---")
print("best customer segment is:",best_customer)
print("worst customer segment is:",worst_customer)

#best and worst salesman
salesman_profit=df.groupby("Salesperson")['Profit'].sum()
best_salesperson=salesman_profit.idxmax()
worst_salesperson=salesman_profit.idxmin()
print("\n--- best and worst salesperson ---")
print("best salesperson is:",best_salesperson)
print("worst salesperson is:",worst_salesperson)

