import matplotlib.pyplot as plt

# for i in [1, 2, 3]:
#     # Create a figure for holding subplots and set size
#     plt.figure(figsize=(14,3))

#     # Create first plot as line plot
#     plt.subplot(131)
#     plt.plot([1, 2, 3, 4], [1, 2, 3, 4])

#     # Create second plot as scatter plot
#     plt.subplot(132)
#     plt.scatter([1, 2, 3, 4], [1, 2, 3, 4])

#     # Create third plot as bar plot
#     plt.subplot(133)
#     plt.bar([1, 2, 3, 4], [1, 2, 3, 4])

# plt.show()

# Create a 2 by 3 subplot grid with shared x-a and y-axis
# fig, ax = plt.subplots(2, 3, sharex='col', sharey='row')
# plt.show()


# plt.figure(figsize=(10,5))
# --- EXERCISE 1.1 ---
x = [1, 3, 6, 9, 16]
y = [7, 3, 7, 1, 5]

plt.plot(x, y, 'k.-', label='Original curve')


# --- EXERCISE 1.2 ---
plt.title('This is the title')


# --- EXERCISE 1.3 ---
plt.xlabel('This is the xlabel')
plt.ylabel('This is the ylabel')


# --- EXERCISE 1.4 ---
y2 = [9, 5, 5, 2, 6]
y3 = [4, 6, 2, 6, 8]
y4 = [1, 8, 1, 3, 2]

plt.plot(x, y2, label='Second curve')
plt.plot(x, y3, label='Third curve')
plt.plot(x, y4, label='Fourth curve')


# --- EXERCISE 1.5 ---
# The labels in the plot commands above were
# added as part of this exercise
plt.legend()

# plt.show()

# Create a figure for holding subplots and set size
plt.figure()

# Create first plot as line plot
plt.subplot(131)
plt.plot([1, 2, 3, 4], [1, 2, 3, 4])

# Create second plot as scatter plot
plt.subplot(132)
plt.plot([1, 2, 3, 4], [1, 2, 3, 4], '.', markersize=12)

# Create third plot as bar plot
plt.subplot(133)
plt.bar([1, 2, 3, 4], [1, 2, 3, 4])
plt.show()
