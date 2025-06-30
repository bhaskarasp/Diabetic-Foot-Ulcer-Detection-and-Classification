import tkinter as tk
import os
import shutil
from tkinter import filedialog, messagebox
from ultralytics import YOLO
from PIL import Image, ImageTk
import numpy as np


class Page2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Set up the background image
        self.background_image = tk.PhotoImage(file="bg (9).png")  # Replace with your image path
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.uploaded_file_path = ""

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Instruction label
        self.label = tk.Label(self, font=('Helvetica', 12), bg='#F0F0F0', fg='#555555')
        self.label.grid(row=6, column=0, columnspan=2, pady=20)

        # Label for uploaded image
        self.sign_image = tk.Label(self, bg='#F0F0F0')
        self.sign_image.grid(row=3, column=0, padx=30, pady=20)

        # Label for result image
        self.resultimg = tk.Label(self, bg='#F0F0F0')
        self.resultimg.grid(row=3, column=1, padx=30, pady=20)

        # Confidence score label
        self.confidence_label = tk.Label(self, text="Confidence: N/A", font=('Helvetica', 14), bg='#F0F0F0',
                                         fg='#000000')
        self.confidence_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Predicted class label
        self.class_label = tk.Label(self, text="Predicted Class: N/A", font=('Helvetica', 14), bg='#F0F0F0',
                                    fg='#000000')
        self.class_label.grid(row=5, column=0, columnspan=2, pady=10)

        # Upload Image Button
        upload_button = tk.Button(self, text="Upload Image", command=self.upload_image, padx=15, pady=10)
        upload_button.configure(background='#5E81AC', foreground='white', font=('Helvetica', 14, 'bold'), relief="flat",
                                borderwidth=0)
        upload_button.grid(row=7, column=0, padx=20, pady=10, sticky='ew')  # Use sticky to expand horizontally

        # Classify Image Button
        classify_button = tk.Button(self, text="Classify Image", command=self.classify, padx=15, pady=10)
        classify_button.configure(background='#5E81AC', foreground='white', font=('Helvetica', 14, 'bold'),
                                  relief="flat", borderwidth=0)
        classify_button.grid(row=7, column=1, padx=20, pady=10, sticky='ew')  # Use sticky to expand horizontally

        # Heading
        heading = tk.Label(self, text="Foot Ulcer Detection", pady=20, font=('Helvetica', 30, 'bold'))
        heading.configure(background='#F0F0F0', foreground='#2E3440')
        heading.grid(row=0, column=0, columnspan=2)

        # Center the layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Set minimum size for rows to prevent movement
        self.grid_rowconfigure(3, minsize=200)  # Adjust this value as needed
        self.grid_rowconfigure(4, minsize=50)   # Adjust this value as needed
        self.grid_rowconfigure(5, minsize=50)   # Adjust this value as needed
        self.grid_rowconfigure(6, minsize=50)   # Adjust this value as needed
        self.grid_rowconfigure(7, minsize=50)   # Adjust this value as needed

    def upload_image(self):
        try:
            self.uploaded_file_path = filedialog.askopenfilename(title="Select an image file",
                                                                 filetypes=[("Image Files", "*.jpg;*.png"),
                                                                            ("JPG files", "*.jpg;"),
                                                                            ("PNG files", "*.png")])
            if self.uploaded_file_path:
                uploaded = Image.open(self.uploaded_file_path)
                uploaded.thumbnail(((self.winfo_width() / 3), (self.winfo_height() / 3)))
                im = ImageTk.PhotoImage(uploaded)
                self.sign_image.configure(image=im)
                self.sign_image.image = im
                self.label.configure(text='Image uploaded! Now click "Classify Image" to classify it.', fg='black')
                self.confidence_label.configure(text='Confidence: N/A')
                self.class_label.configure(text='Predicted Class: N/A')
            else:
                self.label.configure(text='No image selected.', fg='red')
        except Exception as e:
            print(f"Error: {e}")

    def classify(self):
        if self.uploaded_file_path == "":
                self.class_label.configure(text='No prediction available', fg='red')
                return
        path = "output"
        if os.path.exists(path):
            shutil.rmtree(path)  # Delete the existing output directory
        os.makedirs(path)  # Create a new output directory

        model = YOLO("best.pt")  # Load your YOLO model
        results = model.predict(source=self.uploaded_file_path, project="output", save=True, conf=0.2,
                                line_thickness=1)

        # Extract all predictions
        result = results[0]
        boxes = result.boxes

        if len(boxes) > 0:
            predictions = []
            for i in range(len(boxes.conf)):
                confidence = boxes.conf[i].item()
                predicted_class = model.names[int(boxes.cls[i].item())]
                predictions.append((predicted_class, confidence))

            # Display result image
            filename = os.path.splitext(os.path.basename(self.uploaded_file_path))[0]
            im = Image.open(r"output/predict/" + filename + ".jpg")
            im.save("output/predict/predictedimage.jpg")
            uploaded = Image.open("output/predict/predictedimage.jpg")
            uploaded.thumbnail((self.winfo_width() // 2, self.winfo_height() // 2))
            im = ImageTk.PhotoImage(uploaded)
            self.resultimg.configure(image=im)
            self.resultimg.image = im

            # Display all predictions
            prediction_text = "\n".join([f"{cls}: {conf:.2f}" for cls, conf in predictions])
            self.confidence_label.configure(text=f'Predictions:\n{prediction_text}', fg='green')

            # Optionally, execute scripts based on detected classes
            for predicted_class, confidence in predictions:
                if predicted_class == "Stage 1_Ulcer":
                    os.system("python stage1.py")
                elif predicted_class == "Stage 2_Ulcer":
                    os.system("python stage2.py")
                elif predicted_class == "Stage 3_Ulcer":
                    os.system("python stage3.py")
                elif predicted_class == "Final_Stage_Ulcer":
                    os.system("python stage4.py")
        else:
            self.confidence_label.configure(text='No detections', fg='red')
            self.class_label.configure(text='No prediction available', fg='red')


        if __name__ == "__main__":
            root = tk.Tk()
            root.title("Foot Ulcer Detection")
            root.geometry("800x600")  # Set the window size
            app = Page2(root)
            app.pack(fill="both", expand=True)
            root.mainloop()
