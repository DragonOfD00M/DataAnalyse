from Data_Analyse import DataAnalyst
import matplotlib.pyplot as plt
import numpy as np

Example_x_axis = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
Example_y_axis = np.array([1, 3, 6, 7, 9, 10, 13, 15, 16, 20])

Example_Data = DataAnalyst(Example_x_axis, Example_x_axis)
Example_Data.configure_plots(title="Example Title",
                            xlabel="x-axis",
                            ylabel="y-axis",
                            titlesize=25,
                            labelsize=20,
                            ticksize=15,
                            linecolor="green",
                            pointcolor="red"
                            )

def Example_model(x, A, B): return A*x + B


###########
# Example 1: Shows only the pointplot
Example_Data.point_plot()
plt.show()
###########
# Example 2: Shows only the fitted model
Example_Data.func_reg(Example_model)
plt.show()
###########
# Example 3: Shows both pointplot and fit, along with coefficient info
fig, (ax1, info_ax)  = plt.subplots(1, 2, figsize=(7.5,7.5))
Example_Data.point_plot(ax1)
reg_info = Example_Data.func_reg(Example_model, True, ax1, info_ax, True)
for info in reg_info:
    print(f"coefficient value = {info[0]}\nstandard deviation = {info[1]}\n")
plt.show()
###########



