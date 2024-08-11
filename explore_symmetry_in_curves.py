import numpy as np
import matplotlib.pyplot as plt

def read_shape_from_file(filepath):
    """Read shapes from a CSV file where each shape is a set of polylines."""
    data = np.genfromtxt(filepath, delimiter=',')
    print("Loaded Data:")
    print(data)  # Debugging: print the loaded data

    # Remove rows with NaN values
    data = data[~np.isnan(data).any(axis=1)]

    shapes = []
    for i in np.unique(data[:, 0]):
        shape_data = data[data[:, 0] == i][:, 1:]
        paths = []
        for j in np.unique(shape_data[:, 0]):
            path = shape_data[shape_data[:, 0] == j][:, 1:]
            if path.size > 0:
                paths.append(path)
        if paths:
            shapes.append(paths)
        else:
            print(f"No valid paths found for shape index {i}.")
    return shapes

def reflect_point(point, axis):
    """Reflect a point across a given axis."""
    if axis == 'x':
        return np.array([point[0], -point[1]])
    elif axis == 'y':
        return np.array([-point[0], point[1]])
    elif axis == '45':
        return np.array([point[1], point[0]])
    elif axis == '-45':
        return np.array([-point[1], -point[0]])

def check_symmetry(shape, axis):
    """Check if a shape has reflection symmetry about a given axis."""
    shape = np.array(shape)
    reflected_shape = [reflect_point(point, axis) for point in shape]
    reflected_shape = np.array(reflected_shape)
    
    # Debug prints
    print(f"Original Shape:\n{shape}")  # Debugging
    print(f"Reflected Shape:\n{reflected_shape}")  # Debugging
    
    # Normalize points to avoid floating-point issues
    shape_sorted = np.sort(shape, axis=0)
    reflected_sorted = np.sort(reflected_shape, axis=0)
    
    print(f"Shape (sorted):\n{shape_sorted}")  # Debugging
    print(f"Reflected Shape (sorted):\n{reflected_sorted}")  # Debugging
    
    return np.allclose(shape_sorted, reflected_sorted, atol=1e-6)


def plot_shape(shape, axis=None):
    """Plot the shape and optional symmetry axis."""
    plt.figure()
    plt.plot(shape[:, 0], shape[:, 1], 'b-', label='Original Shape')
    
    if axis:
        if axis == 'x':
            plt.axhline(y=0, color='r', linestyle='--', label='Symmetry Axis')
        elif axis == 'y':
            plt.axvline(x=0, color='r', linestyle='--', label='Symmetry Axis')
        elif axis == '45':
            plt.axline((0, 0), slope=1, color='r', linestyle='--', label='Symmetry Axis')
        elif axis == '-45':
            plt.axline((0, 0), slope=-1, color='r', linestyle='--', label='Symmetry Axis')
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.show()

def test_symmetry_from_file(filepath):
    """Test symmetry of shapes from a file."""
    shapes = read_shape_from_file(filepath)
    
    axes = ['x', 'y', '45', '-45']
    results = []
    
    for shape in shapes:
        if shape:
            # Flatten paths into a single array of points
            shape_points = np.vstack([np.vstack(path) for path in shape if path.size > 0])
            
            if shape_points.size == 0:
                print("No valid points found for the shape.")
                continue
            
            result = {'shape': shape_points, 'symmetries': {}}
            for axis in axes:
                if check_symmetry(shape_points, axis):
                    result['symmetries'][axis] = True
                else:
                    result['symmetries'][axis] = False
            
            results.append(result)
        else:
            print("Empty shape data found.")

    for result in results:
        plot_shape(result['shape'])
        print("Symmetry Results:")
        for axis, has_symmetry in result['symmetries'].items():
            print(f"  {axis}-axis symmetry: {'Yes' if has_symmetry else 'No'}")

# Example usage
test_symmetry_from_file("butterfly_coordinates.csv")
