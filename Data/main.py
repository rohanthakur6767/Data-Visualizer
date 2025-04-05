import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Title
st.title('📊 Data Visualizer')

# Get current working directory
working_dir = os.getcwd()  # This works better in Streamlit Cloud

# Specify the folder where CSV files should be (if running locally)
folder_path = os.path.join(working_dir, 'Data')

# Initialize files list
files = []

# Check if folder exists and list CSV files
if os.path.exists(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
else:
    st.warning(f"⚠️ Folder not found: {folder_path}\nUpload a CSV file instead.")

# Upload a CSV file
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

# Initialize DataFrame
df = None

# Load data from uploaded file or selected local file
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    selected_file = "Uploaded File"
elif files:
    selected_file = st.selectbox('📁 Select a file from local folder', files, index=None)
    if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        df = pd.read_csv(file_path)

# Display DataFrame and plotting options if data is loaded
if df is not None:
    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("### Data Preview")
        st.write(df.head())

    with col2:
        st.write("### Plot Configuration")
        x_axis = st.selectbox('📊 Select X-axis', options=columns)
        y_axis = st.selectbox('📊 Select Y-axis', options=columns)

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        plot_type = st.selectbox('📌 Select Plot Type', options=plot_list)

    # Generate the plot
    if st.button('📈 Generate Plot'):
        fig, ax = plt.subplots(figsize=(6, 4))

        if plot_type == 'Line Plot':
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Bar Chart':
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Scatter Plot':
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Distribution Plot':
            sns.histplot(df[x_axis], kde=True, ax=ax)
            y_axis = 'Density'
        elif plot_type == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax)
            y_axis = 'Count'

        # Adjust labels
        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)

        # Show the results
        st.pyplot(fig)
