import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title and header
st.title("Proyek Analisis Data: E-Commerce Public Dataset")
st.markdown("**Nama:** Suci Ihtisabi Hida Nursyifa")
st.markdown("**Email:** sucinursyifa064@gmail.com")
st.markdown("**ID Dicoding:** mc222d5x1275")

st.markdown("---")

# Load data
main_data = pd.read_csv("main_data.csv")

# Proses data
main_data['total_spent'] = main_data['price'] + main_data['freight_value']

# Create city to state/region mapping
city_state_mapping = main_data[['customer_city', 'customer_state']].drop_duplicates()

# Mapping region
region_colors = {
    "North": "#FF5733",
    "Northeast": "#33FF57",
    "Center-West": "#3357FF",
    "Southeast": "#FF33A8",
    "South": "#FFC300"
}

state_to_region = {
    "Acre": "North", "Amapá": "North", "Amazonas": "North", "Pará": "North", "Rondônia": "North", "Roraima": "North", "Tocantins": "North",
    "Alagoas": "Northeast", "Bahia": "Northeast", "Ceará": "Northeast", "Maranhão": "Northeast", "Paraíba": "Northeast", "Pernambuco": "Northeast", "Piauí": "Northeast", "Rio Grande do Norte": "Northeast", "Sergipe": "Northeast",
    "Distrito Federal": "Center-West", "Goiás": "Center-West", "Mato Grosso": "Center-West", "Mato Grosso do Sul": "Center-West",
    "Espírito Santo": "Southeast", "Minas Gerais": "Southeast", "Rio de Janeiro": "Southeast", "São Paulo": "Southeast",
    "Paraná": "South", "Rio Grande do Sul": "South", "Santa Catarina": "South"
}

# State abbreviation to full name mapping
state_name_mapping = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia", 
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás", 
    "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais", 
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí", 
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul", 
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo", 
    "SE": "Sergipe", "TO": "Tocantins"
}

# Create reverse mapping from state abbreviation to region
state_abbr_to_region = {abbr: state_to_region.get(full_name, "Unknown") 
                        for abbr, full_name in state_name_mapping.items()}

# Add region to main data
main_data['region'] = main_data['customer_state'].map(state_abbr_to_region)

# Create city to region mapping
city_region_mapping = {}
for _, row in city_state_mapping.iterrows():
    city = row['customer_city']
    state_abbr = row['customer_state']
    region = state_abbr_to_region.get(state_abbr, "Unknown")
    city_region_mapping[city] = region

# Create sidebar for filters
st.sidebar.header("Filter Region")

# Add checkboxes for each region in the sidebar
selected_regions = []
all_regions = list(region_colors.keys())
region_selections = {}

for region in all_regions:
    region_selections[region] = st.sidebar.checkbox(region, value=True)
    if region_selections[region]:
        selected_regions.append(region)

# Filter data based on selected regions
filtered_data = main_data[main_data['region'].isin(selected_regions)]

# Create tabs for different analyses
tab1, tab2, tab3 = st.tabs(["Analisis Transaksi", "Peta Potensial Market", "Pola Waktu Pembelian"])

with tab1:
    # Create aggregations for visualizations
    state_transaction = filtered_data.groupby('customer_state')['order_id'].nunique().reset_index()
    state_transaction.columns = ['State', 'Jumlah Transaksi']
    state_transaction = state_transaction.sort_values('Jumlah Transaksi', ascending=False)

    state_total_spent = filtered_data.groupby('customer_state')['total_spent'].sum().reset_index()
    state_total_spent.columns = ['State', 'Total Pengeluaran']
    state_total_spent = state_total_spent.sort_values('Total Pengeluaran', ascending=False)

    city_transaction = filtered_data.groupby('customer_city')['order_id'].nunique().reset_index()
    city_transaction.columns = ['City', 'Jumlah Transaksi']
    city_transaction = city_transaction.sort_values('Jumlah Transaksi', ascending=False)

    city_total_spent = filtered_data.groupby('customer_city')['total_spent'].sum().reset_index()
    city_total_spent.columns = ['City', 'Total Pengeluaran']
    city_total_spent = city_total_spent.sort_values('Total Pengeluaran', ascending=False)

    # Create visualizations section
    st.header("Analisis Transaksi dan Pengeluaran")

    # Create two columns for the visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Jumlah Transaksi per State (Top 5)")
        # 1. Top States berdasarkan jumlah transaksi
        # Mengurutkan data berdasarkan jumlah transaksi (dari besar ke kecil)
        sorted_state = state_transaction.sort_values('Jumlah Transaksi', ascending=False).reset_index(drop=True)
        
        if len(sorted_state) > 0:
            # Membuat data untuk top 5 dan sisanya digabung sebagai "Others"
            top_5 = sorted_state.iloc[:min(5, len(sorted_state))].copy()
            
            if len(sorted_state) > 5:
                others = pd.DataFrame({
                    'State': ['Others'],
                    'Jumlah Transaksi': [sorted_state.iloc[5:]['Jumlah Transaksi'].sum()]
                })
                # Menggabungkan top 5 dengan others
                plot_data = pd.concat([top_5, others]).reset_index(drop=True)
            else:
                plot_data = top_5
                
            # Create pie chart
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            explode = [0.05] * len(plot_data)  # Nilai yang sama untuk semua bagian
            ax1.pie(plot_data['Jumlah Transaksi'], 
                    labels=plot_data['State'],
                    autopct='%1.1f%%',
                    startangle=50,
                    explode=explode)
            ax1.axis('equal')  # Agar pie chartnya berbentuk lingkaran
            plt.legend(plot_data['State'], loc='best')
            st.pyplot(fig1)
        else:
            st.write("No data available for the selected regions")

    with col2:
        st.subheader("Distribusi Total Pengeluaran per State (Top 5)")
        # Top States berdasarkan Total Pengeluaran
        sorted_state = state_total_spent.sort_values('Total Pengeluaran', ascending=False).reset_index(drop=True)
        
        if len(sorted_state) > 0:
            # Membuat data untuk top 5 dan sisanya digabung sebagai "Others"
            top_5 = sorted_state.iloc[:min(5, len(sorted_state))].copy()
            
            if len(sorted_state) > 5:
                others = pd.DataFrame({
                    'State': ['Others'],
                    'Total Pengeluaran': [sorted_state.iloc[5:]['Total Pengeluaran'].sum()]
                })
                # Menggabungkan top 5 dengan others
                plot_data = pd.concat([top_5, others]).reset_index(drop=True)
            else:
                plot_data = top_5
                
            # Create pie chart
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            explode = [0.05] * len(plot_data)  # Nilai yang sama untuk semua bagian
            ax2.pie(plot_data['Total Pengeluaran'], 
                    labels=plot_data['State'],
                    autopct='%1.1f%%',
                    startangle=50,
                    explode=explode)
            ax2.axis('equal')  # Agar pie chartnya berbentuk lingkaran
            plt.legend(plot_data['State'], loc='best')
            st.pyplot(fig2)
        else:
            st.write("No data available for the selected regions")

    # Create two columns for bar charts
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("10 Kota Teratas Berdasarkan Jumlah Transaksi")
        if len(city_transaction) > 0:
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            data_to_plot = city_transaction.head(10)
            sns.barplot(x='City', y='Jumlah Transaksi', data=data_to_plot, ax=ax3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig3)
        else:
            st.write("No data available for the selected regions")

    with col4:
        st.subheader("10 Kota Teratas Berdasarkan Total Pengeluaran")
        if len(city_total_spent) > 0:
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            data_to_plot = city_total_spent.head(10)
            sns.barplot(x='City', y='Total Pengeluaran', data=data_to_plot, ax=ax4)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig4)
        else:
            st.write("No data available for the selected regions")

with tab2:
    # Compute city potential data on FULL dataset (before filtering regions)
    city_potential_full = main_data.groupby('customer_city').agg({
        'order_id': 'nunique',
        'total_spent': 'sum'
    }).reset_index()

    city_coords_full = main_data.groupby('customer_city')[['geolocation_lat', 'geolocation_lng']].mean().reset_index()
    city_potential_full = city_potential_full.merge(city_coords_full, on='customer_city')
    city_potential_full['Rata-rata Pengeluaran per Transaksi'] = city_potential_full['total_spent'] / city_potential_full['order_id']
    city_potential_full = city_potential_full.rename(columns={'order_id': 'Jumlah Transaksi', 'total_spent': 'Total Pengeluaran'})

    # Add region to city_potential_full
    city_potential_full['Region'] = city_potential_full['customer_city'].map(city_region_mapping)

    # Calculate thresholds on the FULL dataset
    low_transaction_threshold = city_potential_full['Jumlah Transaksi'].quantile(0.9)
    high_transaction_threshold = city_potential_full['Jumlah Transaksi'].quantile(0.95)
    high_spending_threshold = city_potential_full['Rata-rata Pengeluaran per Transaksi'].quantile(0.75)

    # Apply thresholds to get all potential markets
    potential_markets_full = city_potential_full[
        (city_potential_full['Jumlah Transaksi'] >= low_transaction_threshold) & 
        (city_potential_full['Jumlah Transaksi'] <= high_transaction_threshold) & 
        (city_potential_full['Rata-rata Pengeluaran per Transaksi'] > high_spending_threshold)
    ].sort_values('Rata-rata Pengeluaran per Transaksi', ascending=False)

    # Then filter by selected regions
    filtered_potential_markets = potential_markets_full[potential_markets_full['Region'].isin(selected_regions)]

    # Map section
    st.header("Peta Potensial Market")

    # Load GeoJSON
    geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    response = requests.get(geojson_url)
    brazil_geojson = response.json()

    selected_states = [state for state, region in state_to_region.items() if region in selected_regions]

    # Create map
    brazil_map = folium.Map(location=[-15.77972, -47.92972], zoom_start=4, tiles='CartoDB positron')

    folium.GeoJson(
        brazil_geojson,
        name="Brazil Regions",
        style_function=lambda feature: {
            "fillColor": region_colors.get(state_to_region.get(feature["properties"]["name"], "North"), "#FFFFFF") if feature["properties"]["name"] in selected_states else "transparent",
            "color": "black",
            "weight": 1 if feature["properties"]["name"] in selected_states else 0.5,
            "fillOpacity": 0.3 if feature["properties"]["name"] in selected_states else 0
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=["name"],
            aliases=["State:"],
            style=("background-color: white; color: black; font-family: arial; font-size: 12px; padding: 5px;")
        )
    ).add_to(brazil_map)

    # Only add markers for the filtered potential markets
    for _, row in filtered_potential_markets.iterrows():
        folium.CircleMarker(
            location=[row['geolocation_lat'], row['geolocation_lng']],
            radius=6,
            fill=True,
            fill_color="red",
            fill_opacity=0.5,
            popup=folium.Popup(f"{row['customer_city']}<br>Region: {row['Region']}<br>Avg Spending: {row['Rata-rata Pengeluaran per Transaksi']:.2f}", max_width=300),
            tooltip=row['customer_city']
        ).add_to(brazil_map)

    folium.LayerControl().add_to(brazil_map)

    # Display map
    folium_static(brazil_map)

    # Optionally, display the filtered potential markets data
    if st.checkbox("Show Potential Markets Data"):
        st.write(f"Showing {len(filtered_potential_markets)} potential markets from selected regions")
        st.dataframe(filtered_potential_markets[['customer_city', 'Region', 'Jumlah Transaksi', 'Total Pengeluaran', 'Rata-rata Pengeluaran per Transaksi']])

with tab3:
    st.header("Pola Waktu Pembelian")
    
    st.subheader("5 Kategori Produk Terpopuler")
    
    category_counts = filtered_data.groupby('product_category_name_english').size().reset_index(name='count')
    top_categories = category_counts.sort_values('count', ascending=False).head(5)
    
    if not top_categories.empty:
        # Plot ukuran untuk kategori produk terpopuler
        fig_top_products = plt.figure(figsize=(12, 6))
        sns.barplot(
            data=top_categories,
            x="product_category_name_english",
            y="count",
            palette="tab10"
        )
        plt.title("5 Kategori Produk Terpopuler", fontsize=14)
        plt.xlabel("Kategori Produk", fontsize=12)
        plt.ylabel("Jumlah Produk Terjual", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig_top_products)
    else:
        st.write("No data available for the selected regions")
    
    # Convert timestamp columns to datetime if they aren't already
    if 'order_purchase_timestamp' in filtered_data.columns and not pd.api.types.is_datetime64_any_dtype(filtered_data['order_purchase_timestamp']):
        filtered_data['order_purchase_timestamp'] = pd.to_datetime(filtered_data['order_purchase_timestamp'])
    
    # Extract time components
    filtered_data['order_month'] = filtered_data['order_purchase_timestamp'].dt.month
    filtered_data['order_day'] = filtered_data['order_purchase_timestamp'].dt.day_name()
    filtered_data['order_hour'] = filtered_data['order_purchase_timestamp'].dt.hour
    
    # Radio button for total or by region analysis
    analysis_type = st.radio(
        "Pilih Jenis Analisis", 
        ["Total (Semua Region)", "Per Region"]
    )
    
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("Set2")
    
    if analysis_type == "Total (Semua Region)":
        # Pola pembelian bulanan (total)
        monthly_purchase = filtered_data.groupby('order_month')['order_id'].nunique().reset_index(name='order_count')

        # Pola pembelian berdasarkan hari (total)
        daily_purchase = filtered_data.groupby('order_day')['order_id'].nunique().reset_index(name='order_count')

        # Pola pembelian berdasarkan jam (total)
        hourly_purchase = filtered_data.groupby('order_hour')['order_id'].nunique().reset_index(name='order_count')

        # 1. Monthly Order Patterns (Total)
        st.subheader("Pola Pembelian Bulanan")
        
        # Ensure months are in order
        monthly_purchase['order_month'] = pd.to_numeric(monthly_purchase['order_month'])
        monthly_purchase = monthly_purchase.sort_values('order_month')

        # Map month numbers to names
        month_names = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        monthly_purchase['month_name'] = monthly_purchase['order_month'].map(month_names)

        # Plot line chart for monthly patterns
        fig_monthly = plt.figure(figsize=(12, 6))
        sns.lineplot(data=monthly_purchase, x='month_name', y='order_count', marker='o', linewidth=2.5, color='blue')
        plt.title('Pola Pembelian Bulanan', fontsize=16)
        plt.xlabel('Bulan', fontsize=12)
        plt.ylabel('Jumlah Order', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig_monthly)

        # 2. Daily Order Patterns (Total)
        st.subheader("Pola Pembelian Berdasarkan Hari")
        
        # Define the correct order of days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_purchase['order_day'] = pd.Categorical(daily_purchase['order_day'], categories=day_order, ordered=True)
        daily_purchase = daily_purchase.sort_values('order_day')

        # Plot line chart for daily patterns
        fig_daily = plt.figure(figsize=(12, 6))
        sns.lineplot(data=daily_purchase, x='order_day', y='order_count', marker='o', linewidth=2.5, color='green')
        plt.title('Pola Pembelian Berdasarkan Hari', fontsize=16)
        plt.xlabel('Hari', fontsize=12)
        plt.ylabel('Jumlah Order', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig_daily)

        # 3. Hourly Order Patterns (Total)
        st.subheader("Pola Pembelian Berdasarkan Jam")
        
        # Ensure hours are in order
        hourly_purchase['order_hour'] = pd.to_numeric(hourly_purchase['order_hour'])
        hourly_purchase = hourly_purchase.sort_values('order_hour')

        # Plot line chart for hourly patterns
        fig_hourly = plt.figure(figsize=(12, 6))
        sns.lineplot(data=hourly_purchase, x='order_hour', y='order_count', marker='o', linewidth=2.5, color='purple')
        plt.title('Pola Pembelian Berdasarkan Jam', fontsize=16)
        plt.xlabel('Jam (Format 24-jam)', fontsize=12)
        plt.ylabel('Jumlah Order', fontsize=12)
        plt.xticks(range(0, 24))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig_hourly)
        
    else:  # Per Region
        # Pola pembelian bulanan per region
        monthly_purchase_region = filtered_data.groupby(['region', 'order_month'])['order_id'].nunique().reset_index(name='order_count')
        
        # Pola pembelian berdasarkan hari per region
        daily_purchase_region = filtered_data.groupby(['region', 'order_day'])['order_id'].nunique().reset_index(name='order_count')
        
        # Pola pembelian berdasarkan jam per region
        hourly_purchase_region = filtered_data.groupby(['region', 'order_hour'])['order_id'].nunique().reset_index(name='order_count')
        
        # 1. Monthly Order Patterns by Region
        st.subheader("Pola Pembelian Bulanan per Region")
        
        # Ensure months are in order
        monthly_purchase_region['order_month'] = pd.to_numeric(monthly_purchase_region['order_month'])
        
        # Map month numbers to names
        month_names = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        monthly_purchase_region['month_name'] = monthly_purchase_region['order_month'].map(month_names)
        
        # Sort by month
        monthly_purchase_region = monthly_purchase_region.sort_values('order_month')
        
        # Plot line chart for monthly patterns by region
        fig_monthly_region = plt.figure(figsize=(12, 6))
        sns.lineplot(data=monthly_purchase_region, x='month_name', y='order_count', hue='region', marker='o', linewidth=2.5)
        plt.title('Pola Pembelian Bulanan per Region', fontsize=16)
        plt.xlabel('Bulan', fontsize=12)
        plt.ylabel('Jumlah Order', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.legend(title='Region', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig_monthly_region)
        
        # 2. Daily Order Patterns by Region
        st.subheader("Pola Pembelian Berdasarkan Hari per Region")
        
        # Define the correct order of days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_purchase_region['order_day'] = pd.Categorical(daily_purchase_region['order_day'], categories=day_order, ordered=True)
        daily_purchase_region = daily_purchase_region.sort_values('order_day')
        
        # Plot line chart for daily patterns by region
        fig_daily_region = plt.figure(figsize=(12, 6))
        sns.lineplot(data=daily_purchase_region, x='order_day', y='order_count', hue='region', marker='o', linewidth=2.5)
        plt.title('Pola Pembelian Berdasarkan Hari per Region', fontsize=16)
        plt.xlabel('Hari', fontsize=12)
        plt.ylabel('Jumlah Order', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.legend(title='Region', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig_daily_region)
        
        # 3. Hourly Order Patterns by Region
        st.subheader("Pola Pembelian Berdasarkan Jam per Region")
        
        # Ensure hours are in order
        hourly_purchase_region['order_hour'] = pd.to_numeric(hourly_purchase_region['order_hour'])
        hourly_purchase_region = hourly_purchase_region.sort_values('order_hour')
        
        # Plot line chart for hourly patterns by region
        fig_hourly_region = plt.figure(figsize=(12, 6))
        sns.lineplot(data=hourly_purchase_region, x='order_hour', y='order_count', hue='region', marker='o', linewidth=2.5)
        plt.title('Pola Pembelian Berdasarkan Jam per Region', fontsize=16)
        plt.xlabel('Jam (Format 24-jam)', fontsize=12)
        plt.ylabel('Jumlah Order', fontsize=12)
        plt.xticks(range(0, 24))
        plt.grid(True, alpha=0.3)
        plt.legend(title='Region', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig_hourly_region)
        