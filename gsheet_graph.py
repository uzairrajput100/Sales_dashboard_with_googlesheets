import streamlit as st
from streamlit_gsheets import GSheetsConnection
import numpy as np
import datetime
import pandas as pd
import datetime
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go

# Define the Google Sheets URL
url = "https://docs.google.com/spreadsheets/d/12_CL4PLsLPbL2E4fhI40K1sndrvkmDkF2EY_-9gsKJQ/edit?usp=sharing"

# Establish the connection to Google Sheets
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Read the data from Google Sheets
df = conn.read(spreadsheet=url)

st.dataframe(df)

# Setting up the page and title
html_title1 = """
<style>.title-test {
    font-weight: bold;
    padding: 5px;
    border-radius: 6px;
}
</style>
<center><h1 class="title-test">1</h1></center>"""

html_title = """
<style>.title-test {
    font-weight: bold;
    padding: 5px;
    border-radius: 6px;
}
</style>
<center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center>"""

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.markdown(html_title1, unsafe_allow_html=True)
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1,0.45,0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n{box_date}")

# Plot Total Sales by Retailer
with col4:
    fig = px.bar(df, x="Retailer", y="Total Sales", labels={"Total Sales" : "Total Sales {$}"},
                 title="Total Sales by Retailer", hover_data=["Total Sales"],
                 height=500, template="gridon")
    st.plotly_chart(fig, use_container_width=True)

# Retailer wise Sales
_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer", "Total Sales"]].groupby(by="Retailer")["Total Sales"].sum()
    expander.write(data)
with dwn1:
    st.download_button('Get data', data=data.to_csv().encode('utf-8'),
                       file_name="Retailer Sales.csv", mime="text/csv")

# Monthly Sales
df['Month_year'] = pd.to_datetime(df['Invoice Date']).dt.strftime("%b '%y")
result = df.groupby(by="Month_year")["Total Sales"].sum().reset_index()
with col5:
    fig1 = px.line(result, x="Month_year", y="Total Sales", title="Total sales over time",
                   template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)
with dwn2:
    st.download_button('Get data', data=result.to_csv().encode('utf-8'),
                       file_name="Monthly Sales.csv", mime="text/csv")
st.divider()

# Total Sales and Units Sold by State
result1 = df.groupby(by="State")[["Total Sales", "Units Sold"]].sum().reset_index()
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1['State'], y=result1['Total Sales'], name='Total Sales'))
fig3.add_trace(go.Scatter(x=result1['State'], y=result1['Units Sold'], mode="lines",
                          name="Units Sold", yaxis="y2"))
fig3.update_layout(title="Total Sales and Units Sold by State",
                   xaxis=dict(title="State"),
                   yaxis=dict(title="Total Sales", showgrid=True),
                   yaxis2=dict(title="Units Sold", overlaying='y', side='right'),
                   template="gridon", legend=dict(x=1, y=1))
_, col6 = st.columns([0.1, 0.9])
with col6:
    st.plotly_chart(fig3, use_container_width=True)

_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button('Get data', data=result1.to_csv().encode('utf-8'),
                       file_name="Sales by units sold.csv", mime="text/csv")
st.divider()

# Total Sales by Region and City in Treemap
_, col7 = st.columns([0.1, 0.9])
treemap = df[['Region', 'City', 'Total Sales']].groupby(by=['Region', 'City'])['Total Sales'].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)
treemap['Total Sales (Formatted)'] = treemap['Total Sales'].apply(format_sales)

fig4 = px.treemap(treemap, path=['Region', 'City'], values="Total Sales", hover_name='Total Sales (Formatted)',
                  hover_data=["Total Sales (Formatted)"], color='City', height=700, width=600)
fig4.update_traces(textinfo='label+value')

with col7:
    st.subheader(':point_right: Total Sales by Region and City in Treemap')
    st.plotly_chart(fig4, use_container_width=True)

_, view4, dwn4 = st.columns([0.5, 0.45, 0.45])
with view4:
    result2 = df[['Region', 'City', 'Total Sales']].groupby(by=['Region', 'City'])['Total Sales'].sum()
    expander = st.expander("View Data for Total Sales by Region and City")
    expander.write(result2)
with dwn4:
    st.download_button('Get data', data=result2.to_csv().encode('utf-8'),
                       file_name="Sales by Region.csv", mime="text/csv")

# View Sales Raw Data
_, view5, dwn5 = st.columns([0.5, 0.45, 0.45])
with view5:
    expander = st.expander("View Sales Raw Data")
    expander.write(df)
with dwn5:
    st.download_button('Get Raw data', data=df.to_csv().encode('utf-8'),
                       file_name="Sales Raw Data.csv", mime="text/csv")

# Footer
st.markdown(""" 
---
**Contact Us:** For any sales queries or support, feel free to reach out at +92 333 6611988 or email uzairrajput100@gmail.com
""")

st.divider()
