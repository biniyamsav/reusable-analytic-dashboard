import streamlit as st 
import pandas as pd
import database as db 
import plotly.express as px
#THIS IS THE UPLOAD PAGE
def load_page():
    if "data" not in st.session_state:
        st.session_state.data = None

    st.markdown("# ⬆️ Upload New Dataset")
    st.markdown("##### Add a new sales dataset to your analytics dashboard")
    st.markdown("---")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.session_state.data = st.file_uploader("📂 Drop your CSV file here", type=["csv"])

        if st.session_state.data is not None:
            st.success(f"✅ **{st.session_state.data.name}** ready to upload!")
            st.session_state.data = pd.read_csv(st.session_state.data)
            return st.session_state.data, True

    st.markdown("---")
    st.markdown("### 📋 Before You Upload")
    st.markdown("Make sure your file has these exact column names:")

    col1, col2 = st.columns(2)
    with col1:
        st.code("order_id\norder_date\ncustomer_id\ncustomer_name\nproduct_name\ncategory")
    with col2:
        st.code("region\nquantity\nunit_price\ndiscount\nsales_amount")

    st.markdown("---")
    if st.button("⬅️ Back", use_container_width=True):
        st.session_state.page = 0
        st.rerun()

    return st.session_state.data, False

def just_load(name=None):
    if "name" not in st.session_state:
        st.session_state.name = name
        st.session_state.next_page=False
    if st.session_state.name is None:
        st.session_state.name,st.session_state.next_page=load_page()
        return st.session_state.name,st.session_state.next_page 
    elif st.session_state.name is not None:
        return st.session_state.name ,True

#THIS FUNCTION IS THE REVENUE PAGE
def revenue_analysis_page(name):
    if "name" not in st.session_state:
        st.session_state.total = None
        st.session_state.name = name
        st.session_state.rev_region = None
        st.session_state.rev_category = None
        st.session_state.rev_product = None
        st.session_state.back = False
        st.session_state.next = False
        st.session_state.rev_time =False
        
        

    st.markdown("## 📊 Revenue Analysis")
    st.markdown("---")

    # total revenue metric
    st.session_state.pass_data = db.total_revenue(st.session_state.name)
    total = st.session_state.pass_data.iloc[0][0]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("💰 Total Revenue", f"${total:,.2f}")
    with c2:
        st.session_state.rev_region = db.revenue_by_region(st.session_state.name)
        top_region = st.session_state.rev_region.iloc[0][0]
        st.metric("🌍 Top Region", top_region)
    with c3:
        st.session_state.rev_category = db.revenue_by_category(st.session_state.name)
        top_category = st.session_state.rev_category.iloc[0][0]
        st.metric("🏆 Top Category", top_category)

    st.markdown("---")

    # region and category side by side
    left, right = st.columns(2)
    with left:
        fig = px.bar(st.session_state.rev_region, x=0, y=1,
                     title="Revenue by Region",
                     color=0,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(xaxis_title="Region", yaxis_title="Total Sales",
                          height=350, showlegend=False,)
        st.plotly_chart(fig)

    with right:
        fig = px.pie(st.session_state.rev_category, names=0, values=1,
                     title="Revenue by Category",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(height=350)
        st.plotly_chart(fig)

    st.markdown("---")

    # product horizontal bar
    st.session_state.rev_product = db.revenue_by_product(st.session_state.name)
    fig = px.bar(st.session_state.rev_product, x=1, y=0,
                 title="Revenue by Product",
                 orientation='h',
                 color=1)
    fig.update_layout(xaxis_title="Total Sales", yaxis_title="",
                      height=500, showlegend=False,
                      yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig)
    st.session_state.rev_time = db.revenue_over_time(st.session_state.name)
    st.session_state.rev_time['Date'] = st.session_state.rev_time[0].astype(str) + '-' + st.session_state.rev_time[1].astype(str)
    st.session_state.rev_time['Date'] = pd.to_datetime(st.session_state.rev_time['Date'])
    fig = px.line(st.session_state.rev_time, x='Date', y=2,
                title="Revenue Over Time",
                markers=True)
    fig.update_traces(line=dict(color='#00C9A7', width=2.5),
                    marker=dict(size=6, color='white', line=dict(color='#00C9A7', width=2)))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Sales ($)",
        height=450,
        showlegend=False,
        hovermode='x unified'
    )
    st.plotly_chart(fig, width='stretch')
        
   
    a1, a2 = st.columns([1, 1])
    with a1:
        if st.button("⬅️ Back", width='stretch'):
            st.session_state.page = 0
            st.rerun()
    with a2:
        if st.button("Next ➡️", width='stretch', type="primary"):
            st.session_state.page = 3
            st.rerun()
            
def order_analysis_page(name):
    if "name" not in st.session_state:
        st.session_state.name = name
        st.session_state.tot_order = None
        st.session_state.avg_ord = None
        st.session_state.ord_ovr_time = None
        st.session_state.top_prdct = None
        st.session_state.worst_prdct = None

    st.markdown("## 📦 Order Analysis")
    st.markdown("---")

    # metrics
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.tot_order = db.total_number_of_orders(st.session_state.name)
        st.metric("🧾 Total Orders", f"{st.session_state.tot_order.iloc[0][0]:,}")
    with c2:
        st.session_state.avg_ord = db.average_order_value(st.session_state.name)
        st.metric("💵 Average Order Value", f"${st.session_state.avg_ord.iloc[0][0]:,.2f}")

    st.markdown("---")

    # orders over time
    st.session_state.ord_ovr_time = db.orders_over_time(st.session_state.name)
    st.session_state.ord_ovr_time['Date'] = st.session_state.ord_ovr_time[0].astype(str) + '-' + st.session_state.ord_ovr_time[1].astype(str)
    st.session_state.ord_ovr_time['Date'] = pd.to_datetime(st.session_state.ord_ovr_time['Date'])
    fig = px.line(st.session_state.ord_ovr_time, x='Date', y=2,
                  title="Orders Over Time", markers=True)
    fig.update_traces(line=dict(color='#4A90D9', width=2.5),
                      marker=dict(size=6, color='white', line=dict(color='#4A90D9', width=2)))
    fig.update_layout(xaxis_title="Month", yaxis_title="Total Orders",
                      height=400, showlegend=False, hovermode='x unified')
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")

 
  
    st.session_state.top_prdct = db.top_products_by_revenue(st.session_state.name)
    fig = px.bar(st.session_state.top_prdct, x=1, y=0,
                    title="🏆 Top 10 Products",
                    orientation='h', color=1,
                    color_continuous_scale='teal')
    fig.update_layout(xaxis_title="Total Sales", yaxis_title="",
                        showlegend=False, height=400,
                        yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig, width='stretch')


    st.session_state.worst_prdct = db.worst_performing_products(st.session_state.name)
    fig = px.bar(st.session_state.worst_prdct, x=1, y=0,
                    title="⚠️ Worst 5 Products",
                    orientation='h', color=1,
                    color_continuous_scale='reds')
    fig.update_layout(xaxis_title="Total Sales", yaxis_title="",
                        showlegend=False, height=400,
                        yaxis=dict(categoryorder='total descending'))
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")

    a1, a2 = st.columns([1, 1])
    with a1:
        if st.button("⬅️ Back", width='stretch'):
            st.session_state.page = 2
            st.rerun()
    with a2:
        if st.button("Next ➡️", width='stretch', type="primary"):
            st.session_state.page = 4
            st.rerun()

def customer_analysis_page(name):
    if "name" not in st.session_state:
        st.session_state.name = name
        st.session_state.avg_spend=None 
        st.session_state.dis_impact=None 
        

    st.markdown("## 👥 Customer Analysis")
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.session_state.avg_spend = db.average_spend_per_customer(st.session_state.name)
        st.metric("💳 Average Spend Per Customer", f"${st.session_state.avg_spend.iloc[0][0]:,.2f}")

    st.markdown("---")

    top_customers = db.top_customers_by_revenue(st.session_state.name)
    fig = px.bar(top_customers, x=1, y=0, title="🏆 Top 10 Customers by Revenue",
                 orientation='h', color=1)
    fig.update_layout(xaxis_title="Total Revenue", yaxis_title="",
                      showlegend=False, height=400,
                      yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")

    avg_discount = db.average_discount_by_category(st.session_state.name)
    fig = px.bar(avg_discount, x=0, y=1, title="🏷️ Average Discount by Category",
                 color=0, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(xaxis_title="Category", yaxis_title="Avg Discount",
                      showlegend=False, height=400)
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    st.session_state.dis_impact = db.discount_impact(st.session_state.name)

    w1, w2 = st.columns(2)
    with w1:
        fig = px.bar(st.session_state.dis_impact, x=0, y=1,
                    title="💰 Discount vs Avg Sales Amount",
                    color=1, color_continuous_scale='teal')
        fig.update_layout(xaxis_title="Discount", yaxis_title="Avg Sales Amount",
                        showlegend=False, height=400)
        st.plotly_chart(fig, width='stretch')

    with w2:
        fig = px.bar(st.session_state.dis_impact, x=0, y=2,
                    title="📦 Discount vs Number of Orders",
                    color=1, color_continuous_scale='blues')
        fig.update_layout(xaxis_title="Discount", yaxis_title="Number of Orders",
                        showlegend=False, height=400)
        st.plotly_chart(fig, width='stretch')

    st.markdown("---")

    a1, a2 = st.columns([1, 1])
    with a1:
        if st.button("⬅️ Back", width='stretch'):
            st.session_state.page = 3
            st.rerun()
    with a2:
        if st.button("Main ➡️", width='stretch', type="primary"):
            st.session_state.page = 0
            st.rerun()
def main_page():
    if "names" not in st.session_state:
        st.session_state.names = None
        st.session_state.upload = False
    if 'i' not in st.session_state:
        st.session_state.i = 0
        st.session_state.button = {}

    st.session_state.names = db.tables_in_database()
    st.session_state.names = st.session_state.names[0]

    st.markdown("# 📊 Sales Analytics Dashboard")
    st.markdown("##### Turn your raw sales data into actionable insights")
    st.markdown("---")

    # how it works section
    st.markdown("### 🔍 How It Works")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("**1. Upload**\n\nUpload your CSV sales file")
    with c2:
        st.info("**2. Store**\n\nData is saved to your database")
    with c3:
        st.info("**3. Analyze**\n\nExplore revenue, orders, and customers")
    with c4:
        st.info("**4. Decide**\n\nMake data-driven decisions")

    st.markdown("---")

    # column requirements
    with st.expander("📋 Required Column Names — click to expand"):
        st.markdown("""
        Your CSV file **must** contain these exact column names:
        
        | Column | Type | Description |
        |--------|------|-------------|
        | `order_id` | Integer | Unique order identifier |
        | `order_date` | Date | Date of the order (YYYY-MM-DD) |
        | `customer_id` | Integer | Unique customer identifier |
        | `customer_name` | Text | Full name of the customer |
        | `product_name` | Text | Name of the product |
        | `category` | Text | Product category |
        | `region` | Text | Sales region |
        | `quantity` | Integer | Number of units ordered |
        | `unit_price` | Decimal | Price per unit |
        | `discount` | Decimal | Discount applied (0.0 to 1.0) |
        | `sales_amount` | Decimal | Total sales value |
        
        ⚠️ Column names are case-sensitive. Make sure they match exactly.
        """)

    st.markdown("---")

    # tables section
    st.markdown("### 🗄️ Your Datasets")

    if len(st.session_state.names) == 0:
        st.warning("⚠️ No datasets found in your database. Upload a CSV file to get started.")
    else:
        st.markdown(f"You have **{len(st.session_state.names)}** dataset(s) available. Click one to analyze it.")
        st.markdown("")
        for name in st.session_state.names:
            st.session_state.button[name] = st.button(f"📂 {name}", key=f"btn_{name}", width='stretch')
            if st.session_state.button[name]:
                st.session_state.name = name  # add this line
                just_load(name)
                st.session_state.page = 2
                st.rerun()

    st.markdown("---")
    st.button("⬆️ Upload New Dataset", width='stretch', type="primary",
              on_click=lambda: st.session_state.update({"page": 1}))
        
            
      
        
        
        
        
    # table[st.session_state.names[st.session_state.i]]=st.button(st.session_state.names[st.session_state.i], key=f"btn_{st.session_state.i}")
    # if st.session_state.i<len(st.session_state.names):
    #     st.session_state.i+=1
    #     st.rerun()
    
    
    
            
            
        

    


















def main():
    if "name" not in st.session_state:
        st.session_state.name=None
        st.session_state.page=0
    if st.session_state.page==0:
        main_page()
    if st.session_state.page==1:
        st.session_state.data,next_stage=load_page()
        if next_stage:
            st.session_state.name=db.load_data(st.session_state.data)
            st.session_state.page=2
            st.rerun()
    elif st.session_state.page==2:
        revenue_analysis_page(st.session_state.name)
    elif st.session_state.page==3:
        order_analysis_page(st.session_state.name)
    elif st.session_state.page==4:
        customer_analysis_page(st.session_state.name)
    
    















if __name__ == "__main__":
    main()



# source .venv/bin/activate