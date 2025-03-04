import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set the style of the visualization
sns.set(style='darkgrid')

# Load the data
daily_data = pd.read_csv('./data/day_clean.csv')
hourly_data = pd.read_csv('./data/hour_clean.csv')

# Get the total count of rentals by day
def count_by_daily_data(daily_data):
    daily_rentals = daily_data.query(str('date >= "2011-01-01" and date < "2012-12-31"'))
    return daily_rentals

# Get the total count of rentals by day for registered users
def total_registered_df(daily_data):
   daily_registered_rentals =  daily_data.groupby(by="date").agg({
      "registered": "sum"
    })
   daily_registered_rentals = daily_registered_rentals.reset_index()
   daily_registered_rentals.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return daily_registered_rentals

# Get the total count of rentals by day for casual users
def total_casual_df(daily_data):
   daily_casual_rentals =  daily_data.groupby(by="date").agg({
      "casual": ["sum"]
    })
   daily_casual_rentals = daily_casual_rentals.reset_index()
   daily_casual_rentals.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return daily_casual_rentals

# Sorting the data by date
datetime_columns = ["date"]
daily_data.sort_values(by="date", inplace=True)
daily_data.reset_index(inplace=True)   

hourly_data.sort_values(by="date", inplace=True)
hourly_data.reset_index(inplace=True)

# For each datetime column, convert it to datetime type
for column in datetime_columns:
    daily_data[column] = pd.to_datetime(daily_data[column])
    hourly_data[column] = pd.to_datetime(hourly_data[column])

# Get the min and max date of the data
min_date_daily_data = daily_data["date"].min()
max_date_daily_data = daily_data["date"].max()

min_date_hourly_data = hourly_data["date"].min()
max_date_hourly_data = hourly_data["date"].max()

# Sidebar
with st.sidebar:
    st.image("assets/bike-bg.jpg", width=400)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_daily_data,
        max_value=max_date_daily_data,
        value=[min_date_daily_data, max_date_daily_data])
  
# Filter the data based on the date range
main_df_days = daily_data[(daily_data["date"] >= str(start_date)) & (daily_data["date"] <= str(end_date))]

# Filter the data based on the date range
main_df_hour = hourly_data[(hourly_data["date"] >= str(start_date)) & (hourly_data["date"] <= str(end_date))]

daily_rentals = count_by_daily_data(main_df_days)
daily_registered_rentals = total_registered_df(main_df_days)
daily_casual_rentals = total_casual_df(main_df_days)

#Melengkapi Dashboard dengan Berbagai Visualisasi Dat
st.header('Bike Sharing Analysis 📈')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = daily_rentals.cnt.sum()
    st.metric("Total Sharing Bike", value=format(total_orders, ","))

with col2:
    total_sum = daily_registered_rentals.register_sum.sum()
    st.metric("Total Registered", value=format(total_sum, ","))

with col3:
    total_sum = daily_casual_rentals.casual_sum.sum()
    st.metric("Total Casual", value=format(int(total_sum), ","))
    
st.subheader('Visualisasi Jawaban Pertanyaan Bisnis :')

st.write("1. Pada Musim Apa Tren Penggunaan Sepeda Rental mencapai tingkat tertinggi?")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=daily_data, x='season', y='cnt', ax=ax)
ax.set_title('Tren Penggunaan Sepeda Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig)

st.write("2. Pada Jam Berapa tren penggunaan sepeda rental mencapai nilai tertinggi dalam satu hari?")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=hourly_data, x='hour', y='cnt', ax=ax)
ax.set_title('Tren Penggunaan Sepeda dalam Sehari')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig)

st.write("3. Bagaimana Tren Pengguna Sepeda tiap bulan berdasarkan jenis penyewanya (Registrasi dan Biasa)?")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=daily_data, x='month', y='casual', ax=ax, label='Casual')
sns.lineplot(data=daily_data, x='month', y='registered', ax=ax, label='Registered')
ax.set_title('Tren Pengguna Sepeda tiap Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Rata-rata Jumlah Penyewaan')
st.pyplot(fig)

st.write("4. Seberapa besar pengaruh cuaca terhadap jumlah penyewaan sepeda?")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=hourly_data, x='weather_situation', y='cnt', ax=ax)
ax.set_title('Pengaruh Cuaca terhadap Jumlah Penyewaan')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

st.write("-------------------------------")
st.write("Conclusion:")
st.write("1. Tren Penggunaan Sepeda Rental mencapai tingkat tertinggi padapada musim Gugur, Disusul Musim Panas, Musim Dingin, dan Musim Semi.")
st.write("2. Tren penggunaan sepeda rental menunjukan waktu Sore hari menjadi waktu penyewaan sepeda terpadat terutama pada jam 5 sore, sedangkan pagi hari menjadi waktu penyewaan sepeda tersepi terutama pada jam 4 pagi.")
st.write("3. Tren penggunaan sepeda tiap bulan berdasarkan jenis penyewanya (Registrasi dan Biasa) didominasi oleh user yang sudah teregistrasi di bandingkan user yang belum teregistrasi dan cenderung meningkat")
st.write("4. Pengaruh cuaca terhadap jumlah penyewaan sepeda menunjukan kondisi cuaca yang cerah menjadi faktor utama dalam jumlah penyewaan sepeda, sedangkan kondisi cuaca yang buruk seperti hujan dan salju menjadi faktor terendah dalam jumlah penyewaan sepeda.")