import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Set the page config
st.set_page_config(
    page_title='📊 Data Visualizer',
    layout='centered',
    page_icon='📊'
)

# Title
st.title('📊 Data Visualizer')

# Get the working directory
working_dir = os.getcwd()  # Use current working directory

# Specify the folder where CSV files are stored
folder_path = os.path.join(working_dir, 'Data')

# Check if the folder exists
if not os.path.exists(folder_path):
    st.warning(f"⚠️ Folder not found: `{folder_path}`. Please upload a file.")
    files = []
else:
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# File uploader
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

df = None  # Initialize dataframe

# Handle uploaded file
if uploaded_file:
    with st.spinner('Loading file...'):
        time.sleep(1)  # Simulating load time
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

# File selection dropdown (only show if files exist)
if files:
    selected_file = st.selectbox('📁 Select a file', files)
    if selected_file:
        with st.spinner('Loading data...'):
            time.sleep(1)
            file_path = os.path.join(folder_path, selected_file)
            df = pd.read_csv(file_path)
            st.success(f"✅ Loaded `{selected_file}`")

if df is not None:
    # Show data preview
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    # Show data statistics
    st.subheader("📊 Data Statistics")
    st.write(df.describe())

    # Column selection for visualization
    columns = df.columns.tolist()
    x_axis = st.selectbox('📌 Select X-axis', options=columns + ["None"])
    y_axis = st.selectbox('📌 Select Y-axis', options=columns + ["None"])

    plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
    plot_type = st.selectbox('📈 Select the type of plot', options=plot_list)

    # Generate the plot with animation
    if st.button('🚀 Generate Plot'):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

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

        st.pyplot(fig)
        st.success("🎉 Plot generated successfully!")
