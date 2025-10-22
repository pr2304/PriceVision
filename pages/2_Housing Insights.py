import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title='Housing Insights', layout='wide')
st.title('🏘️ Housing Insights Dashboard')

# Load data
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))

# Tabs for better organization
tabs = st.tabs(["Geomap", "WordCloud", "Price Analysis", "BHK Analysis", "Distribution"])

# ------------------ GEOMAP ------------------
with tabs[0]:
    st.header('Sector Price per Sqft Geomap')
    group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean().reset_index()
    fig = px.scatter_mapbox(
        group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
        mapbox_style="open-street-map", width=1000, height=600, hover_name="sector"
    )
    st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True, 'displayModeBar': True, 'displaylogo': False})

# ------------------ WORDCLOUD ------------------
with tabs[1]:
    st.header("Features WordCloud")
    wordcloud_property_type = st.selectbox('Select Property Type for WordCloud', ['overall', 'flat', 'house'])
    stop_words = STOPWORDS.union({"is", "are", "will", "s"})

    if wordcloud_property_type == 'overall':
        text_data = feature_text
    else:
        filtered_df = new_df[new_df['property_type'] == wordcloud_property_type]
        text_data = ' '.join(filtered_df['features'].dropna().astype(str).tolist()) if 'features' in filtered_df.columns else feature_text

    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stop_words, min_font_size=10).generate(text_data)
    fig_wc = plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(fig_wc)

# ------------------ PRICE ANALYSIS ------------------
with tabs[2]:
    st.header('Area vs Price')
    col1, col2 = st.columns(2)
    with col1:
        property_type_select = st.selectbox('Select Property Type for Price Chart', ['flat', 'house'])
    with col2:
        bedroom_filter = st.slider('Filter by BHK', min_value=int(new_df['bedRoom'].min()), max_value=int(new_df['bedRoom'].max()), value=(int(new_df['bedRoom'].min()), int(new_df['bedRoom'].max())))

    filtered_df = new_df[(new_df['property_type'] == property_type_select) & (new_df['bedRoom'].between(*bedroom_filter))]
    fig_area = px.scatter(filtered_df, x="built_up_area", y="price", color="bedRoom", title=f"Area vs Price for {property_type_select.title()}")
    st.plotly_chart(fig_area, use_container_width=True)

# ------------------ BHK ANALYSIS ------------------
with tabs[3]:
    st.header('BHK Analysis')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('BHK Pie Chart')
        sector_options = ['overall'] + list(new_df['sector'].unique())
        selected_sector = st.selectbox('Select Sector', sector_options)
        df_sector = new_df if selected_sector == 'overall' else new_df[new_df['sector'] == selected_sector]
        fig_pie = px.pie(df_sector, names='bedRoom', title=f'BHK Distribution in {selected_sector.title()}')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader('BHK Price Comparison')
        df_bhk = new_df[new_df['bedRoom'] <= 4]
        fig_box = px.box(df_bhk, x='bedRoom', y='price', color='bedRoom', title='BHK Price Range')
        st.plotly_chart(fig_box, use_container_width=True)

# ------------------ DISTRIBUTION ------------------
with tabs[4]:
    st.header('Price Distribution by Property Type')
    fig_dist = plt.figure(figsize=(12, 5))
    sns.histplot(new_df[new_df['property_type'] == 'house']['price'], kde=True, label='House', color='skyblue', stat="density")
    sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], kde=True, label='Flat', color='orange', stat="density")
    plt.title('Price Distribution')
    plt.legend()
    st.pyplot(fig_dist)
