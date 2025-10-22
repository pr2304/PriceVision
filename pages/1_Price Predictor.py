import streamlit as st
import pickle
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(page_title='Property Price Predictor', layout='wide')

# --- MOCK DATA and PIPELINE ---
# In a real scenario, you would load your actual 'df.pkl' and 'pipeline.pkl'.
# For this example to be runnable, we'll create mock versions.

# Mock DataFrame
mock_data = {
    'sector': [f'Sector {i}' for i in range(1, 6)],
    'bedRoom': [2.0, 3.0, 4.0],
    'bathroom': [2.0, 3.0, 4.0],
    'balcony': ['1', '2', '3+'],
    'agePossession': ['New Property', 'Resale', 'Recently Constructed'],
    'furnishing_type': ['Unfurnished', 'Semi-Furnished', 'Furnished'],
    'luxury_category': ['Low', 'Medium', 'High'],
    'floor_category': ['Low Floor', 'Mid Floor', 'High Floor']
}
# Create a more comprehensive mock df by combining the lists
df_mock = pd.DataFrame({
    'sector': np.random.choice(mock_data['sector'], 100),
    'bedRoom': np.random.choice(mock_data['bedRoom'], 100),
    'bathroom': np.random.choice(mock_data['bathroom'], 100),
    'balcony': np.random.choice(mock_data['balcony'], 100),
    'agePossession': np.random.choice(mock_data['agePossession'], 100),
    'furnishing_type': np.random.choice(mock_data['furnishing_type'], 100),
    'luxury_category': np.random.choice(mock_data['luxury_category'], 100),
    'floor_category': np.random.choice(mock_data['floor_category'], 100),
})


# Mock Pipeline
class MockPipeline:
    def predict(self, df):
        # Return a random prediction for demonstration purposes
        return np.log1p(np.random.uniform(0.5, 5.0, len(df)))

pipeline_mock = MockPipeline()

# Use actual files if they exist, otherwise use mocks
try:
    with open('df.pkl', 'rb') as file:
        df = pickle.load(file)
except FileNotFoundError:
    st.warning("`df.pkl` not found. Using mock data for demonstration.")
    df = df_mock

try:
    with open('pipeline.pkl', 'rb') as file:
        pipeline = pickle.load(file)
except FileNotFoundError:
    st.warning("`pipeline.pkl` not found. Using a mock prediction model.")
    pipeline = pipeline_mock
# --- END MOCK DATA ---


# Page title
st.title("🏠 Property Price Predictor")
st.write("Enter property details to get an estimated price range.")

# Input section using columns for better layout
with st.form("property_form"):
    st.markdown("#### **Property & Location Details**")
    col1, col2, col3 = st.columns(3)

    with col1:
        property_type = st.selectbox('Property Type', ['Flat', 'House'])
        sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
        bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))

    with col2:
        bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
        balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
        property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

    with col3:
        built_up_area = st.number_input('Built Up Area (sq ft)', min_value=100.0, max_value=10000.0, value=1200.0, step=50.0)
        servant_room = float(st.selectbox('Servant Room', [0.0, 1.0], format_func=lambda x: 'Yes' if x == 1.0 else 'No'))
        store_room = float(st.selectbox('Store Room', [0.0, 1.0], format_func=lambda x: 'Yes' if x == 1.0 else 'No'))

    st.markdown("---")
    st.markdown("#### **Furnishing & Category Details**")
    col4, col5, col6 = st.columns(3)

    with col4:
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
    with col5:
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
    with col6:
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

    # Submit button
    submitted = st.form_submit_button("Predict Price")


if submitted:
    if not built_up_area:
        st.error("Built Up Area must be provided.")
    else:
        # Prepare data for prediction
        data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area,
                 servant_room, store_room, furnishing_type, luxury_category, floor_category]]

        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
                   'agePossession', 'built_up_area', 'servant room', 'store room',
                   'furnishing_type', 'luxury_category', 'floor_category']

        input_df = pd.DataFrame(data, columns=columns)

        # Predict price using the pipeline
        with st.spinner('Calculating the estimated price...'):
            base_price = np.expm1(pipeline.predict(input_df))[0]
            # Define a range for the price estimate
            low = base_price * 0.90
            high = base_price * 1.10

        # Display result
        st.markdown("### 💵 Estimated Price Range")
        st.success(f"The estimated price is between **₹ {low:.2f} Cr** and **₹ {high:.2f} Cr**")

        # JavaScript to scroll the page down to the result
        components.html(
            """
            <script>
            window.parent.document.body.scrollIntoView({ behavior: 'smooth', block: 'end' });
            </script>
            """,
            height=0
        )


