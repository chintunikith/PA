import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
# Title and header
st.header("R&R Data Explorer", divider = "gray")
# st.header("Market Authorization and Reimbursement Bodies", divider="gray")

# Function to load data
@st.cache_data
def load_data(file_name):
    df = pd.read_excel(file_name)
    df["Date of decision"] = pd.to_datetime(df["Date of decision"], errors='coerce',format='mixed')
    # Drop columns where all values are None
    df.dropna(axis=1, how='all', inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


# Load Excel data based on country and type
@st.cache_data
def load_country_data(country, data_type):
    if country == "Europe" or country == "USA":
        return load_data(f"{country}_MA.xlsx")
    else:
        temp = "MA" if data_type == "Market Authorization" else "Reimbursement"
        return load_data(f"{country}_{temp}.xlsx")
    
def visualize(num):
    color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    grouped_counts = filtered_data[authorization_type + ' Status'].value_counts()
    status_color_map = dict(zip(grouped_counts.index, color_list))
    col1, col2 = st.columns((3.5, 6.5))
    # Donut chart
    def donut():
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(grouped_counts.values, labels=grouped_counts.index,
                                        autopct=lambda pct: f'{int(round(pct / 100 * sum(grouped_counts.values)))}',
                                        startangle=120, colors=[status_color_map.get(status, 'gray') for status in grouped_counts.index], wedgeprops={'edgecolor': 'white'})
        ax.axis('equal')  
        centre_circle = plt.Circle((0, 0), 0.50, color='white')
        ax.add_artist(centre_circle)
        ax.legend(fontsize=20,loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=1)
        for text in texts + autotexts:
            text.set_fontsize(14)

        with col1:
            st.subheader('Number of decisions')
            st.pyplot(fig)

    #Bar graph
    def bar(val):
        top_areas = filtered_data[val].value_counts().head(5).index.tolist()
        nested_dict = {}

        for area in top_areas:
            subset_df = filtered_data[filtered_data[val] == area]
            status_counts = subset_df[authorization_type + ' Status'].value_counts().to_dict()
            nested_dict[area] = status_counts

        therapeutic_areas = list(nested_dict.keys())
        x_labels = grouped_counts.index
        y_labels = therapeutic_areas
        data_values = [[nested_dict[area].get(status, 0) for status in grouped_counts.index] for area in therapeutic_areas]
        
        # Sort therapeutic areas by the sum of counts
        therapeutic_areas_sorted = sorted(therapeutic_areas, key=lambda area: sum(nested_dict[area].values()), reverse=False)
        fig1, ax = plt.subplots(figsize=(13, 11))
        bar_width = 0.25
        bar_positions = np.arange(len(therapeutic_areas_sorted))

        for i, status in enumerate(grouped_counts.index):
            counts_sorted = [nested_dict[area].get(status, 0) for area in therapeutic_areas_sorted]
            bars = ax.barh(bar_positions - bar_width / 2 + i * bar_width, counts_sorted, height=bar_width, label=status, color=status_color_map.get(status, 'gray'))
            for bar, value in zip(bars, counts_sorted):
                ax.annotate(f'{value}', xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2), 
                            xytext=(5, 0),  # 5 points horizontal offset
                            textcoords='offset points',
                            ha='left', va='center', fontsize=25)

        ax.set_yticks(bar_positions)
        ax.set_yticklabels(therapeutic_areas_sorted, fontsize=25)
        ax.legend(fontsize=25,loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=1)
        ax.tick_params(axis='x', which='major', labelsize=25, length=3)
        ax.set_aspect('auto')

        with col2:
            st.subheader('Top 5 '+val)
            st.pyplot(fig1)

    if num==1:
        donut()
        bar('Manufacturer')
    if num==2:
        donut()
        bar('Therapeutic Area')
st.header("Market Authorization and Reimbursement Authorities", divider="gray")


# Streamlit UI for selecting country and data type
selected_country = st.selectbox("Select Country:", ["Europe", "USA", "Germany", "Australia", "UK", "Scotland"])

df_new = pd.read_excel("Roadmaps-Procedures.xlsx")
df_new_disp = df_new[df_new["Region "] == selected_country]
st.data_editor(
    df_new_disp,
    column_config={
        "Market Authorization Process": st.column_config.LinkColumn(
            "Market Authorization Process",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            # display_text="https://(.*?)\.streamlit\.app"
            display_text = "source"
        ),
        
        "Reimbursement  Process": st.column_config.LinkColumn(
            "Reimbursement  Process",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            # display_text="https://(.*?)\.streamlit\.app"
            display_text = "source"
        ),
        "Additional references": st.column_config.LinkColumn(
            "Additional References",
            help="Click to open",
            validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            # display_text="https://(.*?)\.streamlit\.app"
            display_text="source"
        )
    },
    hide_index=True,
)

# st.header("Market Authorization and Reimbursement Details", divider="gray")


if selected_country == "Europe":
    st.link_button("Market Authorization Procedure Summary", "https://docs.google.com/document/d/10GRfl8GDVBQxiv0V5chL51NQdwWKvNJgqkTkvabu_1k/edit?usp=sharing")
    # st.link_button("Reimbursement Procedure Summary", reimbursement_proc_url)
elif selected_country == "USA":
    st.link_button("Market Authorization Procedure Summary", "https://docs.google.com/document/d/1kCf6dmgI2SOB0Qi1aRoOeUKaZsZmaFXCfhuwn_PkAMA/edit?usp=sharing")
    # st.link_button("Reimbursement Procedure Summary", reimbursement_proc_url)
elif selected_country == "Germany":
    st.link_button("Market Authorization Procedure Summary", "https://docs.google.com/document/d/1oEOdFCjHb9umnTWeju0w7NBCfbtf4usY904Tw8mae1A/edit?usp=sharing")
    st.link_button("Reimbursement Procedure Summary", "https://docs.google.com/document/d/1B3m0bYUtCp5Dv0AtNKw4ro7VCKzepXuU7SpYUI5lBBw/edit?usp=sharing")
elif selected_country == "Australia":
    st.link_button("Market Authorization Procedure Summary", "https://docs.google.com/document/d/12UsGDDaLU58BPmd5UhykzkMPDLpUgxXbp_TQJwpiQjs/edit?usp=sharing")
    st.link_button("Reimbursement Procedure Summary", "https://docs.google.com/document/d/1YkE6LTbmc9Stvv5FxuZtlqr_rL1GI_3qGfdTEAN4tS0/edit?usp=sharing")
elif selected_country == "UK":
    st.link_button("Market Authorization Procedure Summary", "https://docs.google.com/document/d/1pZb5SaVaTvCQsvsChr0vdaLDymgzu2eK6-u8kKxxYZ0/edit?usp=sharing")
    st.link_button("Reimbursement Procedure Summary", "https://docs.google.com/document/d/1XbFvugZ-Vt-FtbEM6eOjTWBchcZcxkrQOg6JRSEPxFo/edit?usp=sharing")
elif selected_country == "Scotland":
    st.link_button("Market Authorization Procedure Summary", "https://docs.google.com/document/d/1DPF-V3AUzjK_k68pI139Y4ZRO-Sh3pInwZz1_zSPR1Q/edit?usp=sharing")
    st.link_button("Reimbursement Procedure Summary", "https://docs.google.com/document/d/1-DaPRI-s0nt0gNFwL8xLh332NnxGNgHMzWh5iLzqvVg/edit?usp=sharing")

st.header("Market Authorization and Reimbursement Details", divider="gray")

if selected_country in ["Europe", "USA"]:
    authorization_type = st.radio("Select Data Type:", ("Market Authorization",))
else:
    authorization_type = st.radio("Select Data Type:", ("Market Authorization", "Reimbursement"))

# Load data based on selections
data = load_country_data(selected_country, authorization_type)

# Check which columns are available for searching
search_options = []
if 'Product Name' in data.columns:
    search_options.append("Product Name")
if 'Active Substance' in data.columns:
    search_options.append("Active Substance")
if 'Therapeutic Area' in data.columns:
    search_options.append("Therapeutic Area")

# Dropdown for selecting search type
search_type = st.selectbox("Select Search Type:", search_options)

selected_indication=[]
selected_product_name=[]
selected_inn=[]
# Conditional dropdowns based on search type selection
if search_type == "Product Name":
    product_names = data["Product Name"].dropna().unique()
    selected_product_name = st.selectbox("Select Product Name:", [""] + list(product_names))
elif search_type == "Active Substance":
    inns = data["Active Substance"].dropna().unique()
    selected_inn = st.selectbox("Select Active Substance:", [""] + list(inns))
elif search_type == "Therapeutic Area":
    indications = data["Therapeutic Area"].dropna().unique()
    selected_indication = st.selectbox("Therapeutic Area:", [""] + list(indications))

# Date range input
date_start = st.date_input("Start Date of Decision:", value=None)
date_end = st.date_input("End Date of Decision:", value=None)

# Filter data based on user input
if data is not None:
    filtered_data = data.copy()

    if search_type == "Product Name" and selected_product_name:
        filtered_data = filtered_data[filtered_data["Product Name"] == selected_product_name]
    elif search_type == "Active Substance" and selected_inn:
        filtered_data = filtered_data[filtered_data["Active Substance"] == selected_inn]
    elif search_type == "Therapeutic Area" and selected_indication:
        filtered_data = filtered_data[filtered_data["Therapeutic Area"] == selected_indication]

    if date_start and date_end:
        date_start = pd.Timestamp(date_start)
        date_end = pd.Timestamp(date_end)
        filtered_data = filtered_data[(filtered_data["Date of decision"] >= date_start) & 
                                      (filtered_data["Date of decision"] <= date_end)]

    # Display filtered data if there are selections made and data is filtered
    if (selected_product_name or selected_inn or selected_indication or (date_start and date_end )) and not filtered_data.empty:

        if ("Market Authorization Status" in filtered_data.columns or "Reimbursement Status" in filtered_data.columns) and ("Therapeutic Area" in filtered_data.columns):
                # EMA Vis
                if (authorization_type == "Market Authorization" and selected_country == "Europe"):
                    if not ((filtered_data[authorization_type + ' Status'].isnull().any()) and filtered_data['Therapeutic Area'].isnull().any()):
                        visualize(2)
                # Germany Vis
                if (selected_country == "Germany"):
                    if not ((filtered_data[authorization_type + ' Status'].isnull().any()) and filtered_data['Therapeutic Area'].isnull().any()):
                        visualize(2)
                # UK_Vis_Reim
                if (authorization_type == "Reimbursement" and selected_country == "UK"):
                    if not ((filtered_data[authorization_type + ' Status'].isnull().any()) and filtered_data['Therapeutic Area'].isnull().any()):
                        visualize(2)
        elif ("Market Authorization Status" in filtered_data.columns or "Reimbursement Status" in filtered_data.columns):
                # USA_Vis
                if (selected_country == "USA"):
                    if not (filtered_data[authorization_type + ' Status'].isnull().any()):
                        visualize(1)
                # Australia_Vis
                if (selected_country == "Australia"):
                    if not (filtered_data[authorization_type + ' Status'].isnull().any()):
                        visualize(1)
                # Scotland_Vis
                if (selected_country == "Scotland"):
                    if not (filtered_data[authorization_type + ' Status'].isnull().any()):
                        visualize(1)
                #UK_Vis_MA
                if (selected_country == "UK" and authorization_type == "Market Authorization" ):
                    if not (filtered_data[authorization_type + ' Status'].isnull().any()):
                        visualize(1)
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
    else:
        st.write("No data available for the selected criteria.")
else:
    st.write("No data available for the selected criteria.")
