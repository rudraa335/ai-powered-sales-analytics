import os
import pandas as pd
from openai import OpenAI
import mysql.connector

client=OpenAI(api_key=os.environ.get("GROQ_API_KEY"),base_url="https://api.groq.com/openai/v1")
connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.environ.get("MYSQL_PASSWORD"),
    database="sales_analysis"
)

df=pd.read_sql("select * from sales",connection)
print("mysql collunms:",df.columns.tolist())
df.columns=df.columns.str.strip().str.title()
connection.close()
print("data loaded from mysql succesfully!")
df['Product']=df['Product'].astype("string").str.strip()
df['Profit']=pd.to_numeric(df['Profit'],errors="coerce")
df_clean=df.dropna(subset=['Product','Profit'])
df_clean=df_clean[df_clean['Product']!=""]
#clean colunm names
df.columns=df.columns.str.strip()
#convert import colunms to numeric
for colunms in ['Sales','Profit','Quantity','Discount','Shipping_Cost']:
    df[colunms]=pd.to_numeric(df[colunms],errors="coerce")

df=df.dropna(subset=['Sales','Profit','Quantity'])
print("\n--------------")
print("ai sales analyst")
print("-----------------")
print(f"dataset loaded:{len(df):,}records")
print("ask question about your sales data:")
print("type 'exit' to stop.\n")

while True:
    question=input("You:").strip()

    if question.lower() in['exit','quit']:
        print("AI Analyst:GoodBye!")
        break
    if not question:
        continue
#calculate verified datset from result
    question_lower = question.lower()
    result=None
    if "compare" in question_lower :
        products=df['Product'].dropna().unique() 
        clean_question="".join(question_lower.split())
        print("debug clean question:",clean_question)
        matched_products = [
        product for product in df['Product'].dropna().unique()
            if str(product).lower() in question_lower
        ]
        print("debug matched product",matched_products)
        print("debug matched product",matched_products)
        if len(matched_products)>=2:
               comparision=df[df['Product'].isin(matched_products[:2])]
               comparision=comparision.groupby("Product").agg(
                     total_sales=("Sales","sum"),
                     total_profit=("Profit","sum"),
                     total_quantity=("Quantity","sum")
               )
               comparision['profit_margin']=(comparision['total_profit']/comparision['total_sales'].replace(0,float('nan'))*100)
               result="product comparision:\n"+comparision.to_string()
               sales_winner=comparision['total_sales'].idxmax()
               profit_winner=comparision['total_profit'].idxmax()
               quantity_winner=comparision['total_quantity'].idxmax()
               margin_winner=comparision["profit_margin"].idxmax()
               winner_summary=f""" automatic winner detaction
               highest sales:{sales_winner}
               highest profit:{profit_winner}
               highest quantity:{quantity_winner}
               highest margin:{margin_winner}
               """
               result=("product comparision:\n"+comparision.to_string()+"\n"+winner_summary)
        else:
              result="please mention two valid names to compare"
    
    elif "profit" in question_lower and "product" in question_lower:
        profit_by_product=df.groupby("Product")['Profit'].sum().sort_values()
        if "lowest" in question_lower or"least" in question_lower:
            product=profit_by_product.index[0]
            amount=profit_by_product.iloc[0]
            result=f"product with lowest total profit:{product}.total profit:{amount:,.2f}"
        else:
            product=profit_by_product.index[-1]
            amount=profit_by_product.iloc[-1]
            result=f"product with highest total profit:{product}.total profit:{amount:,.2f}"
    elif "region" in question_lower and "profit" in question_lower:
            profit_by_region=df.groupby("Region")['Profit'].sum().sort_values(ascending=False)
            if "lowest" in question_lower or "least" in question_lower:
                region=profit_by_region.idxmin()
                amount=profit_by_region.min()
                result=f"region with lowest:{region}.total profit:{amount:,.2f}"
            else:
                region=profit_by_region.idxmax()
                amount=profit_by_region.max()
                result=f"region with highest :{region}.total profit:{amount:,.2f}"
    elif "sales" in question_lower and ("total" in question_lower or "overall" in question_lower):
        result=f"total sales accross the datset:{df['Sales'].sum():,.2f}"
    elif "category" in question_lower and "profit" in question_lower:
                profit_by_category=(df.groupby("Category")['Profit'].sum().sort_values())
                if profit_by_category.empty:
                     result="no category profit avauiulable"
                elif "lowest" in question_lower or "least" in question_lower:
                    category= profit_by_category.index[0]
                    amount=profit_by_category.iloc[0]
                    result=(f"category with lowest total profit:{category}.total profit{amount:,.2f}")
                else:
                     category= profit_by_category.index[-1]
                     amount=profit_by_category.iloc[-1]
                     result=(f"category with highest total profit:{category}.total profit{amount:,.2f}")
    elif "salesperson" in question_lower and "profit" in question_lower:
        sales_data=df.copy()
        sales_data['Salesperson']=(sales_data['Salesperson'].astype("string").str.strip())
        sales_data=sales_data.dropna(subset=['Salesperson'])
        sales_data=sales_data[sales_data["Salesperson"]!=""]
        profit_by_salesperson=(sales_data.groupby('Salesperson')['Profit'].sum().sort_values())
        if profit_by_salesperson.empty:
              result="no salesperson profit available"
        elif "lowest" in question_lower or "least" in question_lower:
              salesperson=profit_by_salesperson.index[0]
              amount=profit_by_salesperson.iloc[0]
              result=(f"salesperson with lowest total profit:{salesperson}.total profit{amount:,.2f}")
        else:
              salesperson=profit_by_salesperson.index[-1]
              amount=profit_by_salesperson.iloc[-1]
              result=(f"salesperson with highest total profit:{salesperson}.total profit{amount:,.2f}")
    elif "segment" in question_lower and "profit" in question_lower:
                    profit_by_customer=(df.groupby("Customer_Segment")['Profit'].sum().sort_values())
                    if profit_by_customer.empty:
                         result="no category profit avauiulable"
                    elif "lowest" in question_lower or "least" in question_lower:
                        segment= profit_by_customer.index[0]
                        amount=profit_by_customer.iloc[0]
                        result=(f"segment with lowest total profit:{segment}.total profit{amount:,.2f}")
                    else:
                         segment= profit_by_customer.index[-1]
                         amount=profit_by_customer.iloc[-1]
                         result=(f"segment with highest total profit:{segment}.total profit{amount:,.2f}")
    elif "discount" in question_lower and ("profit" in question_lower or "margin" in question_lower):
                    discount_analysis=(df.groupby("Discount").agg(total_sales=("Sales","sum"),total_profit=("Profit","sum")))
                    discount_analysis=discount_analysis[discount_analysis['total_sales']!=0]
                    discount_analysis['profit_margin']=(discount_analysis['total_profit']/discount_analysis['total_sales'])*100
                    if discount_analysis.empty:
                         result="no valid discount data"
                    elif "highest" in question_lower or"best" in question_lower:
                        discount= discount_analysis['profit_margin'].idxmax()
                        margin= discount_analysis['profit_margin'].max()
                        result=(f"discount with highest profit margin:"f"{discount:.0%}.profit margin:{margin:.2f}%")
                    elif "lowest" in question_lower or "least" in question_lower:
                         discount=discount_analysis['profit_margin'].idxmin()
                         margin=discount_analysis['profit_margin'].min()
                         result=(f"discount with lowest profit margin:"f"{discount:.0%}.profit margin{margin:.2f}%")
                    else:
                         result="ask for the highest or lowest profit by margin"

    elif "shipping" in question_lower and ("profit" in question_lower or "margin" in question_lower):
                        df['Shipping_Range']=pd.cut(df['Shipping_Cost'],bins=[-float("inf"),500,1000,2000,float("inf")],labels=['low (<=500)','medium(501-1000)','high(1001-2000)','very_high(>2000)'])
                        shipping_analysis=(df.groupby("Shipping_Range",observed=False).agg(total_sales=("Sales","sum"),total_profit=("Profit","sum")))
                        shipping_analysis=shipping_analysis[shipping_analysis['total_sales']!=0]
                        shipping_analysis['profit_margin']=(shipping_analysis['total_profit']/shipping_analysis['total_sales'])*100
                        if shipping_analysis.empty:
                             result="no valid discount data"
                        elif "highest" in question_lower or"best" in question_lower:
                            shipping= shipping_analysis['profit_margin'].idxmax()
                            margin= shipping_analysis['profit_margin'].max()
                            result=(f"shipping cost with highest profit margin:"f"{shipping}.profit margin:{margin:.2f}%")
                        elif "lowest" in question_lower or "least" in question_lower:
                             shipping=shipping_analysis['profit_margin'].idxmin()
                             margin=shipping_analysis['profit_margin'].min()
                             result=(f"shipping cost with lowest profit margin:"f"{shipping}.profit margin{margin:.2f}%")
                        else:
                             result="ask for the highest or lowest profit by margin"
    elif "customer" in question_lower and "segment" not in question_lower and("profit" in question_lower or "sales" in question_lower):
                    customer_data=df.copy()
                    customer_data['Customer_Name']=(customer_data['Customer_Name'].astype("string").str.strip())
                    customer_data=customer_data.dropna(subset=['Customer_Name'])
                    customer_data=customer_data[customer_data['Customer_Name']!=""]
                    customer_analysis=(customer_data.groupby("Customer_Name").agg(total_sales=("Sales","sum"),total_profit=("Profit","sum")))
                    if customer_analysis.empty:
                            result="no valid discount data"
                    elif "highest" in question_lower or"best" in question_lower:
                            if "sales" in question_lower :
                                customer=customer_analysis['total_sales'].idxmax()
                                amount= customer_analysis['total_sales'].max()
                                metric="sales"
                            else:
                                customer=customer_analysis['total_profit'].idxmax()
                                amount= customer_analysis['total_profit'].max()
                                metric="profit"
                            result=(f"customer with highest total{metric}:{customer}."f"total{metric}:{amount:,.2f}")
                    elif "lowest" in question_lower or "least" in question_lower:
                            if "sales" in question_lower :
                                customer=customer_analysis['total_sales'].idxmin()
                                amount=customer_analysis['total_sales'].min()
                                metric="sales"
                            else:
                                customer=customer_analysis['total_profit'].idxmin()
                                amount=customer_analysis['total_profit'].min()
                                metric="profit"
                                
                            result=(f"customer with lowest total{metric}:{customer}."f"total{metric}:{amount:,.2f}")
                    else:
                            result="ask for the highest or lowest profit by margin"
    elif "margin" in question_lower:
            total_sales=df["Sales"].sum()
            total_profit=df['Profit'].sum()
            if total_sales==0:
                result="cannot calculate profit margin because total sales are zero"
            else:
                profit_margin=(total_profit/total_sales)*100
                result=f"overall profit margin:{profit_margin:.2f}%"
    elif "profit" in question_lower and("total" in question_lower or "overall" in question_lower):
        result=f"total profit accross dataset:{df['Profit'].sum():,.2f}"
    elif "month" in question_lower and "sales" in question_lower:
        dates = pd.to_datetime(df["Order_Date"],dayfirst=True, errors="coerce")
        valid_rows = df.loc[dates.notna()].copy()
        valid_rows["Month"] = dates.loc[dates.notna()].dt.to_period("M")
        monthly_sales=valid_rows.groupby("Month")['Sales'].sum()
        if monthly_sales.empty:
            result="no valid order dates available"
        elif "lowest" in question_lower or "least" in question_lower:
            month=monthly_sales.idxmin()
            amount=monthly_sales.min()
            result=f"month with lowest sales:{month}.sales:{amount:,.2f}"
        else:
            month=monthly_sales.idxmax()
            amount=monthly_sales.max()
            result=f"month with highest sales:{month}.sales:{amount:,.2f}"
    if result is None:
            print("\n ai analyst :this question is not supported by current calculation rules:")
            continue
    #send the question and dataset structure to the ai
    print("\n debug result")
    print(result)
    prompt=f""" 
    you are ai salaes analyst.
the user ask:
{question}
verified result from the actual sales dataset:
{result}
explain this result in simple language. 
do not invent the figures,assume a currecny or invent facts
if the comparision data is provided,cmpare the product
using the available sales,profit,quantity and profit margin.
important rules
explain this result in simple language.
1.use only verified result provided.
2.never assume usd,inr or any other currencies
3.do not invent any product specification
4.do not assume why product has higher sales or profit
5.explain only what calculated numbers prove
6.clearly distinguish total profit from profit margin
7.never invent missing figures.
8. Never use currency-specific words such as dollar, rupee, or cents.
9. Never describe a profit margin as healthy, poor, good, or bad without a verified benchmark.
10. Never claim effective or ineffective cost management from these figures alone.
11. Do not add business judgments or unsupported conclusions.
"""
    response=client.chat.completions.create(
          model="openai/gpt-oss-20b",
          messages=[{'role':'user','content':prompt}],
          temperature=0.2
    )
    print("\n ai analyst:",response.choices[0].message.content,"\n")
