import pandas as pd
import plotly.express as px

class Cleaned:
    def __init__(self):
        pass
    
    def load_data(self, path):
        # Import Data and Convert it into a DataFrame
        self.data = pd.read_csv(path)
        return self.data
        
    def fill_empty_data(self, data, column, value):
        # Fill empty values with a specific value
        pass
    
    def scatter_plot(self, data, x, y):
        # Create a scatter plot
        fig = px.scatter(data, x=x, y=y)
        return fig.show()