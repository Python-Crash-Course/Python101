

# Compute distance from point (2, 5) to point (3, 4)
x1, y1, x2, y2 = 2, 5, 3, 4
dist1 = ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)

# Compute distance from point (7, 6) to point (3, 5)
x1, y1, x2, y2 = 7, 6, 3, 5
dist2 = ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)

# Compute distance from point (2, 4) to point (7, 5)
x1, y1, x2, y2 = 2, 4, 7, 5
dist3 = ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)


# Same lines are repeated many times   ==>   Hard to maintain or change   ==>   create a function

# ------------------------------------------------

# Same code as above:
def points_dist(x1, y1, x2, y2):
    '''Compute the distance between two points (x1, y1) and (x2, y2)'''
    return ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)

# Calculate the distances by function calls
dist1 = points_dist(2, 5, 3, 4)
dist2 = points_dist(7, 6, 3, 5)
dist3 = points_dist(2, 4, 7, 5)

# -----------------------------------------------
# Alternative by function and list comprehension
xx1 = [2, 7, 2]
yy1 = [5, 6, 4]
xx2 = [3, 3, 7]
yy2 = [4, 5, 5]

distances = [points_dist(xx1[i], yy1[i], xx2[i], yy2[i]) for i in range(len(xx1))]
print(distances)

# -----------------------------------------------
# Alternative with list comprehension and zip
distances2 = [points_dist(x1, y1, x2, y2) for i in zip(xx1, yy1, xx2, yy2)]
print(distances)


def polygon_area(xv, yv, signed=False):
    ''' Return the area of a non-self-intersecting polygon given the coordinates of its vertices'''

    # Perform shoelace multiplication
    a1 = [xv[i] * yv[i+1] for i in range(len(xv)-1)]
    a2 = [yv[i] * xv[i+1] for i in range(len(yv)-1)]

    # Check is area should be signed and return area
    if signed:          # <--- Same as "if signed == True:"
        return 1/2 * ( sum(a1) - sum(a2) )
    else:
        return 1/2 * abs( sum(a1) - sum(a2) )



def polygon_centroid(x, y):

    # Initialize empty lists for holding summation terms
    cx, cy = [], []

    # Loop over vertices and put the summation terms in the lists
    for i in range(len(x)-1):

        # Compute and append summation terms to each list
        cx.append((x[i] + x[i+1]) * (x[i] * y[i+1] - x[i+1] * y[i]))
        cy.append((y[i] + y[i+1]) * (x[i] * y[i+1] - x[i+1] * y[i]))

    # Calculate the signed polygon area by calling already defined function
    A = polygon_area(x, y, signed=True)

    # Sum summation terms and divide by 6A to get coordinates
    Cx = sum(cx) / (6*A)
    Cy = sum(cy) / (6*A)

    return Cx, Cy



def plot_polygon(xv, yv, plot_centroid=True):
    '''Plot the polygon with the specified vertex coordinates.

    The plot is created with legend and the computed area of the
    polygon shown in the title. The plots shows the centroid of
    the polygon, but this can be turned off by setting
    plot_centroid=False.

    Args:
        xv (list)            : x-coordinates of polygon vertices
        yv (list)            : y-coordinates of polygon vertices
        plot_centroid (bool) : Plot centroid of polygon (Cx, Cy).
                               Defaults to plotting the centroid.
    '''

    # Compute area of polygon
    A = polygon_area(xv, yv)
    
    # Compute polygon centroid
    cx, cy = polygon_centroid(xv, yv)

    # Plot the polygon
    plt.plot(xv, yv, '.-', label='Polygon')

    # Plot the centroid with coordinates if that was chosen
    if plot_centroid:   # <- Eqiuvalent to: if plot_centroid == True:
        plt.plot(cx, cy, 'x', label='Centroid')
        plt.annotate(f'({cx:.1f}, {cy:.1f})', xy=(cx, cy),
                     xytext=(cx, cy), textcoords='offset points')

    # Set labels, titles and legend
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Polygon with A={A}')
    plt.legend()
    plt.show()

import matplotlib.pyplot as plt

x_polygon = [-5, 2, 5, 7, 8, 5, 1, -5]
y_polygon = [-2, -15, -13, -10, -6, 2, 5, -2]
plot_polygon(x_polygon, y_polygon)
