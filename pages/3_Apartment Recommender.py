import streamlit as st
import pickle
import pandas as pd


# Page configuration
st.set_page_config(page_title='Apartment Recommendations', layout='wide')
st.title("🏢 Smart Apartment Recommendations")

# Load data
location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

# ------------------ RECOMMENDER FUNCTION ------------------
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()
    recommendations_df = pd.DataFrame({
        'Property Name': top_properties,
        'Similarity Score': top_scores
    })
    return recommendations_df

# ------------------ LAYOUT USING TABS ------------------
tabs = st.tabs(["Search by Radius", "Recommend Apartments"])

# ---------- TAB 1: SEARCH BY RADIUS ----------
with tabs[0]:
    st.header("📍 Find Properties Within Radius")
    col1, col2 = st.columns([2, 1])

    with col1:
        selected_location = st.selectbox('Select Location', sorted(location_df.columns.to_list()))
    with col2:
        radius = st.number_input('Radius (in Kms)', min_value=1, max_value=50, value=5, step=1)

    if st.button('Search Properties', key='search_button'):
        result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
        if not result_ser.empty:
            st.success(f"Found {len(result_ser)} properties within {radius} Kms of {selected_location}")
            for key, value in result_ser.items():
                st.markdown(f"**{key}** — {round(value / 1000, 1)} kms")
        else:
            st.warning("No properties found within this radius.")

# ---------- TAB 2: RECOMMEND APARTMENTS ----------
with tabs[1]:
    st.header("🏠 Recommend Similar Apartments")
    selected_apartment = st.selectbox('Select an Apartment', sorted(location_df.index.to_list()))

    if st.button('Get Recommendations', key='recommend_button'):
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        st.success(f"Top {len(recommendation_df)} similar apartments to {selected_apartment}")
        st.dataframe(recommendation_df.style.format({'Similarity Score': "{:.2f}"}))
