import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

#########

# Load Data
all_df = pd.read_csv('all_data1.csv')

##############

# Memastikan kolom datetime
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
all_df['order_delivered_customer_date'] = pd.to_datetime(all_df['order_delivered_customer_date'])
all_df['order_estimated_delivery_date'] = pd.to_datetime(all_df['order_estimated_delivery_date'])

# Setup halaman Streamlit
st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo3.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = all_df[
    (all_df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (all_df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
]

st.title("Dashboard Penjualan")

# **1. Jumlah Pesanan per Bulan**
st.subheader("Jumlah Pesanan per Bulan")
all_df['order_month'] = all_df['order_purchase_timestamp'].dt.to_period("M")
monthly_orders = all_df['order_month'].value_counts().sort_index()

fig1, ax1 = plt.subplots(figsize=(10, 6))
monthly_orders.plot(kind='line', marker='o', color='skyblue', ax=ax1)
ax1.set_xlabel('Bulan')
ax1.set_ylabel('Jumlah Pesanan')
ax1.set_title('Jumlah Pesanan per Bulan')
plt.xticks(rotation=45)
st.pyplot(fig1)

st.markdown('''
    :gray[Penjelasan] :blue-background[Dari grafik diatas menunjkan pada bulan januari 2017 sampai akhir bulan oktober 2017 terjadi lonjakan pesanan yang signifikan, masuk pada bulan januari s/d juli pesanan secara grafik terlihat normal namun pada akhir bulan juli terjadi penurunan secara signifikan. 
miliki pola tertentu.]
''')

# **2. Distribusi Status Pesanan**
st.subheader("Distribusi Status Pesanan")
order_status_counts = all_df['order_status'].value_counts()

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=order_status_counts.index, hue=order_status_counts.index, y=order_status_counts.values, palette="Blues", ax=ax2)
ax2.set_xlabel('Status Pesanan')
ax2.set_ylabel('Jumlah Pesanan')
ax2.set_title('Distribusi Status Pesanan')
st.pyplot(fig2)
st.markdown('''
    :gray[Penjelasan] :blue-background[Grafik ini menunjukkan setiap status pesanan di sepanjang sumbu x dan jumlah pesanan untuk setiap status pada sumbu y dimana semua pesanan terdeliver dan tidak ada pesanan yang dicancele dll]
''')

# **3. Durasi Pengiriman: Waktu Aktual vs Estimasi**
st.subheader("Durasi Pengiriman: Waktu Pengiriman Aktual vs Estimasi")
all_df['actual_delivery_duration'] = (all_df['order_delivered_customer_date'] - all_df['order_purchase_timestamp']).dt.days
all_df['estimated_delivery_duration'] = (all_df['order_estimated_delivery_date'] - all_df['order_purchase_timestamp']).dt.days

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.histplot(all_df['actual_delivery_duration'], color="skyblue", label="Durasi Pengiriman Aktual", kde=True, ax=ax3)
sns.histplot(all_df['estimated_delivery_duration'], color="salmon", label="Durasi Pengiriman Estimasi", kde=True, ax=ax3)
ax3.set_xlabel('Durasi Pengiriman (hari)')
ax3.set_ylabel('Frekuensi')
ax3.set_title('Distribusi Durasi Pengiriman (Aktual vs Estimasi)')
ax3.legend()
st.pyplot(fig3)
st.markdown('''
    :gray[Penjelasan] :blue-background[-]
''')

# **4. Rata-rata Waktu Pengiriman Berdasarkan Bulan**
st.subheader("Rata-rata Waktu Pengiriman Berdasarkan Bulan")
all_df['delivery_month'] = all_df['order_delivered_customer_date'].dt.to_period("M")
avg_delivery_time_per_month = all_df.groupby('delivery_month')['actual_delivery_duration'].mean()

fig4, ax4 = plt.subplots(figsize=(12, 6))
avg_delivery_time_per_month.plot(kind='line', marker='o', color='green', ax=ax4)
ax4.set_xlabel('Bulan')
ax4.set_ylabel('Rata-rata Durasi Pengiriman (hari)')
ax4.set_title('Rata-rata Waktu Pengiriman Berdasarkan Bulan')
plt.xticks(rotation=45)
st.pyplot(fig4)
st.markdown('''
    :gray[Penjelasan] :blue-background[Dari grafik diatas menunjkan rata-rata waktu pengiriman tiap bulanya, pada awal bulan januari menunjukan peningkatan secara signifikan namun begitu masuk pada bulan berikutnya sampai pada bulan juli 2018 terjadi penurunan.]
''')

# **5. Jumlah Pesanan per Hari dalam Seminggu**
st.subheader("Jumlah Pesanan per Hari dalam Seminggu")
all_df['order_dayofweek'] = all_df['order_purchase_timestamp'].dt.day_name()
orders_by_day = all_df['order_dayofweek'].value_counts().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.barplot(x=orders_by_day.index, hue=orders_by_day.index, y=orders_by_day.values, palette="Blues", ax=ax5)
ax5.set_xlabel('Hari dalam Minggu')
ax5.set_ylabel('Jumlah Pesanan')
ax5.set_title('Jumlah Pesanan per Hari dalam Seminggu')
st.pyplot(fig5)
st.markdown('''
    :gray[Penjelasan] :blue-background[Dari grafik dipaparkan jumlah pesanan per Hari dalam seminggu, pada hari senin dan selasa mengalami kepadatan pesanan namun begitu hari rabu sampai hari minggu terjadi penurunan.]
''')

# **6. Ringkasan Statistik Pesanan**
st.subheader("Ringkasan Statistik Pesanan")
total_sales = all_df['order_id'].nunique()
total_customers = all_df['customer_id'].nunique() if 'customer_id' in all_df else "Data Tidak Tersedia"
avg_delivery_time = all_df['actual_delivery_duration'].mean()

# **7. Distribusi Statistik Pesanan**
st.subheader("Distribusi Metode Pembayaran")
payment_method_count = all_df['payment_type'].value_counts()
fig, ax = plt.subplots(figsize=(10, 8))
ax.pie(payment_method_count, labels=payment_method_count.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
ax.set_title('Metode Pembayaran Terpopuler')
st.pyplot(fig)
st.markdown('''
    :gray[Penjelasan] :blue-background[Dari pie diatas menunjkan persentase metode pembayaran terbesar pada angka 73.7%, menggunakan voucher 5.4%, debit_card 1.4%, beleto 19.5% dan not_defined / metode pembayaran tidak terdefinisi 0.0%.]
''')

st.write(f"**Total Pesanan:** {total_sales}")
st.write(f"**Total Pelanggan:** {total_customers}")
st.write(f"**Rata-rata Waktu Pengiriman:** {avg_delivery_time:.2f} hari")

name = '''
EEEEEEE                                                                          
EE               cccc  oooo  mm mm mmmm  mm mm mmmm    eee  rr rr    cccc   eee  
EEEEE   _____  cc     oo  oo mmm  mm  mm mmm  mm  mm ee   e rrr  r cc     ee   e 
EE             cc     oo  oo mmm  mm  mm mmm  mm  mm eeeee  rr     cc     eeeee  
EEEEEEE         ccccc  oooo  mmm  mm  mm mmm  mm  mm  eeeee rr      ccccc  eeeee
by: Anwar Muhammad
'''
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.code(name, language='python')
st.markdown("</div>", unsafe_allow_html=True)
st.link_button("github-repo", "https://github.com/0nhoel1/e-commerce")
