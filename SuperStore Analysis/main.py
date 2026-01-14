import pandas as pd
import streamlit as st
import joblib

st.set_page_config(
    page_title='Discount Predictor',
    layout='wide'
)

@st.cache_resource
def load_model(file_path):
    try:
        model = joblib.load(file_path)
        st.success("Model loaded successfully!")
        return model
    except Exception as e:
        st.error(f'Error: {e}')

model = load_model(r"model.pkl")

st.title('Predict discount easilty')
st.markdown('---')
col_a, col_b = st.columns(2, gap='large', border=True, vertical_alignment='center')
with col_a:
    shipmode = st.selectbox('Ship Mode', ['Second Class','Standard Class','First Class','Same Day'], index=0)
    Segment = st.selectbox('Segment', ['Consumer','Corporate','Home Office'], index=0)
    City = st.text_input('City (from United States)', placeholder='Eg: Los Angeles, Henderson, Miami')
    Region = st.selectbox('Region', ['South','West','Central','East'], index=0)
    Category = st.selectbox('Ctaegory', ['Furniture', 'Office Supplies','Technology'], index=1)

with col_b:
    SubCategory = st.selectbox(
        "Sub-Category",
        ['Bookcases',
         'Chairs',
         'Labels',
         'Tables',
         'Storage',
         'Furnishings',
         'Art',
         'Phones',
         'Binders',
         'Appliances',
         'Paper',
         'Envelopes',
         'Supplies',
         'Fasteners',
         'Copiers']
    )
    Quantity = st.number_input('Quantity', min_value=0, max_value=50, step=1)
    Sales = st.number_input('Sales', min_value=0, max_value=100000)
    IfProfit = st.radio(label='If Profit?', options=['yes','no'], index=0)

st.markdown('---')

st.subheader('Review Inputs')
data = {
    'Ship Mode':[shipmode],
    'Segment':[Segment],
    'City':[City],
    'Region':[Region],
    'Category':[Category],
    'Sub-Category':[SubCategory],
    'Sales':[Sales],
    'Quantity':[Quantity],
    'if_profit':[IfProfit]
}

df = pd.DataFrame(data, index=[0])

st.table(df, border=True)
st.markdown('---')

if st.button('Submit', type='primary'):
    if model is not None:
        with st.spinner('Predicting...'):
            try:
                pred_discount = model.predict(df)
                st.success(f'Predicted Discount: {pred_discount[0]:.2f} %')
            except Exception as e:
                st.error(f'Error: {e}')
    else:
        st.error('Error: Cannot run prediction because model failed to load.')