import numpy as np
import matplotlib.pyplot as plt

# Function to load data from a CSV file
def load_data(file_path):
    return np.loadtxt(file_path, delimiter=',', dtype=float)

# Load test case data from files
np_path_XYs = load_data("C:/Users/kamin/OneDrive/Desktop/problems/problems/frag0.csv")  # Replace with your actual file path
np_path_XY2s = load_data("C:/Users/kamin/OneDrive/Desktop/problems/problems/frag1.csv")  # Replace with your actual file path

# Get unique IDs for paths
size = len(np.unique(np_path_XYs[:, 0]))
size2 = len(np.unique(np_path_XY2s[:, 0]))

# Extract paths for XY and XY2
XY = []
XY2 = []

for i in range(size):
    new_path = np_path_XYs[np_path_XYs[:, 0] == i][:, 2:]
    XY.append(new_path)

for i in range(size2):
    new_path = np_path_XY2s[np_path_XY2s[:, 0] == i][:, 2:]
    XY2.append(new_path)

# Function to reflect points across the y-axis
def reflect_across_y(points):
    reflected_points = np.copy(points)
    reflected_points[:, 0] = -reflected_points[:, 0]  # Reflect x-coordinates
    return reflected_points

# Function to check if a curve is regularized (smoothness criteria)
def is_regular_curve(points, tolerance=1e-2):
    # Check if the points are approximately equally spaced
    distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
    mean_distance = np.mean(distances)
    return np.all(np.abs(distances - mean_distance) < tolerance)

# Check symmetry and regularity for XY
symmetry_XY = []
regularity_XY = []
for i in range(size):
    reflected_path = reflect_across_y(XY[i])
    is_symmetric = np.allclose(reflected_path, XY[i], atol=1e-6)  # Adjust tolerance as needed
    symmetry_XY.append(is_symmetric)
    
    is_regular = is_regular_curve(XY[i])
    regularity_XY.append(1 if is_regular else 0)

# Check symmetry and regularity for XY2
symmetry_XY2 = []
regularity_XY2 = []
for i in range(size2):
    reflected_path = reflect_across_y(XY2[i])
    is_symmetric = np.allclose(reflected_path, XY2[i], atol=1e-6)
    symmetry_XY2.append(is_symmetric)
    
    is_regular = is_regular_curve(XY2[i])
    regularity_XY2.append(1 if is_regular else 0)

# Plotting the paths and saving the images
for i in range(size):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    ax.plot(XY[i][:, 0], XY[i][:, 1], linewidth=2, label=f'Path {i} - {"Regular" if regularity_XY[i] else "Non-Regular"}')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.savefig(f'XY_path_{i}.png')  # Save the image
    plt.show()

fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
for i in range(size):
    ax.plot(XY[i][:, 0], XY[i][:, 1], linewidth=2, label=f'Path {i} - {"Regular" if regularity_XY[i] else "Non-Regular"}')
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.savefig('XY_combined.png')  # Save the image
plt.show()

for i in range(size2):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    ax.plot(XY2[i][:, 0], XY2[i][:, 1], linewidth=2, label=f'Path {i} - {"Regular" if regularity_XY2[i] else "Non-Regular"}')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.savefig(f'XY2_path_{i}.png')  # Save the image
    plt.show()

fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
for i in range(size2):
    ax.plot(XY2[i][:, 0], XY2[i][:, 1], linewidth=2, label=f'Path {i} - {"Regular" if regularity_XY2[i] else "Non-Regular"}')
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.savefig('XY2_combined.png')  # Save the image
plt.show()

# Print symmetry and regularity results
print("Symmetry check for XY paths:", symmetry_XY)
print("Regularity check for XY paths:", regularity_XY)
print("Symmetry check for XY2 paths:", symmetry_XY2)
print("Regularity check for XY2 paths:", regularity_XY2)
