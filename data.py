import pandas as pd
import matplotlib.pyplot as plt
# warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
plt.style.use('seaborn-v0_8-whitegrid')
cbo_df = pd.read_csv('DSAS - CBO.csv')
restaurant_df = pd.read_csv('DSAS - Restaurant.csv')
meals_df = pd.read_csv('DSAS-Rethink_Meals_combined.csv')