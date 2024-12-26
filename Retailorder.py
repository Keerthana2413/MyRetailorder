
import streamlit as st
import pandas as pd
import mysql.connector

# Function to fetch data from the database
def myretail(query):
    # Establish the database connection
    myretail = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database="My_retail_order"
    )
    # Fetch data into a Pandas DataFrame
    df = pd.read_sql(query, myretail)
    # Close the database connection
    myretail.close()
    return df

def main():
    st.title("My Retailorder Analysis")
    group_1_queries={
        "Find top 10 highest revenue generating products?":'''
            select product_id, sum(sale_price*quantity) as Highestrevenue
            from retailorders2
            group by product_id
            order by Highestrevenue DESC
            LIMIT 10;
        ''',
        " Find the top 5 cities with the highest profit margins?":'''
            select r1.city,sum(r2.profit) as Highest_profit_Margin
            from retailorder1 as r1
            left join retailorders2 as r2 on r1.order_id=r2.order_id
            group by r1.city
            order by Highest_profit_Margin DESC
            LIMIT 5;
        ''',
        "Calculate the total discount given for each category?":'''
            select r1.category,sum(r2.discount) as Total_discount
            from retailorder1 as r1
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r1.category;
        ''',
        "Find the average sale price per product category?":'''
            select r2.product_id,r1.category,avg(sale_price) as Avg_sale_price
            from retailorder1 as r1
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r2.product_id,r1.category;
        ''',
        "Find the region with the highest average sale price?":'''
            select r1.region,avg(sale_price) as Highest_avg_saleprice 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r1.region order 
            by Highest_avg_saleprice 
            DESC;
        ''',
        "Find the total profit per category?":'''
            select r1.category,sum(profit) as Total_Profit
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r1.category ;
        ''',
        " Identify the top 3 segments with the highest quantity of orders?":'''
            select r1.segment,sum(quantity) as Highest_quantity_order 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r1.segment 
            order by Highest_quantity_order DESC 
            LIMIT 3;
        ''',
        "Determine the average discount percentage given per region?":'''
            select r1.region ,avg(discount_percent) as Avg_Discount_percent 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r1.region;
        ''',
        "Find the product category with the highest total profit?":'''
            select r2.product_id,r1.category,sum(profit) as Total_profit 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r2.product_id,r1.category 
            order by Total_profit 
            DESC LIMIT 1;

        ''',
        "Calculate the total revenue generated per year?":'''
            select year(order_date) as year,sum(sale_price*quantity) as Total_Revenue
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by year 
            order by year
            ASC;
        ''',
    }
    group_2_queries = {
        "Find the total sale of binders in sub category?":'''
            select sub_category,sum(sale_price) as Total_sale_price
            from retailorders2  
            where sub_category in("binders") 
            group by sub_category;
        ''',
        "Display the cost price above 10000?":'''
            select * from retailorders2
            where cost_price >10000;
        ''',
        "What is the maximum discount given for each category?":'''
            select r1.category,max(discount) as Max_Discount from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r1.category;
        ''',
        "Overall quantity sold for the year?":'''
            select year(order_date) as year,sum(quantity) as overall_quantity 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id
            group by year;
        ''',
        "What is the city wise product sold show in sub_category wise?":'''
            select r1.city,r2.sub_category,count(sub_category) as product 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by r1.city,r2.sub_category 
            order by product 
            DESC;
        ''',
        "Find the total profit of united state?":'''
            select r1.country,sum(profit)as Total_Profit 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id
            where r1.country in("United States");
        ''',
        "Find the maximum value of list price?":'''
            select max(list_price)
            from retailorders2;
        ''',
        "Overall phones  sold in the year 2021?":'''
            select year(order_date) as year,count(sub_category) as phones 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            where r2.sub_category in ("phones")
            group by year;
        ''',
        "Highest shipmode used in the city of fort wort?":'''
            select city,ship_mode,count(ship_mode) as Highest_ship_mode 
            from retailorder1 where city in("fort worth") 
            group by ship_mode order by Highest_ship_mode 
            DESC 
            LIMIT 1;
        ''',
        "Which region has highest discount percent given?":'''
            select r1.region,count(discount_percent) as Highest_discountpercent_count 
            from retailorder1 as r1 
            left join retailorders2 as r2 on r1.order_id=r2.order_id 
            group by region order by Highest_discountpercent_count
            DESC 
            limit 1;
        '''
    }
    tab1, tab2 = st.tabs(["Guvi Questions", "My Questions"])
    with tab1:
        st.subheader("Guvi Questions")
        question_1 = st.selectbox("Select a question from Guvi:", list(group_1_queries.keys()))
        if st.button("Guvi output"):
            query_1 = group_1_queries[question_1]
            data_1 = myretail(query_1)
            st.write(f"Results for: {question_1}")
            st.dataframe(data_1)

    with tab2:
        st.subheader("My Questions")
        question_2 = st.selectbox("Select a question from Mine:", list(group_2_queries.keys()),key="group_2")
        if st.button("My output"):
            query_2 =group_2_queries[question_2]
            data_2 = myretail(query_2)
            st.write(f"Results for: {question_2}")
            st.dataframe(data_2)

if __name__ == "__main__":
    main()
