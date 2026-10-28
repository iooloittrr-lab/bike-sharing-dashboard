import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Analisis Bike Sharing",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .insight-box {
        background-color: #f0f7ff;
        border-radius: 6px;
        padding: 1rem;
        border-left: 4px solid #2563eb;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'main_data.csv')
    if not os.path.exists(file_path):
        file_path = 'dashboard/main_data.csv'
        
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['year_label'] = df['year_label'].astype(str)
    return df

df = load_data()

with st.sidebar:
    st.header("Filter Data")
    st.write("Silakan pilih parameter filter untuk memperbarui tampilan data:")
    
    min_date = df['dteday'].min().date()
    max_date = df['dteday'].max().date()
    
    date_range = st.date_input(
        "Rentang Tanggal:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        start_date = date_range[0]
        end_date = max_date
    else:
        start_date, end_date = min_date, max_date
        
    season_options = ["Semua Musim"] + list(df['season_label'].unique())
    selected_season = st.selectbox(
        "Musim (Season):",
        options=season_options,
        index=0
    )
    
    day_options = ["Semua Tipe Hari"] + list(df['workingday_label'].unique())
    selected_day = st.selectbox(
        "Tipe Hari:",
        options=day_options,
        index=0
    )
    
    weather_options = ["Semua Cuaca"] + list(df['weather_label'].unique())
    selected_weather = st.selectbox(
        "Kondisi Cuaca:",
        options=weather_options,
        index=0
    )
    
    st.markdown("---")
    st.markdown("**Pengembang:**  \nNama: Rama Dwi Nugraha  \nEmail: iooloittrr@gmail.com")

filtered_df = df[
    (df['dteday'].dt.date >= start_date) &
    (df['dteday'].dt.date <= end_date)
]

if selected_season != "Semua Musim":
    filtered_df = filtered_df[filtered_df['season_label'] == selected_season]

if selected_day != "Semua Tipe Hari":
    filtered_df = filtered_df[filtered_df['workingday_label'] == selected_day]

if selected_weather != "Semua Cuaca":
    filtered_df = filtered_df[filtered_df['weather_label'] == selected_weather]

if filtered_df.empty:
    st.warning("Tidak ada data yang cocok dengan kriteria filter yang dipilih. Silakan sesuaikan kembali filter di sidebar.")
    st.stop()

daily_agg = filtered_df.groupby('dteday').agg({
    'cnt': 'sum',
    'casual': 'sum',
    'registered': 'sum',
    'temp_celsius': 'mean',
    'humidity_pct': 'mean',
    'season_label': 'first',
    'weather_label': 'first',
    'workingday_label': 'first',
    'year_label': 'first',
    'month_label': 'first'
}).reset_index()

st.markdown('<div class="main-title">Dashboard Analisis Bike Sharing</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Analisis Tren Penyewaan Sepeda, Pola Jam Harian, Pengaruh Cuaca, dan Segmentasi Pengguna (2011-2012)</div>', unsafe_allow_html=True)

total_rentals = int(filtered_df['cnt'].sum())
total_registered = int(filtered_df['registered'].sum())
total_casual = int(filtered_df['casual'].sum())
pct_reg = (total_registered / total_rentals * 100) if total_rentals > 0 else 0
pct_cas = (total_casual / total_rentals * 100) if total_rentals > 0 else 0
avg_daily = int(daily_agg['cnt'].mean()) if len(daily_agg) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="Total Penyewaan",
        value=f"{total_rentals:,}"
    )
with col2:
    st.metric(
        label="Pengguna Terdaftar (Registered)",
        value=f"{total_registered:,}",
        delta=f"{pct_reg:.1f}% total"
    )
with col3:
    st.metric(
        label="Pengguna Kasual (Casual)",
        value=f"{total_casual:,}",
        delta=f"{pct_cas:.1f}% total"
    )
with col4:
    st.metric(
        label="Rata-rata Harian",
        value=f"{avg_daily:,} unit"
    )

st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Tren Waktu",
    "Pola Jam dan Tipe Hari",
    "Pengaruh Musim dan Cuaca",
    "Analisis Lanjutan (Clustering)",
    "Data Mentah"
])

with tab1:
    st.subheader("Tren Volume Penyewaan Sepeda Harian")
    st.caption("Grafik pergerakan jumlah sewa harian untuk pengguna kasual, terdaftar, dan total.")
    
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(daily_agg['dteday'], daily_agg['cnt'], color='#2563eb', linewidth=1.5, label='Total Sewa (cnt)', alpha=0.9)
    ax.plot(daily_agg['dteday'], daily_agg['registered'], color='#059669', linewidth=1.2, linestyle='--', label='Pengguna Terdaftar', alpha=0.8)
    ax.plot(daily_agg['dteday'], daily_agg['casual'], color='#dc2626', linewidth=1.2, linestyle=':', label='Pengguna Kasual', alpha=0.8)
    
    if len(daily_agg) >= 7:
        daily_agg['rolling_7d'] = daily_agg['cnt'].rolling(window=7).mean()
        ax.plot(daily_agg['dteday'], daily_agg['rolling_7d'], color='#d97706', linewidth=2.2, label='Rata-rata 7 Hari')
        
    ax.set_ylabel("Jumlah Unit Tersewa", fontweight='bold')
    ax.set_xlabel("Tanggal", fontweight='bold')
    ax.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.subheader("Perbandingan Bulanan Tahun 2011 vs 2012")
    monthly_summary = filtered_df.groupby(['year_label', 'month_label'])['cnt'].sum().reset_index()
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_pivot = monthly_summary.pivot(index='month_label', columns='year_label', values='cnt').reindex(month_order).fillna(0)
    monthly_pivot.columns = [str(c) for c in monthly_pivot.columns]
    
    fig2, ax2 = plt.subplots(figsize=(12, 4.8))
    x = np.arange(len(monthly_pivot.index))
    width = 0.38
    
    has_2011 = '2011' in monthly_pivot.columns
    has_2012 = '2012' in monthly_pivot.columns
    
    if has_2011:
        ax2.bar(x - width/2, monthly_pivot['2011'], width, label='Tahun 2011', color='#93c5fd')
    if has_2012:
        ax2.bar(x + width/2, monthly_pivot['2012'], width, label='Tahun 2012', color='#1d4ed8')
        
    ax2.set_xticks(x)
    ax2.set_xticklabels(monthly_pivot.index)
    ax2.set_ylabel("Total Sepeda Tersewa", fontweight='bold')
    
    max_val = monthly_pivot.values.max() if len(monthly_pivot) > 0 and monthly_pivot.values.size > 0 else 0
    if max_val > 0:
        ax2.set_ylim(0, max_val * 1.15)
        
    ax2.legend(frameon=True)
    plt.tight_layout()
    st.pyplot(fig2)
    
    st.markdown("""
    <div class="insight-box">
        <b>Insight:</b>
        <ul>
            <li>Volume penyewaan pada tahun 2012 mengalami peningkatan dibandingkan tahun 2011 di seluruh bulan.</li>
            <li>Puncak penyewaan terjadi pada rentang bulan Mei hingga September, yang bertepatan dengan musim panas dan awal musim gugur.</li>
            <li>Pengguna terdaftar mendominasi sebagian besar transaksi sewa secara stabil sepanjang tahun.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("Rata-rata Penyewaan per Jam: Hari Kerja vs Hari Libur/Akhir Pekan")
    st.caption("Perbandingan pola penyewaan antara aktivitas komuter kerja dengan waktu libur.")
    
    hourly_pivot = filtered_df.pivot_table(index='hr', columns='workingday_label', values='cnt', aggfunc='mean')
    
    fig, ax = plt.subplots(figsize=(14, 5.5))
    if 'Working Day' in hourly_pivot.columns:
        ax.plot(hourly_pivot.index, hourly_pivot['Working Day'], marker='o', linewidth=2.5, color='#2563eb', label='Hari Kerja')
    if 'Holiday / Weekend' in hourly_pivot.columns:
        ax.plot(hourly_pivot.index, hourly_pivot['Holiday / Weekend'], marker='s', linewidth=2.5, linestyle='--', color='#ea580c', label='Hari Libur / Akhir Pekan')
        
    ax.set_xlabel("Jam (00:00 - 23:00)", fontweight='bold')
    ax.set_ylabel("Rata-rata Sepeda Tersewa", fontweight='bold')
    ax.set_xticks(range(0, 24))
    ax.legend(frameon=True, loc='upper left')
    
    if 'Working Day' in hourly_pivot.columns:
        if 8 in hourly_pivot.index:
            ax.annotate('Puncak Pagi (08:00)', xy=(8, hourly_pivot.loc[8, 'Working Day']),
                        xytext=(8, hourly_pivot.loc[8, 'Working Day'] + 70),
                        ha='center', fontweight='bold', color='#2563eb',
                        arrowprops=dict(facecolor='#2563eb', shrink=0.08, width=1.2, headwidth=5))
        if 17 in hourly_pivot.index:
            ax.annotate('Puncak Sore (17:00 - 18:00)', xy=(17, hourly_pivot.loc[17, 'Working Day']),
                        xytext=(17, hourly_pivot.loc[17, 'Working Day'] + 70),
                        ha='center', fontweight='bold', color='#2563eb',
                        arrowprops=dict(facecolor='#2563eb', shrink=0.08, width=1.2, headwidth=5))
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.subheader("Distribusi Rata-rata Rental Berdasarkan Kategori Waktu")
    tod_order = ['Night (00-05)', 'Morning Rush (06-09)', 'Midday (10-15)', 'Evening Rush (16-19)', 'Late Evening (20-23)']
    tod_data = filtered_df.groupby('time_of_day')['cnt'].mean().reindex(tod_order)
    
    fig_tod, ax_tod = plt.subplots(figsize=(10, 4))
    max_tod = tod_data.max()
    colors_tod = ['#1d4ed8' if val == max_tod else '#93c5fd' for val in tod_data.values]
    bars_tod = ax_tod.bar(tod_data.index, tod_data.values, color=colors_tod, width=0.55)
    ax_tod.set_ylabel("Rata-rata Rental per Jam (Unit)", fontweight='bold')
    for bar in bars_tod:
        yval = bar.get_height()
        ax_tod.text(bar.get_x() + bar.get_width()/2.0, yval + 5, f'{yval:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig_tod)
    
    st.markdown("""
    <div class="insight-box">
        <b>Insight:</b>
        <ul>
            <li>Pada hari kerja, lonjakan penyewaan terjadi pada pukul 08:00 (berangkat kerja) dan 17:00-18:00 (pulang kerja).</li>
            <li>Pada hari libur/akhir pekan, pola penggunaan lebih merata dengan puncak aktivitas berada pada siang hari antara pukul 12:00 hingga 16:00.</li>
            <li>Distribusi ini menunjukkan peran penting bike sharing sebagai sarana transportasi komuter pada hari kerja dan rekreasi pada akhir pekan.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.subheader("Pengaruh Musim dan Kondisi Cuaca terhadap Jumlah Sewa")
    
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        st.markdown("**Rata-rata Sewa Harian Berdasarkan Musim**")
        season_perf = daily_agg.groupby('season_label')['cnt'].mean().sort_values(ascending=False)
        fig_s, ax_s = plt.subplots(figsize=(6, 4))
        colors_s = ['#1e40af' if s == season_perf.index[0] else '#93c5fd' for s in season_perf.index]
        bars_s = ax_s.bar(season_perf.index, season_perf.values, color=colors_s, width=0.55)
        ax_s.set_ylabel("Rata-rata Rental Harian", fontweight='bold')
        for bar in bars_s:
            yval = bar.get_height()
            ax_s.text(bar.get_x() + bar.get_width()/2.0, yval + 80, f'{int(yval):,}', ha='center', va='bottom', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig_s)
        
    with col_w2:
        st.markdown("**Rata-rata Sewa Harian Berdasarkan Cuaca**")
        weather_perf = daily_agg.groupby('weather_label')['cnt'].mean().sort_values(ascending=False)
        fig_w, ax_w = plt.subplots(figsize=(6, 4))
        max_weather = weather_perf.max()
        colors_w = ['#1e40af' if val == max_weather else '#93c5fd' for val in weather_perf.values]
        bars_w = ax_w.bar(weather_perf.index, weather_perf.values, color=colors_w, width=0.55)
        ax_w.set_ylabel("Rata-rata Rental Harian", fontweight='bold')
        ax_w.tick_params(axis='x', rotation=15)
        for bar in bars_w:
            yval = bar.get_height()
            ax_w.text(bar.get_x() + bar.get_width()/2.0, yval + 80, f'{int(yval):,}', ha='center', va='bottom', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig_w)
        
    st.markdown("""
    <div class="insight-box">
        <b>Insight:</b>
        <ul>
            <li>Musim gugur (Fall) dan musim panas (Summer) mencatatkan tingkat penyewaan harian tertinggi.</li>
            <li>Musim semi (Spring) memiliki rata-rata penyewaan terendah, yang dipengaruhi oleh temperatur yang masih dingin di awal tahun.</li>
            <li>Kondisi cuaca hujan atau salju menurunkan rata-rata penyewaan secara signifikan dibandingkan cuaca cerah.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.subheader("Analisis Lanjutan: Segmentasi Suhu dan Kelembapan (Clustering/Binning)")
    st.caption("Penerapan manual grouping dan binning pada variabel lingkungan tanpa machine learning.")
    
    col_cl1, col_cl2 = st.columns(2)
    
    with col_cl1:
        st.markdown("**Rata-rata Sewa per Jam Berdasarkan Kategori Suhu**")
        temp_order = ['Cold (<12°C)', 'Mild (12-20°C)', 'Warm (20-28°C)', 'Hot (>28°C)']
        temp_perf = filtered_df.groupby('temp_category')['cnt'].mean().reindex(temp_order).dropna()
        
        fig_t, ax_t = plt.subplots(figsize=(6, 4))
        max_temp = temp_perf.max()
        colors_t = ['#1e40af' if val == max_temp else '#93c5fd' for val in temp_perf.values]
        bars_t = ax_t.bar(temp_perf.index, temp_perf.values, color=colors_t, width=0.55)
        ax_t.set_ylabel("Rata-rata Rental / Jam (Unit)", fontweight='bold')
        for bar in bars_t:
            yval = bar.get_height()
            ax_t.text(bar.get_x() + bar.get_width()/2.0, yval + 5, f'{yval:.1f}', ha='center', va='bottom', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig_t)
        
    with col_cl2:
        st.markdown("**Rata-rata Sewa per Jam Berdasarkan Kategori Kelembapan**")
        hum_order = ['Dry (<40%)', 'Ideal (40-70%)', 'Humid (>70%)']
        hum_perf = filtered_df.groupby('humidity_category')['cnt'].mean().reindex(hum_order).dropna()
        
        fig_h, ax_h = plt.subplots(figsize=(6, 4))
        max_hum = hum_perf.max()
        colors_h = ['#1e40af' if val == max_hum else '#93c5fd' for val in hum_perf.values]
        bars_h = ax_h.bar(hum_perf.index, hum_perf.values, color=colors_h, width=0.55)
        ax_h.set_ylabel("Rata-rata Rental / Jam (Unit)", fontweight='bold')
        for bar in bars_h:
            yval = bar.get_height()
            ax_h.text(bar.get_x() + bar.get_width()/2.0, yval + 5, f'{yval:.1f}', ha='center', va='bottom', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig_h)
        
    st.subheader("Matriks Heatmap Interaksi Suhu dan Kelembapan")
    pivot_heatmap = filtered_df.pivot_table(
        index='temp_category',
        columns='humidity_category',
        values='cnt',
        aggfunc='mean'
    ).round(1)
    
    fig_heat, ax_heat = plt.subplots(figsize=(10, 4.5))
    sns.heatmap(pivot_heatmap, annot=True, fmt='.1f', cmap='YlGnBu', linewidths=0.5, cbar_kws={'label': 'Rata-rata Rental / Jam'}, ax=ax_heat)
    ax_heat.set_ylabel("Kategori Suhu", fontweight='bold')
    ax_heat.set_xlabel("Kategori Kelembapan", fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig_heat)
    
    st.markdown("""
    <div class="insight-box">
        <b>Insight Analisis Lanjutan:</b>
        <ul>
            <li>Pengelompokan suhu memperlihatkan bahwa temperatur Warm (20-28°C) dan Hot (>28°C) menghasilkan rata-rata sewa tertinggi (>230 unit/jam).</li>
            <li>Kelembapan udara kategori Ideal (40-70%) merupakan kondisi paling disukai oleh pesepeda.</li>
            <li>Kombinasi suhu dingin (<12°C) dengan kelembapan tinggi (>70%) menghasilkan angka penggunaan terendah (<100 unit/jam).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab5:
    st.subheader("Data Mentah Hasil Filter")
    st.write(f"Menampilkan {len(filtered_df):,} baris data sesuai filter yang dipilih.")
    
    st.dataframe(filtered_df, use_container_width=True, height=380)
    
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Unduh Data CSV",
        data=csv_data,
        file_name="bike_sharing_filtered.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown(
    "<center><small>Proyek Analisis Data - Belajar Analisis Data dengan Python (Dicoding) | Rama Dwi Nugraha</small></center>",
    unsafe_allow_html=True
)
