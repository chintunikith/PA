import pandas as pd
import streamlit as st
from PIL import Image


img = Image.open(r"Roche Logo.jpg")
# st.image(img,width=120)
st.sidebar.image(img,  use_column_width=True)
st.title("Roche Prism Access")

st.header("Market Authorization and Reimbursement Bodies",divider="gray")

# Load Excel data for Europe
@st.cache_data
def load_europe_data():
    df = pd.read_excel("Europe_MA.xlsx")  # Read Europe Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], errors='coerce', dayfirst=True)  # Parse dates with day first format
    return df

# Load Excel data for USA
@st.cache_data
def load_usa_data():
    df = pd.read_excel("USA_MA.xlsx")  # Read USA Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], errors='coerce')  # Parse dates
    return df

# Load Excel data for Germany (Market Authorization)
@st.cache_data
def load_germany_ma_data():
    df = pd.read_excel("Germany_MA.xlsx")  # Read Germany Market Authorization Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], errors='coerce')  # Parse dates
    return df

# Load Excel data for Germany (Reimbursement)
@st.cache_data
def load_germany_reimbursement_data():
    df = pd.read_excel("Germany_Reimbursement.xlsx")  # Read Germany Reimbursement Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], format='%d.%m.%Y', errors='coerce')  # Parse dates with specific format
    return df

# Load Excel data for Australia (Market Authorization)
@st.cache_data
def load_australia_data():
    df = pd.read_excel("Australia_MA.xlsx")  # Read Australia Market Authorization Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], errors='coerce')  # Parse dates
    return df

# Load Excel data for Australia (Reimbursement)
@st.cache_data
def load_australia_reimbursement_data():
    df = pd.read_excel("Australia_Reimbursement.xlsx")  # Read Australia Reimbursement Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], format='%d.%m.%Y', errors='coerce')  # Parse dates with specific format
    return df

# Load Excel data for UK (Market Authorization)
@st.cache_data
def load_uk_ma_data():
    df = pd.read_excel("UK_MA.xlsx")  # Read UK Market Authorization Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], format='%d-%m-%Y', errors='coerce')  # Parse dates with specific format
    return df

# Load Excel data for UK (Reimbursement)
@st.cache_data
def load_uk_reimbursement_data():
    df = pd.read_excel("UK_Reimbursement.xlsx")  # Read UK Reimbursement Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], format='%d-%m-%Y', errors='coerce')  # Parse dates with specific format
    return df

# Load Excel data for Scotland (Market Authorization)
@st.cache_data
def load_scotland_ma_data():
    df = pd.read_excel("Scotland_MA.xlsx")  # Read Scotland Market Authorization Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], format='%d-%m-%Y', errors='coerce')  # Parse dates with specific format
    return df

# Load Excel data for Scotland (Reimbursement)
@st.cache_data
def load_scotland_reimbursement_data():
    df = pd.read_excel("Scotland_Reimbursement.xlsx")  # Read Scotland Reimbursement Excel file
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], format='%d/%m/%Y', errors='coerce')  # Parse dates with specific format
    return df

# Streamlit UI
# Streamlit UI


# Initialize select box lists
selected_country = st.selectbox("Select Country:", ["Europe", "USA", "Germany", "Australia", "UK", "Scotland"])

# Show radio buttons conditionally based on selected country


df_new = pd.read_excel(r"Roadmaps-Procedures.xlsx")
# print(df_new.columns)

df_new_disp = df_new[df_new["Region "] == selected_country]
st.data_editor(
    df_new_disp,
    column_config={
        "Market Authorization Process": st.column_config.LinkColumn(
            "Reimbursement  Process",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            display_text="https://(.*?)\.streamlit\.app"
        ),
        "Market Authorization Body": st.column_config.LinkColumn(
            "Market Authorization Body",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            display_text="https://(.*?)\.streamlit\.app"
        ),
        "Reimbursement  Process": st.column_config.LinkColumn(
            "Reimbursement  Process",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            display_text="https://(.*?)\.streamlit\.app"
        ),
        "Reimbursement  Body": st.column_config.LinkColumn(
            "Reimbursement  Body",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            display_text="https://(.*?)\.streamlit\.app"
        ),
        "Additional references": st.column_config.LinkColumn(
            "Additional References",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            display_text="https://(.*?)\.streamlit\.app"
        )
        
    },
    hide_index=True,
)
st.header("Market Authorization and Reimbursement Details",divider="gray")

if selected_country in ["Europe", "USA"]:
    authorization_type = st.radio("Select Data Type:", ("Market Authorization",))
else:
    authorization_type = st.radio("Select Data Type:", ("Market Authorization", "Reimbursement"))
data = None

# Load data based on selected country and authorization type
if selected_country == "Europe":
    if authorization_type == "Market Authorization":
        data = load_europe_data()
elif selected_country == "USA":
    if authorization_type == "Market Authorization":
        data = load_usa_data()
elif selected_country == "Germany":
    if authorization_type == "Market Authorization":
        data = load_germany_ma_data()
    else:  # Reimbursement
        data = load_germany_reimbursement_data()
elif selected_country == "Australia":
    if authorization_type == "Market Authorization":
        data = load_australia_data()
    else:  # Reimbursement
        data = load_australia_reimbursement_data()
elif selected_country == "UK":
    if authorization_type == "Market Authorization":
        data = load_uk_ma_data()
    else:  # Reimbursement
        data = load_uk_reimbursement_data()
elif selected_country == "Scotland":
    if authorization_type == "Market Authorization":
        data = load_scotland_ma_data()
    else:  # Reimbursement
        data = load_scotland_reimbursement_data()



# Update product names, INNs, and indications based on selected data
if data is not None:
    product_names = data["Product Name"].dropna().unique() if "Product Name" in data.columns else []
    inns = data["INN - Active Substance"].dropna().unique() if "INN - Active Substance" in data.columns else []
    indications = data["Indication - Therapeutic Area"].dropna().unique() if "Indication - Therapeutic Area" in data.columns else []
else:
    product_names = []
    inns = []
    indications = []

# Select box for product name if data is available
if product_names.size > 0:
    selected_product_name = st.selectbox("Select Product Name:", [""] + list(product_names))
else:
    selected_product_name = ""

# Select box for INN if data is available
if inns.size > 0:
    selected_inn = st.selectbox("Select INN - Active Substance:", [""] + list(inns))
else:
    selected_inn = ""

# Select box for Indication if data is available
if indications.size > 0:
    selected_indication = st.selectbox("Select Indication - Therapeutic Area:", [""] + list(indications))
else:
    selected_indication = ""

# Date range input
date_start = st.date_input("Start Date of Decision:", value=None)
date_end = st.date_input("End Date of Decision:", value=None)

# Filter data based on user input
if data is not None:
    filtered_data = data.copy()
    
    if selected_product_name:  # Filter product name regardless of country
        filtered_data = filtered_data[filtered_data["Product Name"] == selected_product_name]

    if selected_inn:
        filtered_data = filtered_data[filtered_data["INN - Active Substance"] == selected_inn]
    
    if selected_indication:
        filtered_data = filtered_data[filtered_data["Indication - Therapeutic Area"] == selected_indication]

    if date_start and date_end:
        date_start = pd.Timestamp(date_start)
        date_end = pd.Timestamp(date_end)
        filtered_data = filtered_data[(filtered_data["Date of decision"] >= date_start) & 
                                      (filtered_data["Date of decision"] <= date_end)]

    # Drop columns with all NaN values
    filtered_data.dropna(how='all', axis=1, inplace=True)

    # Drop unnamed columns
    filtered_data = filtered_data.loc[:, ~filtered_data.columns.str.contains('^Unnamed')]
    


    # Display filtered data if there are selections made and data is filtered
    if (selected_product_name or selected_inn or selected_indication or date_start or date_end) and not filtered_data.empty:
        st.data_editor(
    filtered_data,
    column_config={
        "Source of truth": st.column_config.LinkColumn(
            "Source of Truth",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            display_text="https://(.*?)\.streamlit\.app"
        ),
        
    },
    hide_index=True,
)

    elif not (selected_product_name or selected_inn or selected_indication or date_start or date_end):
        st.write("Please select filters to display data.")
    else:
        st.write("No data available for the selected criteria.")
else:
    st.write("No data available for the selected criteria.")
