import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Set name of Excel file to read
file_known = 'known_sections_plaxis.xlsx'

# Set name of sheet to read from Excel file
sheet_known = 'known_sections_plaxis'

# Read data from Excel sheet into a dataframe
df = pd.read_excel(file_known, sheet_name=sheet_known, skiprows=7)

# Extract columns whose names starts with a 'Y' into new dataframe of Y-coordinates
df_y = df[df.columns[df.columns.str.startswith('Y')]]

# Extract columns whose names starts with 'Z' into new dataframe of settlements
df_settlements_known = df[df.columns[df.columns.str.startswith('Z')]]

# Flatten dataframe values into 1D array
y_known = df_y.values.flatten()
settlements_known = df_settlements_known.values.flatten()

# Extract known x-values
x_known = df['X']

# Create X-array by repeating itself as many times as there are Y-columns
# This will create matching(x, y)-points between arrays x and y
x_known = np.repeat(x_known, len(df_y.columns))

# Set names and read Excel file with base slab nodes
file_nodes = 'base_slab_nodes.xlsx'
sheet_nodes = 'XLSX-Export'
df_nodes = pd.read_excel(file_nodes, sheet_name=sheet_nodes)

# Extract x- and y-coordinates of nodes
x_nodes = df_nodes['X [m]']
y_nodes = df_nodes['Y [m]']

# Extract node numbers
node_no = df_nodes['NR']

# Mirror known y-values and add corresponding x-values and settlements
x_known = np.append(x_known, x_known)
y_known = np.append(y_known, -y_known)
settlements_known = np.append(settlements_known, settlements_known)

# Arrange known (x, y) points to fit input for interpolation
xy_known = np.array(list(zip(x_known, y_known)))

# Perform interpolation calculation
settlements_interpolated = griddata(xy_known, settlements_known, (x_nodes, y_nodes), method='cubic')


####################
### Exercise 1.2 ###
####################
# Create figure object
fig = plt.figure()

# Create axis object for 3D plot
ax = fig.add_subplot(111, projection='3d')

# Plot known settlement points as 3D scatter plot (ax.scatter(...))
    # <Put plotting code here!>

# Plot interpolated field as 3D scatter plot
    # <Put plotting code here!>

# Show figure
    # <Put plotting code here!>


####################
### Exercise 1.3 ###
####################
# Write Sofistik input code to .dat-file for applying settlements as imposed displacements
    # <Put plotting code here!>
    
