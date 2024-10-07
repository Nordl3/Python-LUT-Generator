import numpy as np
import matplotlib.pyplot as plt

# Number of samples for the LUT
LUT_SIZE = 512

# Create the exponential rise and fall LUTs
expo_rise = np.exp(np.linspace(0, 5, LUT_SIZE)) - 1  # Starts at 0 and increases sharply at the end (expo rise)
inv_expo_fall = 1 - np.exp(np.linspace(0, 5, LUT_SIZE))  # Starts at 4096 and decreases sharply at the end (invExpoFall)

# Create the inverted exponential rise and fall (logarithmic-like behavior)
inv_expo_rise = np.flip(inv_expo_fall)  # Starts at 0 and increases sharply at the start (invExpoRise)
expo_fall = np.flip(expo_rise)  # Starts at 4096 and decreases sharply at the start (expoFall)

# Normalize all LUTs to the range 0 to 1
expo_rise = (expo_rise - np.min(expo_rise)) / (np.max(expo_rise) - np.min(expo_rise))
inv_expo_fall = (inv_expo_fall - np.min(inv_expo_fall)) / (np.max(inv_expo_fall) - np.min(inv_expo_fall))
inv_expo_rise = (inv_expo_rise - np.min(inv_expo_rise)) / (np.max(inv_expo_rise) - np.min(inv_expo_rise))
expo_fall = (expo_fall - np.min(expo_fall)) / (np.max(expo_fall) - np.min(expo_fall))

# Scale them to your DAC range (e.g., 0 to 4096)
expo_rise_scaled = np.round(expo_rise * 4096).astype(int)
inv_expo_fall_scaled = np.round(inv_expo_fall * 4096).astype(int)
inv_expo_rise_scaled = np.round(inv_expo_rise * 4096).astype(int)
expo_fall_scaled = np.round(expo_fall * 4096).astype(int)

# Function to print arrays in C format
def print_lut_c_format(array, name):
    print(f"const uint16_t {name}[LUT_SIZE] = \n{{")
    print("  ", end="")  # Add 2 spaces at the start of the first line
    for i in range(len(array)):
        if i % 10 == 0 and i != 0:  # Print 10 values per line for better readability
            print("\n  ", end="")
        print(f"{array[i]}, ", end="")
    print("\n};\n")

# Function to save the LUT to a text file
def save_lut_to_txt(array, name):
    filename = f"{name}.txt"
    with open(filename, "w") as f:
        f.write(f"const uint16_t {name}[LUT_SIZE] = \n{{\n")
        f.write("  ")  # Add 2 spaces at the start of the first line
        for i in range(len(array)):
            if i % 10 == 0 and i != 0:  # 10 values per line
                f.write("\n  ")
            f.write(f"{array[i]}, ")
        f.write("\n};\n")
    print(f"Saved {name} to {filename}")

# Function to save PNG plots for each LUT
def save_lut_plot(array, title, filename):
    plt.figure()
    plt.plot(array, label=title)
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename, format='png')
    plt.close()

# Print the LUTs in C-style format
print_lut_c_format(expo_rise_scaled, "expoRiseLUT")
print_lut_c_format(expo_fall_scaled, "expoFallLUT")
print_lut_c_format(inv_expo_rise_scaled, "invExpoRiseLUT")
print_lut_c_format(inv_expo_fall_scaled, "invExpoFallLUT")

# Save the LUTs to text files
save_lut_to_txt(expo_rise_scaled, "expoRiseLUT")
save_lut_to_txt(expo_fall_scaled, "expoFallLUT")
save_lut_to_txt(inv_expo_rise_scaled, "invExpoRiseLUT")
save_lut_to_txt(inv_expo_fall_scaled, "invExpoFallLUT")

# Save PNG plots
save_lut_plot(expo_rise_scaled, "expoRiseLUT", "expoRiseLUT.png")
save_lut_plot(expo_fall_scaled, "expoFallLUT", "expoFallLUT.png")
save_lut_plot(inv_expo_rise_scaled, "invExpoRiseLUT", "invExpoRiseLUT.png")
save_lut_plot(inv_expo_fall_scaled, "invExpoFallLUT", "invExpoFallLUT.png")
