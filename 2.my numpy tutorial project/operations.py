import numpy as np
import matplotlib.pyplot as plt

class IntArray:
    def __init__(self, int_array):
        if not isinstance(int_array, np.ndarray) or int_array.dtype != int:
            raise ValueError("Input must be a NumPy array of integers")
        
        self.int_array = int_array

    def display(self):
        print(self.int_array)

    def salary(self):
        array_shape = self.int_array.shape
        money_for_product = np.full(array_shape, 7)
        salaries = self.int_array * money_for_product

        print(f"People made {self.int_array} products and this is their salaries {salaries}")

    def show_data(self):
        x = np.arange(len(self.int_array))
        plt.plot(x, self.int_array, marker = 'o')

        plt.title('Productivity of employees')
        plt.xlabel('ranks of employees')
        plt.ylabel('products/month')
        plt.xticks(x)
        plt.grid()
        plt.show()
    
    