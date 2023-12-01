#import database
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

st.set_page_config(layout='wide')

#read data
customer = pd.read_pickle('data/customer.pkl')
coord = pd.read_csv('data/streacoordinate.csv')

# ROW 1
st.title('General Category of Our Customers')
st.write("""In our business landscape, the General Category of Our Customers 
         represents a rich and diverse tapestry of partnerships that form the 
         backbone of our success. Comprising a wide array of individuals and 
         organizations, this inclusive category underscores the breadth and depth 
         of our reach across various industries, sectors, and demographics. From small 
         enterprises to large corporations, our valued customers share a common thread 
         of trust and satisfaction in our products and services. Their diversity mirrors 
         our commitment to catering to a broad spectrum of needs, ensuring that our offerings 
         resonate with a global audience. With a shared spirit of collaboration, innovation, and 
         mutual growth, the General Category of Our Customers embodies the dynamic synergy that 
         defines our enduring relationships. As we navigate the ever-evolving landscape, we take 
         pride in the varied mosaic of partners who contribute to the vibrant narrative of our 
         business journey.""")
st.divider()


# ROW 2
col1, col2 = st.columns(2)


##Slider col1
input_slider1 = col1.slider(
    label = 'Age Range',
    min_value = customer['age'].min(),
    max_value = customer['age'].max(),
    value = [25,40]
)

min_slider = input_slider1[0]
max_slider = input_slider1[1]

##data pie chart col1
pie_slider = customer[customer['age'].between(left=min_slider, right=max_slider)]
data_pie = pd.crosstab(index=pie_slider['Profession'],
                        columns='Profession_count',
                        colnames=[None])
data_pie = data_pie.reset_index()

###Pie Chart col1
plot_pie = px.pie(data_frame=data_pie, names='Profession', values='Profession_count',
                    labels={'Profession_count' : 'Count'},
                            )
plot_pie.update_traces(textinfo='value')

col1.write(f'### Customers Profession Based on Age {min_slider} to {max_slider}')
col1.plotly_chart(plot_pie, use_container_width=True)


###data customer col2
range_age = pd.crosstab(index = customer['age'],
                        columns = 'count',
                        colnames=[None])

range_age = range_age.reset_index()

####Bar Chart col2
plot_bar = px.bar(range_age.sort_values(by='age', ascending=True),
                        x='age', y='count', text_auto=True,
                        labels={'age':'Age',
                                'number':'Customer Count'})
plot_bar.update_xaxes(tickmode='linear')
plot_bar.update_traces(textposition='outside')

col2.write('### Customer Count Based on Age')
col2.plotly_chart(plot_bar, use_container_width=True)


st.divider()


#ROW 3
col3, col4, col5 = st.columns(3)

##data rata rata income per provinsi col3
annual_income_table = pd.DataFrame({'province' : customer['province'],
                                   'income' : customer['Annual_Income'],
                                   })

annual_income_means = annual_income_table.groupby('province').mean()
annual_income_means['income'] = annual_income_means['income'].astype('float64')
annual_income_map = annual_income_means.merge(coord, on='province')

###Map Chart col3
plot_map = px.scatter_mapbox(data_frame=annual_income_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom = 3,
                             size='income',
                             hover_name='province',
                             hover_data={'latitude':False,
                                         'longitude':False,
                                         'province':False,
                                         'income':True},
                                         labels={'province':'Province ',
                                                 'income':'Average Income '},
                                                 color="income")

col3.write('### Average Annual Income Based on Province')
col3.plotly_chart(plot_map, use_container_width=True)


##select col4
input_select4 = col4.selectbox(
    label='Select Kelahiran',
    options=customer['Kelahiran'].unique().sort_values()
    )

###data line chart col4
customer_gender_select = customer[customer['Kelahiran'] == input_select4] #Fungsi mengubungkan ke opsi select

customer_gender = pd.crosstab(index = customer_gender_select['Profession'], #Fungsi merge 2 variable
                                columns = customer['gender'],
                                colnames=[None])

customer_gender_melt = customer_gender.melt(ignore_index=False, var_name='gender', value_name='num') #Fungsi Melt
customer_gender_melt = customer_gender_melt.reset_index()

####Line Chart col4
plot_line = px.line(data_frame=customer_gender_melt,
                        x='Profession', y='num', color='gender',
                        labels={'num' : 'Customer Count',
                                'gender' : 'Gender'},
                                text='num')
plot_line.update_traces(textposition='top center')

col4.write(f'### Our Customer Count Based on {input_select4}')
col4.plotly_chart(plot_line, use_container_width=True)


##data bar col5
profession_gender = pd.crosstab(index=customer['Profession'],
                                columns=customer['gender'],
                                colnames=[None])

#melt
customer_profession_melt = profession_gender.melt(ignore_index=False, var_name='gender', value_name='num_people_profession')
customer_profession_melt = customer_profession_melt.reset_index()


###Bar Chart col5
plot_bar2 = px.bar(data_frame=customer_profession_melt.sort_values(by='Profession'), 
                   x='Profession',
                   y='num_people_profession',
                   color='gender', 
                   barmode='group',
                   labels={'num_people_profession': 'Customer Count',
                            'gender': 'Gender'},
                    text_auto=True,
                    color_discrete_map={'Female':'#FF0000',
                                        'Male':'#0000FF'})

col5.write('### Detailed Customers Profession Determined by Gender')
col5.plotly_chart(plot_bar2, use_container_width=True)