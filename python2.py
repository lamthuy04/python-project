import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title = 'Python Project 2')
st.title('Chart Plotter')

excel_file = 'heart2.xlsx'
sheet_name = 'Worksheet'

global df 
df = pd.read_excel(excel_file, 
                   sheet_name=sheet_name,
                   header=0)

global numeric_columns
try:
    st.write(df)
    numeric_columns = list(df.select_dtypes(['float','int']).columns)
except Exception as e:
    print(e)
    
st.header("Scatterplots")
st.subheader("Scatterplots Settings")
try:
    x_values = st.selectbox('X axis', options=numeric_columns)
    y_values = st.selectbox('Y axis', options=numeric_columns) 
    plot = px.scatter(data_frame=df, x=x_values, y=y_values)

    st.plotly_chart(plot)
except Exception as e:
    print(e)

st.header("Violinplots")
st.subheader("Violinplots Settings")
try:
    entry_columns = [col for col in df.columns if df[col].nunique() <= 3]
    column_color = st.selectbox('Column Color', options=entry_columns)
    y_violin = st.selectbox(label = "Select y value for violin chart",
                            options = ["Age","Cholesterol","Oldpeak","MaxHR","RestingBP"])
    plot = px.violin(data_frame=df, x='HeartDisease', y= y_violin, color=column_color, title="Relationship between Old peak and getting Heart Disease", box=True)
    st.plotly_chart(plot)
except Exception as e:
    print(e)



st.header("Barplot")
chestpain = df['ChestPainType'].unique().tolist()
chestpain_selection = st.multiselect('Types of Chest Pain:',
                                     chestpain,
                                     default=chestpain)
heartdisease = df['HeartDisease'].unique().tolist()
heartdisease_selection = st.multiselect('Yes/No Heart Disease:',
                                     heartdisease,
                                     default=heartdisease)
mask = df['ChestPainType'].isin(chestpain_selection)
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

mask1 = df['HeartDisease'].isin(heartdisease_selection)
number_of_result = df[mask].shape[0]

df_grouped = df[mask][mask1].groupby(by=['ChestPainType']).count()[['HeartDisease']]

bar_chart = px.bar(
        df_grouped,
        x = 'HeartDisease',
        color = 'HeartDisease',
        color_continuous_scale = ['pink', 'blue'],
        template = 'plotly_white',
        title = 'Chance of getting Heart Disease of different Chest Pain Type'
    )

st.plotly_chart(bar_chart)



# ----- Sidebar 
with st.sidebar:
    container = st.container()
    all = st.checkbox(label = "Select all")

    if all:
        hd = container.multiselect(label = "Select Heart Disease status",
                                   options = df["HeartDisease"].unique(),
                                   default = df["HeartDisease"].unique())
    else:
        hd = container.multiselect(label = "Select Heart Disease status",
                                   options = df["HeartDisease"].unique())
    if not hd:
        st.error("Please select Heart Disease status")
    # hd = st.multiselect(
    #     label = "Select Heart Disease status",
    #     options = df["HeartDisease"].unique(),
    #     default = df["HeartDisease"].unique()
    # )

df_selection = df.query(
    "HeartDisease == @hd")

# ----- MaxHR vs HD density chart with binwidth slider
st.header("Histogram")
col1, col2 = st.columns(2)
with col1:
    bin_width = st.slider(label = "**Binwidth slider**",
                          min_value = 5, max_value = 30, step = 5)
    
with col2:
    color_selection = st.color_picker(label = "**Pick a chart color**", value = "#F7CAC9")
    st.write("Chart color is ", color_selection)

col3, col4 = st.columns(2)
with col3:
    opacity_selection = st.number_input(label = "**Input chart opacity**",
                                        min_value = 0.0,
                                        max_value = 1.0,
                                        value = 0.7,
                                        step = 0.05)

    x_selection = st.selectbox(label = "**Select x variable**",
                               options = ["RestingBP", "Cholesterol", "MaxHR"])
with col4:
     histnorm_selection = st.selectbox(label = "**Select type of chart normalization**",
                                    options = ["", "density", "percent", "probability density"])

st.markdown("##")

fig = go.Figure(data = [
    go.Histogram(
        x = df_selection["MaxHR"],
        histnorm = histnorm_selection,
        xbins = go.histogram.XBins(size = bin_width),
        marker = go.histogram.Marker(color = color_selection), 
        opacity = opacity_selection
    )])

fig.update_layout(yaxis_title = histnorm_selection, 
                 xaxis_title = x_selection)
st.write("**Distribution of**", x_selection)
st.write(fig)


