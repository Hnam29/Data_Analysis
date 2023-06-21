import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import requests 
import os 
from PIL import Image 
from io import BytesIO
from datetime import datetime
import time
from plotly import graph_objs as go
import graphviz
from annotated_text import annotated_text, annotation


#------------DRAFT (WITH BUTTONS)----------------------------------------------------
# def display_main_interface():
#     # Greeting when user first visit the web app
#     st.header("Welcome to Hector's Web App! Hope you find this suitable and informative to your need :sunglasses:")
#     col1, col2, col3 = st.columns(3)
#     # get the image source 
#     image = Image.open('/Users/vuhainam/Documents/PORTFOLIO_PROJECT_DA/survey.jpg')
#     # show the image
#     col3.image(image,
#                caption='Designed by internet, stolen by Hector :haha:',
#                use_column_width=True)
#     # upload the data
#     file_upload = st.file_uploader('Upload your file :vocano:')
#     # if file_upload is not None: 
#         # if os.path.splitext(file_upload)[1].lower() == '.xlsx':
#         #     st.write('Received an excel file!')
#         #     df = pd.read_excel(file_upload) 
#         #     st.write(df)
#         # elif os.path.splitext(file_upload)[1].lower() == 'csv':
#         #     st.write('Received a CSV file!')
#         #     df = pd.read_csv(file_upload)
#         #     st.write(df)
#         # else:
#         #     st.write('Cannot interpret the origin of file uploaded')
#     if file_upload:
#         df = pd.read_csv(file_upload) 
#         st.write("CSV file uploaded and processed successfully!")
#         st.write(df)

#     # if st.button('Click here to go back to the greeting'):
#     #     display_greeting()

# def display_greeting():
#     st.write("Welcome to your app!")
#     if st.button('Click here to access the main interface'):
#         display_main_interface()

# # Main program 
# if __name__ == '__main__':
#     display_greeting()
#----------------------------------------------------------------

# FUNCTIONS 
@st.cache_resource

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def process_file(file):
    file_type = None
    try:
        # Convert file to dataframe
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
            file_type = 'xlsx'
        elif file.name.endswith('.csv'):
            df = pd.read_csv(file)
            file_type = 'csv'
        else:
            st.error("Invalid file type. Expected CSV or XLSX file.")
            return 'Please upload the file', 'Please upload the file'

        # Process the dataframe
        # ...

        # Return the dataframe and file type
        return df, file_type
        
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None, None


# ----------------ANALYSIS--------------------

def show_columns_info(df):
    c1, c2, c3, c4 = st.columns(4)
    c1.write("Columns Names")
    c1.write(df.columns)
    c2.write("Columns Data Types")
    c2.write(df.dtypes)
    c3.write("Missing Values")
    c3.write(df.isnull().sum())
    c4.write("Unique Values")
    c4.write(df.nunique())



# def show_missing_values(df):
#     #col1 = st.beta_column()
#     c3.write("Missing Values")
#     c3.write(df.isnull().sum())

# def show_unique_values(df):
#     #col2 = st.beta_column()
#     c4.write("Unique Values")
#     c4.write(df.nunique())

def show_standard_deviation(df):
    #col1 = st.beta_column()
    st.write("Standard Deviation")
    st.write(df.std(numeric_only=True))

def show_data_shape(df):
    #col1, col2 = st.beta_columns(2)
    st.write("Number of rows")
    st.write(df.shape[0])
    st.write("Number of columns")
    st.write(df.shape[1])

def show_data_correlation(df):
    #col1 = st.beta_column()
    st.write("Data Correlation")
    st.write(df.corr(numeric_only=True))

def filter_rows(df):
    
    column_name = st.selectbox("Select a column to filter", df.columns)
    value = st.text_input("Enter the filter value")
    # Filter the rows based on the converted column
    if value == "":
        filtered_data = df[df[column_name].isnull()]
    elif df[column_name].dtype == 'float':
          filtered_data = df[df[column_name] >= float(value)]
    else:      
        filtered_data = df[df[column_name].astype(str).str.contains(value, case=False)]
    st.write("Filtered Data")
    st.write(filtered_data)   



def analyze_data(df):
    
    set_header(df)
    delete_column(df)
    show_overall_file(df)
    # st.write("#### Select Columns")
    all_columns = df.columns.tolist()
    options_key = "_".join(all_columns)
    selected_columns = st.multiselect("Select columns for analyzing", options=all_columns)
    
    if selected_columns:
        sub_df = df[selected_columns]
        st.write("### Sub DataFrame")
        st.write(sub_df.head())
        c1, c2 = st.columns(2)
        c1.write("Description")
        c1.write(sub_df.describe())
        c2.write("Data Rank")
        c2.write(sub_df.rank())

        st.sidebar.header("Data Sorted")
        sort_column = st.selectbox("Select column for sorting", sub_df.columns)
        sorted_df = sub_df.sort_values(by=sort_column)
        st.write(sorted_df)

        show_columns_info(sub_df)
        # show_missing_values(sub_df)
        # show_unique_values(sub_df)
        show_standard_deviation(sub_df)
        show_data_shape(sub_df)
        show_data_correlation(sub_df)
        filter_rows(sub_df)

    else:
        st.warning("Please select at least one column.")


# --------SET HEADER-----------
# def set_header(df):
#     if st.button('Update first row as header'):
#         df = df.rename(columns=df.iloc[0]).drop(df.index[0])
#         st.write(df)

def set_header(df):
    if st.button('Update first row as header'):
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        st.write(df)

    ## 1st way
    # button = st.button("Update first row as header")

    # Define a state variable to keep track of whether the button has been clicked
    # button_clicked = False

    # Define what happens when the button is clicked
    # if button:
    #     if not button_clicked:
    #         # Action to be taken on first click
    #         df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    #         st.write(df)
    #         button_clicked = True
    #     else:
    #         # Action to be taken on second click
    #         button_clicked = False
    
    # # 2nd way
    # button = st.button("Update first row as header")
    # if button:
    #     df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    #     st.session_state.response_data = df
    #     st.write(st.session_state.response_data)
    # else:
    #     st.session_state.response_data = None


# the `all_columns` variable is defined after the 'delete_column' function is called, 
# so it will be updated with the new column list after the column is dropped.
def delete_column(df):
    selected_column = st.selectbox('Select a column to drop', df.columns)
    # drop the column if the user selected one
    if st.button('Drop column'):
        df.drop(selected_column, axis=1,inplace=True)
        st.write(df)

def show_overall_file(df):
    col_overall1, col_overall2 = st.columns([5,5])
    col_overall1.write("File Header")
    col_overall1.write(df.head())
    col_overall2.write("File Footer")
    col_overall2.write(df.tail())


# ----------------VISUALIZATION--------------------
def line_chart(sub_df, x_col, y_col, x_label, y_label):

    st.header('Line chart')

    # col_legend = st.sidebar.selectbox('Select column as legend',sub_df.columns,key='color_name')
    # if col_legend:
    #     fig = px.line(sub_df, x=x_col, y=y_col,color=col_legend,labels={'x': x_label, 'y': y_label})
    #     st.plotly_chart(fig)
    # else: 
    #     fig = px.line(sub_df, x=x_col, y=y_col,labels={'x': x_label, 'y': y_label})
    #     st.plotly_chart(fig)
    fig = px.line(sub_df, x=x_col, y=y_col)
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    st.plotly_chart(fig)
        
def multi_line_chart(sub_df, x_col, y_columns, x_label, y_label):

    st.header('Multiple line chart')
    for col in y_columns:
        fig = px.line(sub_df, x=x_col, y=col)
        fig.update_layout(xaxis_title=x_label, yaxis_title=y_label, title=col)
        st.plotly_chart(fig)


# def bar_chart(sub_df, x_min, x_max, y_min, y_max, x_col, y_col, x_label, y_label):

#     st.header('Bar chart')
#     fig = px.bar(sub_df, x=x_col, y=y_col)
#     fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
#     fig.update_x_axes(range=[x_min,x_max])
#     fig.update_y_axes(range=[y_min,y_max])
#     st.plotly_chart(fig)
# def bar_chart(sub_df, x_min, x_max, y_min, y_max, x_col, y_col, x_label, y_label):
def bar_chart(sub_df, y_min, y_max, x_col, y_col, color_col, af_col, ag_col, x_label, y_label):
    st.header('Bar chart')
    fig = px.bar(sub_df, x=x_col, y=y_col, color=color_col, animation_frame=af_col, animation_group=ag_col)
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label,width=900)
    # fig.update_xaxes(range=[float(x_min),float(x_max)])
    fig.update_yaxes(range=[float(y_min),float(y_max)])
    st.plotly_chart(fig)
   
def scatter_plot(sub_df, x_col, y_col, color_col, col_for_size, slider, x_min, x_max, y_min, y_max, x_label, y_label):
    st.header('Scatter Plot')
    #fig = px.scatter(sub_df, x=x_col, y=y_col)
    fig = px.scatter(sub_df, x=x_col, y=y_col, size=col_for_size, color=color_col, hover_name= color_col, size_max=slider, range_x=[x_min,x_max],range_y=[y_min,y_max])
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label,width=900)
    st.plotly_chart(fig)
   
def histogram_plot(sub_df, x_col, y_col, x_label, y_label):
    st.header('Histogram Plot')
    fig = px.histogram(sub_df, x=x_col, y=y_col)
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    st.plotly_chart(fig)
   
def pie_plot(sub_df, x_col, y_col, x_label, y_label):
    st.header('Pie Plot')
    fig = px.pie(sub_df, values=y_col, names=x_col)
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    st.plotly_chart(fig)

# def heat_map(sub_df, x_col, y_col, x_label, y_label):
#     st.header('Heat Map')
#     fig = px.imshow(sub_df.corr())
#     fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
#     st.plotly_chart(fig)

def heat_map(sub_df, x_col, y_col, x_label, y_label):
    st.header('Heat Map')
    fig = px.imshow(sub_df.corr(), x=list(sub_df.columns), y=list(sub_df.columns[::-1]), color_continuous_scale='viridis')
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    st.plotly_chart(fig)


# def heat_map(sub_df, x_col, y_col, x_label, y_label, color_scale='viridis'):
#     st.header('Heat Map')
#     fig = px.imshow(sub_df.corr(), x=list(sub_df.columns), y=list(sub_df.columns[::-1]), color_continuous_scale=color_scale)
#     fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)

#     # Create the color scale bar
#     color_scale_bar = px.imshow([[0, 1]], labels=dict(x=''), color_continuous_scale=color_scale)
#     color_scale_bar.update_layout(
#         width=50, height=350, margin={"r":0,"t":0,"l":0,"b":0},
#         coloraxis=dict(colorbar=dict(lenmode='fraction', len=0.6, yanchor='middle', y=0.5, thickness=15, tickvals=[0, 1], ticktext=[f"{sub_df.corr().values.min():.2f}", f"{sub_df.corr().values.max():.2f}"], ticks='outside'))
#     )
#     # Add the color scale bar to the heatmap figure
#     fig.add_trace(color_scale_bar.data[0])
#     st.plotly_chart(fig)

# def heat_map(sub_df, x_col, y_col, x_label, y_label, color='#ff4466'):
#     st.header('Heat Map')
#     fig = px.imshow(sub_df.corr(), x=list(sub_df.columns), y=list(sub_df.columns[::-1]), color_continuous_scale=[[0, color], [1, color]])
#     fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
#     st.plotly_chart(fig)

def box_plot(sub_df, x_col, y_col, x_label, y_label):
    st.header('Box Plot')
    fig = px.box(sub_df, x=x_col, y=y_col)
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    st.plotly_chart(fig)


# ----------------SCRAPING DATA FROM YOUTUBE--------------------
def get_video_details(video_id):

    #collecting view, like, dislike, comment counts
    url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+api_key
    response_video_stats = requests.get(url_video_stats).json()

    view_count = response_video_stats['items'][0]['statistics']['viewCount']
    like_count = response_video_stats['items'][0]['statistics']['likeCount']
    favorite_count = response_video_stats['items'][0]['statistics']['favoriteCount']
    comment_count = response_video_stats['items'][0]['statistics']['commentCount']

    return view_count, like_count, favorite_count, comment_count

def get_videos(df):
    pageToken = ""
    while 1:
        url = "https://www.googleapis.com/youtube/v3/search?key="+api_key+"&channelId="+channel_id+"&part=snippet,id&order=date&maxResults=10000&"+pageToken

        response = requests.get(url).json()
        time.sleep(1) #give it a second before starting the for loop
        for video in response['items']:
            if video['id']['kind'] == "youtube#video":
                video_id = video['id']['videoId']
                video_title = video['snippet']['title']
                video_title = str(video_title).replace("&","")
                upload_date = video['snippet']['publishedAt']
                upload_date = str(upload_date).split("T")[0]

                view_count, like_count,favorite_count, comment_count = get_video_details(video_id)

                # df = df.append({'video_id':video_id,'video_title':video_title,
                #                 "upload_date":upload_date,"view_count":view_count,
                #                 "like_count":like_count,
                #                 "comment_count":comment_count},ignore_index=True)

                col_row = pd.Series(data={'video_id':video_id,'video_title':video_title,
                                          'upload_date':upload_date,'view_count':view_count,
                                          'like_count':like_count,'favorite_count':favorite_count,
                                          'comment_count':comment_count})
                df = pd.concat([df,col_row.to_frame().T], ignore_index=True)
        try:
            if response['nextPageToken'] != None: #if none, it means it reached the last page and break out of it
                pageToken = "pageToken=" + response['nextPageToken']

        except:
            break

    return df

#----------------------------------------------------------------
# def main():

# Greeting when user first visit the web app
column_greeting1,column_greeting2,column_greeting3 = st.columns([1,100,1])
column_greeting2.header("Welcome to Hector's Web App! Hope you find it suitable and informative :bar_chart:")

# Decoration: indicate the time user interact 
now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
current_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
column_greeting2.write(f'First login at: {current_datetime} :volcano:')

# divider
st.divider()

# Decoration: get the image source 
image = Image.open('survey.jpg')
image1 = Image.open('da_image1.jpeg')
image2 = Image.open('da_image2.jpeg')
image3 = Image.open('da_process.jpeg')

st.sidebar.image(image, width=200)
with st.sidebar:
    option = st.radio('Choose a method :warning:',
             ('Data Analysis📈', 'Data Visualization📊', 'Data Storytelling📶', 'Data Scraping🤖'))
column_header1, column_header2, column_header3 = st.columns([3,5,3])
column_header2.header(option) 


col1, col2 = st.columns([3,1])
# Decoration: show the image
# col2.image(image,
#             caption='Designed by internet, stolen by Hector',
#             use_column_width=True)

# Decoration: A warning bar 
# st.info('Made by "st.info"', icon="ℹ️")

# ------ EXPLORATORY DATA ANALYSIS 
# LOAD: Upload the data
# file_upload = st.file_uploader('Upload your file :sparkles:')
# if file_upload is not None:
#     df, file_type = process_file(file_upload)
#     if df is not None:
#         st.write(f"File type: {file_type}")
#         col1.write(df)


#---------------------DATA ANALYSIS-------------------

if option == 'Data Analysis📈':
    col1, col2 = st.columns([5,3])
    file_upload = col1.file_uploader('Upload your file :sparkles:')
    col2.image(image1,
            caption='observed by HECTOR',
            use_column_width=True)
    df = pd.DataFrame()
    if file_upload is not None:
        df, file_type = process_file(file_upload)
        if df is not None:
            st.write(f"File type: {file_type}")
            col1.write(df)
    if df is not None:
        # if st.button('Click here to update header by first row'):
        #     set_header(df)
        analyze_data(df)

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='data_from_streamlit.csv',
        mime='text/csv',
    )

#---------------------DATA VISUALIZATION-------------------

# when creating a function to generate charts, we need to specify
# type of chart -> prerequisite params related to that type -> 
if option == 'Data Visualization📊':
    col1, col2 = st.columns([5,3])
    file_upload = col1.file_uploader('Upload your file :chart:')
    col2.image(image2,
            caption='depicted by HECTOR',
            use_column_width=True)
    if file_upload is not None:
        df, file_type = process_file(file_upload)
        if df is not None:
            choices = st.sidebar.radio('Select charts:', options=['Line Graph','Bar Chart','Scatter Plot','Histogram','Pie Chart','Heatmap','Box Plot'])
            col1.header(choices)
            if 'Line Graph' in choices:
                st.info('Line chart is great for visualizing trends over time or any ordered data on a continuous scale',icon="ℹ️")
                line_option = st.sidebar.radio('Single or Multiple',options=['1','many'])
                if line_option == '1':
                    st.sidebar.title('Chart options:')
                    # st.write('### Select columns')
                    all_cols = df.columns.tolist()
                    # options_key = '_'.join(all_cols)
                    selected_cols = st.sidebar.multiselect('### Select columns',options=all_cols)
                    if selected_cols:
                        sub_df = df[selected_cols]

                        x_col = st.sidebar.selectbox('Select x column:',sub_df.columns)
                        y_col = st.sidebar.selectbox('Select y column:',sub_df.columns)

                        x_label = st.sidebar.text_input('Enter the x label:')
                        y_label = st.sidebar.text_input('Enter the y label:')
                        line_chart(sub_df, x_col, y_col, x_label, y_label)
                
                if line_option == 'many':
                    st.sidebar.title('Chart options:')
                    # st.write('### Select columns')
                    all_cols1 = df.columns.tolist()
                    # options_key = '_'.join(all_cols)
                    selected_cols1 = st.sidebar.multiselect('### Select columns',options=all_cols1)
                    # selected_cols = list(selected_cols)
                    if selected_cols1:
                        sub_df = df[selected_cols1]

                        x_col = st.sidebar.selectbox('Select x column:',sub_df.columns)
                        y_cols = st.sidebar.multiselect('Select y columns:',sub_df.columns,default=sub_df.columns[1:])

                        x_label = st.sidebar.text_input('Enter the x label:')
                        y_label = st.sidebar.text_input('Enter the y label:')
                        multi_line_chart(sub_df, x_col, y_cols, x_label, y_label)


            if 'Bar Chart' in choices:
                    st.info('Bar chart is ideal for comparing categorical data between different groups or categories',icon="ℹ️")
                    st.sidebar.title('Chart options:')
                    # st.write('### Select columns')
                    all_cols = df.columns.tolist()
                    # options_key = '_'.join(all_cols)
                    selected_cols = st.sidebar.multiselect('### Select columns',options=all_cols)
                    if selected_cols:
                        sub_df = df[selected_cols]
                        numeric_cols = df.select_dtypes(include=['int', 'float']).columns
                        selected_num_cols = st.sidebar.multiselect('Select numeric columns:', options=numeric_cols)
                        num_df = df[selected_num_cols]

                        # x_col = st.sidebar.selectbox('Select x column:',sub_df.columns)
                        # y_col = st.sidebar.selectbox('Select y column:',sub_df.columns)

                        # x_min = st.sidebar.number_input('Enter the min value of x:',min_value=min(sub_df[x_col]),max_value=max(sub_df[x_col]),value=min(sub_df[x_col]))
                        # x_max = st.sidebar.number_input('Enter the max value of x:',min_value=min(sub_df[x_col]),max_value=max(sub_df[x_col]),value=max(sub_df[x_col]))
                        # y_min = st.sidebar.number_input('Enter the min value of y:',min_value=min(sub_df[y_col]),max_value=max(sub_df[y_col]),value=min(sub_df[y_col]))
                        # y_max = st.sidebar.number_input('Enter the max value of y:',min_value=min(sub_df[y_col]),max_value=max(sub_df[y_col]),value=max(sub_df[y_col]))

                        # x_label = st.sidebar.text_input('Enter the x label:')
                        # y_label = st.sidebar.text_input('Enter the y label:')
                        # bar_chart(sub_df, x_min, x_max, y_min, y_max, x_col, y_col, x_label, y_label)
                       
                        x_col = st.sidebar.selectbox('Select x column:', sub_df.columns)
                        default_x_col = sub_df.columns.get_loc(x_col)   # transform 'x_col' from STRING to COLUMN in DATAFRAME
                        x_value_option = sub_df[x_col].unique().tolist()
                        x_value = st.selectbox('Which x value do you want to get',x_value_option)   # CATEGORICAL VALUE
                        y_col = st.sidebar.selectbox('Select y column:', num_df.columns)
                        y_value_option = num_df[y_col].unique().tolist()
                        # y_value = st.selectbox('Which y value do you want to get',y_value_option)  # NUMERICAL VALUE

                        color_col = st.sidebar.selectbox('Select column as legend',sub_df.columns)
                        af_col = st.sidebar.selectbox('Should be "DateTime"',sub_df.columns)
                        ag_col = st.sidebar.selectbox('Should be the same as X axis',sub_df.columns,index=default_x_col)

                        # x_min = st.sidebar.number_input('Enter the minimum x value:', min_value=float(min(sub_df[x_col])), max_value=float(max(sub_df[x_col])), value=float(min(sub_df[x_col])))
                        # x_max = st.sidebar.number_input('Enter the maximum x value:', min_value=float(min(sub_df[x_col])), max_value=float(max(sub_df[x_col])), value=float(max(sub_df[x_col])))
                        # y_min = st.sidebar.number_input('Enter the minimum y value:', min_value=float(min(sub_df[y_col])), max_value=float(max(sub_df[y_col])), value=float(min(sub_df[y_col])))
                        # y_max = st.sidebar.number_input('Enter the maximum y value:', min_value=float(min(sub_df[y_col])), max_value=float(max(sub_df[y_col])), value=float(max(sub_df[y_col])))

                        # y_min = st.sidebar.number_input('Enter the minimum y value:', min_value=float(sub_df[y_col]), value=float(sub_df[y_col]))  # ERROR
                        # y_max = st.sidebar.number_input('Enter the maximum y value:', max_value=float(sub_df[y_col]), value=float(sub_df[y_col]))  # ERROR

                        # y_min = st.sidebar.number_input('Enter the minimum y value:', min_value=min(num_df[y_col]), value=min(num_df[y_col]))
                        # y_max = st.sidebar.number_input('Enter the maximum y value:', max_value=max(num_df[y_col]), value=max(num_df[y_col]))

                        y_min = st.sidebar.number_input('Enter the minimum y value:', value=min(num_df[y_col]))
                        y_max = st.sidebar.number_input('Enter the maximum y value:', value=max(num_df[y_col]))

                        x_label = st.sidebar.text_input('Enter the x label:')
                        y_label = st.sidebar.text_input('Enter the y label:')

                        # bar_chart(sub_df, x_min, x_max, y_min, y_max, x_col, y_col, x_label, y_label)
                        bar_chart(sub_df, y_min, y_max, x_col, y_col, color_col, af_col, ag_col, x_label, y_label)



            if 'Scatter Plot' in choices:
                    st.info('Scatter plot is not a good choice for categorical variables',icon="ℹ️")
                    st.sidebar.title('Chart options:')
                    # st.write('### Select columns')
                    all_cols = df.columns.tolist()
                    # options_key = '_'.join(all_cols)
                    selected_cols = st.sidebar.multiselect('### Select columns',options=all_cols)
                    if selected_cols:
                        sub_df = df[selected_cols]
                        numeric_cols = df.select_dtypes(include=['int','float']).columns
                        selected_num_cols = st.sidebar.multiselect('Select numeric columns:',options=numeric_cols)
                        num_df = df[selected_num_cols]

                        x_col = st.sidebar.selectbox('Select x column:',num_df.columns)
                        y_col = st.sidebar.selectbox('Select y column:',num_df.columns)
                        color_col = st.sidebar.selectbox('Select column as legend:',sub_df.columns)
                        col_for_size = st.sidebar.selectbox('Select column for size param:',num_df.columns)
                        slider = st.sidebar.slider('Customize the size of bubble that you want:',1,100,55)

                        x_min = st.sidebar.number_input('Enter the minimum x value:',value=min(num_df[x_col]))
                        x_max = st.sidebar.number_input('Enter the maximum x value:',value=max(num_df[x_col]))
                        y_min = st.sidebar.number_input('Enter the minimum y value:',value=min(num_df[y_col]))
                        y_max = st.sidebar.number_input('Enter the maximum y value:',value=max(num_df[y_col]))

                        x_label = st.sidebar.text_input('Enter the x label:')
                        y_label = st.sidebar.text_input('Enter the y label:')
                        scatter_plot(sub_df, x_col, y_col, color_col, col_for_size, slider, x_min, x_max, y_min, y_max, x_label, y_label)


            if 'Histogram' in choices:
                    st.info('Histogram is a dominant tool for visualizing data distribution in a continuous variable',icon="ℹ️")
                    st.sidebar.title('Chart options:')
                    st.sidebar.markdown('(Already filtering to only numerical columns)')
                    # st.write('### Select columns')
                    # all_cols = df.columns.tolist() # FOR BOTH NUMERICAL & CATEGORICAL
                    numeric_cols = df.select_dtypes(include=['int','float']).columns  # ONLY FOR NUMERICAL
                    # options_key = '_'.join(all_cols)
                    selected_cols = st.sidebar.multiselect('### Select columns',options=numeric_cols)
                    if selected_cols:
                        sub_df = df[selected_cols]

                        x_col = st.sidebar.selectbox('Select x column:',sub_df.columns)
                        y_col = st.sidebar.selectbox('Select y column:',sub_df.columns)

                        x_label = st.sidebar.text_input('Enter the x label:')
                        y_label = st.sidebar.text_input('Enter the y label:')
                        histogram_plot(sub_df, x_col, y_col, x_label, y_label)


            if 'Pie Chart' in choices:
                    st.info('Pie chart is an engaging way to visualize data that is classified into different categories',icon="ℹ️")
                    st.sidebar.title('Chart options:')
                    # st.write('### Select columns')
                    all_cols = df.columns.tolist()
                    # options_key = '_'.join(all_cols)
                    selected_cols = st.sidebar.multiselect('### Select columns',options=all_cols)
                    if selected_cols:
                        sub_df = df[selected_cols]

                        x_col = st.sidebar.selectbox('Select x column:',sub_df.columns)
                        y_col = st.sidebar.selectbox('Select y column:',sub_df.columns)

                        x_label = st.sidebar.text_input('Enter the x label:')
                        y_label = st.sidebar.text_input('Enter the y label:')
                        pie_plot(sub_df, x_col, y_col, x_label, y_label)


            if 'Heatmap' in choices:
                    st.info('Heat map is a graphing technique to visualize the volume of locations/events within a dataset',icon="ℹ️")
                    st.sidebar.title('Chart options:')
                    st.sidebar.markdown('(Already filtering to only numerical columns)')
                    # st.write('### Select columns')
                    # all_cols = df.columns.tolist() # FOR BOTH NUMERICAL & CATEGORICAL
                    numeric_cols = df.select_dtypes(include=['int','float']).columns  # ONLY FOR NUMERICAL
                    # options_key = '_'.join(all_cols)
                    selected_cols = st.sidebar.multiselect('### Select columns',options=numeric_cols)
                    if selected_cols:
                        sub_df = df[selected_cols]

                        x_col = st.sidebar.selectbox('Select x column:',sub_df.columns)
                        y_col = st.sidebar.selectbox('Select y column:',sub_df.columns)

                        x_label = st.sidebar.text_input('Enter the x label:')
                        y_label = st.sidebar.text_input('Enter the y label:')
                        heat_map(sub_df, x_col, y_col, x_label, y_label)
                        # color = st.color_picker('Pick a color', '#ff4466')
                        # heat_map(sub_df, x_col, y_col, x_label, y_label, color)
                        # heat_map(sub_df, x_col, y_col, x_label, y_label, color_scale='YlOrRd')


            if 'Box Plot' in choices:
                    st.info('Box plot is conveying the distribution of a dataset and identifying outliers or anomalies',icon="ℹ️")
                    st.sidebar.title('Chart options:')
                    # st.write('### Select columns')
                    all_cols = df.columns.tolist()
                    # options_key = '_'.join(all_cols)
                    selected_cols = st.sidebar.multiselect('### Select columns',options=all_cols)
                    if selected_cols:
                        sub_df = df[selected_cols]

                        x_col = st.sidebar.selectbox('Select x column:', sub_df.columns)
                        y_col = st.sidebar.selectbox('Select y column:', sub_df.columns)

                        x_label = st.sidebar.text_input('Enter the x label:')
                        y_label = st.sidebar.text_input('Enter the y label:')

                        box_plot(sub_df, x_col, y_col, x_label, y_label)

#---------------------DATA STORYTELLING-------------------

if option == 'Data Storytelling📶':
    col_dst1, col_dst2 = st.columns([7,3])
    col_dst2.image(image3,
            caption='Source: internet..',
            use_column_width=True)

    annotated_text(
            "This is a   ",
            annotation("DATA", "ANALYTICS", font_family="Comic Sans MS", border="2px dashed blue"),
            " field that consists of technical skills:  ",
            ("Data","Cleaning"),
            ("Data","Wrangling"),
            ("Data","Mining"),
            ("Data","Manipulating/Munging. \n"),
            " \n\n Besides,",
            ("Data", "Warehousing"),
            ("Data", "Modeling"),
            "and also",
            ("Data", "Visualization"),
            "play important roles in making a data analyst. ",
            " \n Here's a quote for you, warrior: ",
            annotation("DATA", "ANALYST", font_family="Comic Sans MS", border="3px dotted red"),
            "turns raw data into valuable insights, unlocking the secrets hidden within the numbers.",
        )    

    col_dst1.graphviz_chart('''
    digraph {
        graph[width=500, height=500];
        raw_data -> d_scraping
        d_scraping -> dataset
        dataset -> database
        database -> ETL
        ETL -> d_analysis
        d_analysis -> d_visual
        d_visual -> d_storytell
        d_storytell -> descriptive_what_happened
        d_storytell -> predictive_30p_true
        database -> m_learning
        d_scraping -> m_learning
        m_learning -> predictive_70p_true
    }
''',use_container_width=True)
    # file_upload = col_dst1.file_uploader('Upload your file :chart:')
    # if file_upload is not None:
    #     # Process the file and extract the selected column
    #     df, file_type = process_file(file_upload)
    #     if df is not None:
    #         col = df.columns.tolist()
    #         selected_col = st.sidebar.selectbox('Select a column', options=col)
    #         if selected_col:
    #             sub_df = df[[selected_col]]
    #             sub_df[selected_col].apply(lambda x: st.progress(x / 1000))
#-----------------------DATA SCRAPING----------------------

# def fetch_github_api():       (EXAMPLE)
#     response = requests.get('https://api.github.com').json()
#     return response

if option.endswith('🤖'):
#if option == 'Data Scraping🤖':
    # if st.button("Click me"):
    #     response = requests.get('https://api.github.com').json()
    #     st.write(response)
    # Get or create our session state object to store the response data
    api_key = st.text_input('Type your API key:')
    channel_id = st.text_input('Type the channel ID:')
    col_ds1, col_ds2, col_ds3 = st.columns([2,3,10])
    if 'response_data' not in st.session_state:
        st.session_state.response_data = None

    if col_ds1.button("Click me"):
        # Fetch the API data and store it in our session state object
        # (EXAMPLE)st.session_state.response_data = fetch_github_api()
        st.session_state.response_data = get_videos(df)
        st.write(st.session_state.response_data)

    if col_ds2.button("Clear Response"):
        # Clear the response data from our session state object
        st.session_state.response_data = None

    if api_key is not None and channel_id is not None:
        data_from_web = pd.DataFrame(columns=["video_id","video_title","upload_date","view_count","like_count","favorite_count","comment_count"])
        data_from_web = get_videos(data_from_web)
        st.write(data_from_web.head())















# with st.sidebar:
#     option = st.radio('Choose a method :chart:',
#              ('Descriptive Analytics', 'Diagnostic Analytics', 'Predictive Analytics', 'Prescriptive Analytics'))
    
# st.header(option)       # header = option name that choose

# # global function
# # def on_file_upload(file):                  # fix 1
# #     # Do something with the uploaded file
# #     print(f"Received a new file: {file.name}")

# if option == 'Descriptive Analytics': 
#     DA1 = st.sidebar.selectbox('Which dashboard you want to make?',
#                                    ('a','b','c','d'))
#     if DA1 == 'a':
#         st.write('Done')
#     if DA1 == 'b':
#         c1, c2 = st.columns((6,4))
#         with c1:
#             st.write('Occupying 60% of the width :uk:')
        
#         with c2: 
#             st.write('Occupying 40% of the width :flag-vn:')



#    instructionCol, buttonCol = st.columns([4,1])
#     with instructionCol:
#         with st.expander("Instructions"):
#             st.write("Pretend these are the instructions.")
#     with buttonCol:
#         st.button("\nRestart\n", on_click=board.reset)

# if __name__ == "__main__":
#     main()
