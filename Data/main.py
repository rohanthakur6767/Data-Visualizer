import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Data Visualizer', layout='centered', page_icon='📊')

st.title('📊 Data Visualizer')

# Define the folder path relative to the script
folder_path = os.path.join(os.path.dirname(__file__), 'Data')

# Check if the folder exists
if not os.path.exists(folder_path):
    st.error(f"Folder not found: {folder_path}")
    files = []
else:
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Option to upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    selected_file = "Uploaded File"
else:
    selected_file = st.selectbox('Select a file', files, index=None)
    if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        df = pd.read_csv(file_path)

if selected_file or uploaded_file:
    st.write(df.head())

    columns = df.columns.tolist()

    x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
    y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

    plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
    plot_type = st.selectbox('Select the type of plot', options=plot_list)

    if st.button('Generate Plot'):
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

        plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)

        st.pyplot(fig)
