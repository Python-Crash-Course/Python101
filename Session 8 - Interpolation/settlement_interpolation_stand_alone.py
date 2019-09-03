import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

### SET VERSION NUMBER ###
version_number = 'v1a'

### SET WHAT TO PLOT ###
plot_model_points = False
plot_known_points = True
plot_interpolated_points = True

### READ EXCEL FILE WITH SECTIONS AND KNOWN SETTLEMENT DATA ###
file_name = f'known_sections_plaxis_{version_number}.xlsx'
sheet_name = 'known_sections_plaxis'
df_x = pd.read_excel(file_name, sheet_name=sheet_name, skiprows=7, usecols=[1])
df_y = pd.read_excel(file_name, sheet_name=sheet_name, skiprows=7, usecols=[2,3,4,5])
df_z25 = pd.read_excel(file_name, sheet_name=sheet_name, skiprows=7, usecols=[6,7,8,9])
df_z26 = pd.read_excel(file_name, sheet_name=sheet_name, skiprows=7, usecols=[10,11,12,13])
df_z27 = pd.read_excel(file_name, sheet_name=sheet_name, skiprows=7, usecols=[14,15,16,17])

# Insert as many X-colunms as there are columns in the other dataframes
for i in range(2, len(df_y.columns)+1):
    df_x[f'X{i}'] = df_x['X']

# Flatten dataframe of y-values into array
y_temp = df_y.values.flatten()

# Get indecies where values are not NaN
idx = np.where(~np.isnan(y_temp))

# Extract all non-NaN values to create array of all known points
y_known = y_temp[idx]
x_known = df_x.values.flatten()[idx]
z25_vals = df_z25.values.flatten()[idx]
z26_vals = df_z26.values.flatten()[idx]
z27_vals = df_z27.values.flatten()[idx]


# Mirror all data, since everything is assumed symmetric about CL (only vals defined on one side)
x_known = np.append(x_known, x_known)
y_known = np.append(y_known, -y_known)
settlements_known = {'25': np.append(z25_vals, z25_vals),
                     '26': np.append(z26_vals, z26_vals),
                     '27': np.append(z27_vals, z27_vals)}

for lc, settlement_known in settlements_known.items():

    # FIXME A lot of stuff should go outside this loop!

    ### D-WALL NODES ###
    # Read data file for structural points and their coordinates (To get D-wall bottom points)
    dfp = pd.read_excel(f'structural_points_{version_number}.xlsx', sheet_name='XLSX-Export')

    # Remove leading or trailing white space from column names
    dfp.columns = dfp.columns.str.strip()

    # Extract D-wall bottom corner points to new dataframe
    df_dwalls_trumpet = dfp[(dfp['Text'] == 'Point') & (dfp['NR'] >= 808) & (dfp['NR'] <= 929)]
    df_dwalls_station1 = dfp[(dfp['Text'] == 'Point') & (dfp['NR'] >= 1021) & (dfp['NR'] <= 1047)]
    df_dwalls_station2 = dfp[(dfp['Text'] == 'Point') & (dfp['NR'] >= 1051) & (dfp['NR'] <= 1077)]
    df_dwalls = pd.concat([df_dwalls_trumpet, df_dwalls_station1, df_dwalls_station2], axis=0)

    # Gather corner points of D-walls (x, y, z) where settlement values will be interpolated
    x_dwalls, y_dwalls, z_dwalls = df_dwalls['X [m]'], df_dwalls['Y [m]'], -df_dwalls['Z [m]']
    node_no_dwalls = df_dwalls['NR']

    ### BASE SLAB NODES ###
    # Read file with base slab node numbers and their coordinates into a dataframe
    df_slabs = pd.read_excel(f'base_slab_nodes_{version_number}.xlsx', sheet_name='XLSX-Export')

    # Remove leading or trailing white space from column names
    df_slabs.columns = df_slabs.columns.str.strip()

    x_slabs, y_slabs, z_slabs = df_slabs['X [m]'], df_slabs['Y [m]'], df_slabs['Z [m]']
    node_no_slabs = df_slabs['NR']

    ### COMBINE BASE SLAB AND D-WALL DATA ###
    x_nodes = np.append(x_dwalls, x_slabs)
    y_nodes = np.append(y_dwalls, y_slabs)
    z_nodes = np.append(z_dwalls, z_slabs)
    node_no = np.append(node_no_dwalls, node_no_slabs)

    ### PERFORM INTERPOLATION ###
    # x-y coordinates of points with known displacements
    xy_known = np.array(list(zip(x_known, y_known)))    # FIXME SHould be outside loop

    # Calculate the interpolated z-values
    settlement_interpolated = griddata(xy_known, settlement_known, (x_nodes, y_nodes), method='linear')

    # Check if interpolated settlements have any nan values
    print('-------------------------------------------')
    print(f'LC{lc}:')
    if np.isnan(settlement_interpolated).any():
        print('    INFO:')
        print("    Some interpolated settlement values are 'nan'.")
        print('    This is probably beacause they fall out of the region defined by known points')
        print('    (extrapolation not suported).')
        nans = np.argwhere(np.isnan(settlement_interpolated))
        print(f'    Number of nan values are {len(nans)} out of {len(settlement_interpolated)} total values.')
        print(f'    X-values for points that failed to intepolate are:\n{x_nodes[nans.flatten()]}')
        # TODO: Replace those nan-values with 0 and make sure they are colored red in the plot

    else:
        print('    All values interpolated succesfully!')
    print('-------------------------------------------')


    ### WRITE INTERPOLATED FIELD TO .DAT FILE AS TEDDY CODE ###
    # Write Teddy code for applying interpolated settlements to file
    with open(f'teddy_code_settlement_field_LC{lc}_{version_number}.dat', 'w') as file:
    #     file.write('''+PROG SOFILOAD urs:47.8 $ Plaxis settlement
    # HEAD Plaxis settlement-LT (interp. all nodes)
    # UNIT TYPE 5
    #
    # LC 25 type 'P' fact 1.0 facd 0.0 titl 'LT settlement all nodes'  \n''')
        for node, settlement in zip(node_no, settlement_interpolated):
            file.write(f'  POIN NODE {node} WIDE 0 TYPE WZZ {settlement} \n')
        # file.write('END')


    ### PLOT KNOWN POINTS WITH INTERPOLATED FIELD ###
    # Check of any plot options are set to True
    if any([plot_model_points, plot_known_points, plot_interpolated_points]):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        if plot_model_points:
            # Plot structural points/nodes in the model
            ax.scatter(x_nodes, y_nodes, z_nodes, '.', s=0.1)                         # Base slabs
            ax.scatter(x_dwalls, y_dwalls, z_dwalls, '.', s=0.1, color='magenta')     # D-walls

        if plot_known_points:
            # Plot known settlement points
            ax.scatter(x_known, y_known, settlement_known, '-.', color='limegreen')

        if plot_interpolated_points:
            # Plot interpolated field
            ax.scatter(x_nodes, y_nodes, settlement_interpolated, '.', color='cornflowerblue', s=0.1)

        # Set limits
        # ax.set_xlim(6800, 7350)
        # ax.set_zlim(-22, -15)
        # ax.set_ylim(-100, 100)
        plt.show()
