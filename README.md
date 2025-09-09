```markdown
# Diabetic Foot Ulcer Detection and Classification

## Overview
This project focuses on the detection and classification of diabetic foot ulcers using deep learning techniques. The goal is to develop a model that can accurately identify and categorize foot ulcers, aiding in early diagnosis and treatment.

## Technologies Used
- **Python**: Version 3.8.10
- **IDE**: PyCharm 2020
- **Deep Learning Framework**: Ultralytics (YOLOv8m)
- **GUI Framework**: Tkinter
- **Image Annotation Tool**: LabelImg

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/bhaskarasp/diabetic-foot-ulcer-detection.git
   cd diabetic-foot-ulcer-detection
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Annotate Images**: Use LabelImg to annotate images of diabetic foot ulcers. Save the annotations in the specified format.
2. **Train the Model**: Run the training script to train the model using the annotated images.
   ```bash
   python train.py
   ```
3. **Run the Application**: Launch the GUI application to detect and classify ulcers.
   ```bash
   python mainpage.py
   ```

## Features
- **Image Annotation**: Easy-to-use interface for annotating images of foot ulcers.
- **Model Training**: Train a deep learning model using annotated images.
- **Real-time Detection**: Detect and classify ulcers through a user-friendly GUI.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the developers of the Ultralytics library for providing a powerful framework for object detection.
- Special thanks to the contributors of LabelImg for their excellent annotation tool.


```