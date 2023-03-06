import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    # Title of the app
    st.title("Univariate Analysis App")
    st.write("**By:** A. Vera")

    st.write("""The Univariate Analysis App is designed to provide users with a quick and easy way to perform exploratory data analysis on a single variable in a dataset.""")
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the file and store it in a pandas dataframe
        df = pd.read_csv(uploaded_file)
        
        # Choose a column from the dataframe
        column = st.selectbox("Choose a column:", df.columns)
        
        if df[column].dtype == "object":
            # Show frequency distribution
            st.subheader("Frequency Distribution")
            st.write("The frequency distribution table shows the count of each unique value in the selected column. The relative frequency and cumulative relative frequency columns show the proportion of each value relative to the total number of values and the cumulative proportion of values, respectively.")
            freq_dist = df[column].value_counts().rename_axis("Unique Values").reset_index(name="Frequencies")
            freq_dist["Relative Frequencies"] = freq_dist["Frequencies"] / freq_dist["Frequencies"].sum()
            freq_dist["Cumulative Relative Frequencies"] = freq_dist["Relative Frequencies"].cumsum()
            st.write(freq_dist)
            
            # Show bar chart
            st.subheader("Bar Chart")
            st.write("The bar chart shows the distribution of the unique values in the selected column. The x-axis represents the unique values, and the y-axis represents the frequency count of each value.")
            fig, ax = plt.subplots()
            ax.bar(freq_dist["Unique Values"], freq_dist["Frequencies"])
            ax.tick_params(axis="x", rotation=45)
            st.pyplot(fig)
        else:
            # Ask the user if they want to treat the numerical variable as categorical
            is_categorical = st.checkbox("Treat as categorical")
            
            if is_categorical:
                # Treat the numerical variable as categorical
                bins = st.slider("Number of bins:", 1, 50, 10)
                df[column] = pd.cut(df[column], bins=bins, include_lowest=True)
                
                # Show frequency distribution
                st.subheader("Frequency Distribution")
                st.write("The frequency distribution table shows the count of values in each bin of the selected column. The relative frequency and cumulative relative frequency columns show the proportion of values in each bin relative to the total number of values and the cumulative proportion of values, respectively.")
                freq_dist = df[column].value_counts().sort_index().rename_axis("Unique Values").reset_index(name="Frequencies")
                freq_dist["Unique Values"] = freq_dist["Unique Values"].astype(str)
                freq_dist["Relative Frequencies"] = freq_dist["Frequencies"] / freq_dist["Frequencies"].sum()
                freq_dist["Cumulative Relative Frequencies"] = freq_dist["Relative Frequencies"].cumsum()
                st.write(freq_dist)
                
                # Show bar chart
                st.subheader("Bar Chart")
                st.write("The bar chart shows the distribution of values in each bin of the selected column. The x-axis represents the bins, and the y-axis represents the frequency count of values in each bin.")
                fig, ax = plt.subplots()
                ax.bar(freq_dist["Unique Values"], freq_dist["Frequencies"])
                ax.tick_params(axis="x", rotation=45)
                st.pyplot(fig)
            else:
                # Show descriptive statistics
                st.subheader("Descriptive Statistics")
                st.write("The descriptive statistics table shows the summary statistics of the selected column, including the count, mean, standard deviation, minimum value, 25th percentile, median, 75th percentile, and maximum value.")
                st.write(df[column].describe())

                # Show histogram
                st.subheader("Histogram")
                st.write("The histogram shows the distribution of the numerical values in the selected column. The x-axis represents the numerical range of values, and the y-axis represents the frequency count of values in each range.")
                fig, ax = plt.subplots()
                ax.hist(df[column], bins="auto")
                st.pyplot(fig)
            
                # Show boxplot
                st.subheader("Boxplot")
                st.write("The boxplot shows the distribution of the numerical values in the selected column. The box represents the interquartile range (IQR) between the 25th and 75th percentiles, and the whiskers represent the range of values within 1.5 times the IQR. Outliers are shown as dots beyond the whiskers.")
                fig, ax = plt.subplots()
                sns.boxplot(x=df[column])
                st.pyplot(fig)
            
                # Show density plot
                st.subheader("Density Plot")
                st.write("The density plot shows the distribution of the numerical values in the selected column. The x-axis represents the numerical range of values, and the y-axis represents the probability density of values in each range.")
                fig, ax = plt.subplots()
                sns.kdeplot(df[column], shade=True)
                st.pyplot(fig)

if __name__ == "__main__":
    main()