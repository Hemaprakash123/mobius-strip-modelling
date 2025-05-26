import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import simpson
from scipy.spatial.distance import euclidean

class MobiusStrip:
    def __init__(self, R=1.0, w=0.2, n=100):
        self.R = R  # Radius from center to the middle of the strip
        self.w = w  # Width of the strip
        self.n = n  
        self.u = np.linspace(0, 2 * np.pi, n)
        self.v = np.linspace(-w / 2, w / 2, n)
        self.U, self.V = np.meshgrid(self.u, self.v)
        self.X, self.Y, self.Z = self.compute_coordinates()

    def compute_coordinates(self):
        U = self.U
        V = self.V
        X = (self.R + V * np.cos(U / 2)) * np.cos(U)
        Y = (self.R + V * np.cos(U / 2)) * np.sin(U)
        Z = V * np.sin(U / 2)
        return X, Y, Z

    def compute_surface_area(self):
        Xu = np.gradient(self.X, axis=1)
        Xv = np.gradient(self.X, axis=0)
        Yu = np.gradient(self.Y, axis=1)
        Yv = np.gradient(self.Y, axis=0)
        Zu = np.gradient(self.Z, axis=1)
        Zv = np.gradient(self.Z, axis=0)
        
        # Cross product magnitude ||Xu x Xv|| gives area element
        cross_x = Yu * Zv - Zu * Yv
        cross_y = Zu * Xv - Xu * Zv
        cross_z = Xu * Yv - Yu * Xv
        area_element = np.sqrt(cross_x**2 + cross_y**2 + cross_z**2)
        
        # Integrate area over parameter space
        area = simpson(simpson(area_element, self.v), self.u)
        return area

    def compute_edge_length(self):
        # Boundary curves for v = -w/2 and v = w/2
        edge1 = np.array([
            (self.X[0, i], self.Y[0, i], self.Z[0, i]) for i in range(self.n)
        ])
        edge2 = np.array([
            (self.X[-1, i], self.Y[-1, i], self.Z[-1, i]) for i in range(self.n)
        ])

        def compute_length(points):
            return sum(euclidean(points[i], points[i + 1]) for i in range(len(points) - 1))
        
        return compute_length(edge1) + compute_length(edge2)

    def plot(self):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(self.X, self.Y, self.Z, cmap='viridis', edgecolor='k', alpha=0.8)
        ax.set_title("Möbius Strip")
        plt.tight_layout()
        plt.show()

mobius = MobiusStrip(R=1, w=0.4, n=200)
surface_area = mobius.compute_surface_area()
edge_length = mobius.compute_edge_length()
mobius.plot()

(surface_area, edge_length)
