'''Create a model to predict the animals in the given picture .it should predict group of animals as well .
  This model should able to identify child animal as well as adult animals . this model should be able to 
identiy the herbivores and carnivores. if the group of animals are there it should be predict how many 
herbivores and carnivores are there . '''

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

# Define the animal detection function
def detect_animals(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detections = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Increased the threshold for better accuracy
            x, y, w, h = cv2.boundingRect(contour)
            detections.append((x, y, x + w, y + h))
    
    return detections

# Define the animal classification function
def classify_animal(image, bbox):
    x1, y1, x2, y2 = bbox
    animal_patch = image[y1:y2, x1:x2]
    
    # Convert the animal patch to grayscale for color analysis
    animal_gray = cv2.cvtColor(animal_patch, cv2.COLOR_BGR2GRAY)
    mean_intensity = np.mean(animal_gray)
    
    # Simple classification based on mean intensity (just for demonstration)
    if mean_intensity > 100:  # Threshold for demonstration; you can add more complex logic
        return "herbivore"
    else:
        return "carnivore"

# Define the prediction function
def predict_animals(image_path):
    image = cv2.imread(image_path)
    animals = detect_animals(image)
    
    herbivores_count = 0
    carnivores_count = 0
    for bbox in animals:
        animal_type = classify_animal(image, bbox)
        if animal_type == "herbivore":
            herbivores_count += 1
        elif animal_type == "carnivore":
            carnivores_count += 1
    
    return herbivores_count, carnivores_count

# Define the function for uploading the image
def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")],
        initialdir="."
    )
    if file_path:
        herbivores_count, carnivores_count = predict_animals(file_path)
        result_label.config(text=f"Herbivores count: {herbivores_count}\nCarnivores count: {carnivores_count}")

# Create the Tkinter window
window = tk.Tk()
window.title("Animal Detection")

# Set window size and background color
window.geometry("400x200")
window.configure(bg="#f0f0f0")

# Create a stylish and bold upload button
upload_button = tk.Button(
    window,
    text="Upload Image",
    command=upload_image,
    font=("Arial", 16, 'bold'),
    bg='#4CAF50',  # Green background color
    fg='white',    # White text color
    padx=20,       # Padding X
    pady=10,       # Padding Y
    relief='raised', # Raised border for 3D effect
    bd=5           # Border width
)
upload_button.pack(pady=20)

# Create a result label with stylish appearance
result_label = tk.Label(
    window,
    text="",
    font=("Arial", 14),
    bg="#f0f0f0",  # Same background color as window
    fg="#333333"   # Dark gray text color
)
result_label.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()
