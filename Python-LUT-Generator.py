import numpy as np
import matplotlib.pyplot as plt

# Number of samples for the LUT
LUT_SIZE = 512

# Create an exponential rise from 0 to 1
inv_expo_rise = 1 - np.exp(-np.linspace(0, 5, LUT_SIZE))  # Previously called expoRise

# invExpoFall is the mirror of expoRise, starting from 1 and falling to 0
inv_expo_fall = np.exp(-np.linspace(0, 5, LUT_SIZE))  # Previously called expoFall

# Normalize both to the range 0 to 1
inv_expo_rise = (inv_expo_rise - np.min(inv_expo_rise)) / (np.max(inv_expo_rise) - np.min(inv_expo_rise))
inv_expo_fall = (inv_expo_fall - np.min(inv_expo_fall)) / (np.max(inv_expo_fall) - np.min(inv_expo_fall))

# expoRise should now be inv_expo_rise flipped horizontally
expo_rise = np.flip(inv_expo_rise)  # Previously called invExpoRise

# expoFall should now be inv_expo_fall flipped horizontally
expo_fall = np.flip(inv_expo_fall)  # Previously called invExpoFall

# Scale them to your DAC range (e.g., 0 to 3090)
inv_expo_rise_scaled = np.round(inv_expo_rise * 3090).astype(int)
inv_expo_fall_scaled = np.round(inv_expo_fall * 3090).astype(int)
expo_rise_scaled = np.round(expo_rise * 3090).astype(int)
expo_fall_scaled = np.round(expo_fall * 3090).astype(int)

# Function to print arrays in C format
def print_lut_c_format(array, name):
    print(f"const uint16_t {name}[LUT_SIZE] = \n{{")
    for i in range(len(array)):
        if i % 10 == 0:  # Print 10 values per line for better readability
            print("\n  ", end="")
        print(f"{array[i]}, ", end="")
    print("\n};\n")

# Function to save the LUT to a text file
def save_lut_to_txt(array, name):
    filename = f"{name}.txt"
    with open(filename, "w") as f:
        f.write(f"const uint16_t {name}[LUT_SIZE] = {{\n")
        for i in range(len(array)):
            if i % 10 == 0:  # 10 values per line
                f.write("\n  ")
            f.write(f"{array[i]}, ")
        f.write("\n};\n")
    print(f"Saved {name} to {filename}")

# Print the LUTs in C-style format
print_lut_c_format(inv_expo_rise_scaled, "invExpoRiseLUT")
print_lut_c_format(inv_expo_fall_scaled, "invExpoFallLUT")
print_lut_c_format(expo_rise_scaled, "expoRiseLUT")
print_lut_c_format(expo_fall_scaled, "expoFallLUT")

# Save the LUTs to text files
save_lut_to_txt(inv_expo_rise_scaled, "invExpoRiseLUT")
save_lut_to_txt(inv_expo_fall_scaled, "invExpoFallLUT")
save_lut_to_txt(expo_rise_scaled, "expoRiseLUT")
save_lut_to_txt(expo_fall_scaled, "expoFallLUT")

# Function to save PNG plots for each LUT
def save_lut_plot(array, title, filename):
    plt.figure()
    plt.plot(array, label=title)
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename, format='png')
    plt.close()

# Save PNG plots
save_lut_plot(inv_expo_rise_scaled, "invExpoRiseLUT", "invExpoRiseLUT.png")
save_lut_plot(inv_expo_fall_scaled, "invExpoFallLUT", "invExpoFallLUT.png")
save_lut_plot(expo_rise_scaled, "expoRiseLUT", "expoRiseLUT.png")
save_lut_plot(expo_fall_scaled, "expoFallLUT", "expoFallLUT.png")
