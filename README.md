# Passport Photo Processor (Ghana SHS / WASSCE)
A Windows desktop application that automatically crops, centers, and resizes passport photographs to the required 150 × 200 pixels format, specifically designed to support manual photo preparation for Ghana SHS and WASSCE registrations.

The application eliminates the need for manual photo editing by using face detection to ensure correct alignment and consistent output.

## Problem Statement

During Ghana SHS placement and WASSCE registration, students are required to submit passport photographs that meet strict size and alignment requirements.

### Common challenges include:

- Incorrect image dimensions

- Poor head positioning

- Inconsistent background handling

- Manual resizing using tools like Photoshop, which is time-consuming and error-prone


## Solution

This application:

- Automatically detects the face

- Crops the image based on passport photo standards

- Centers the head correctly

- Resizes the image to 150 × 200 pixels

- Outputs a clean white background

- Runs as a standalone Windows executable with no Python installation required


## Application Features

- Upload photos using a file selection button

- Drag-and-drop image support

- Face-aware cropping using OpenCV

- Automatic passport aspect ratio enforcement (3:4)

- Batch processing of multiple images

- Progress tracking and processing feedback

- Automatic saving to an output_passport folder

- Distributed as a Windows desktop executable (.exe)


## Technologies Used

- Python

- OpenCV (face detection using Haar Cascade)

- Pillow (image processing)

- Tkinter (graphical user interface)

- TkinterDnD2 (drag-and-drop support)

- PyInstaller (Windows executable packaging)


## Output Specifications

| Property       | Value      |
| -------------- | ---------- |
| Width          | 150 pixels |
| Height         | 200 pixels |
| Aspect Ratio   | 3 : 4      |
| Background     | White      |
| Face Detection | Enabled    |
| Output Formats | JPG, PNG   |


## How to Use (Executable Version)

- Launch passport_app.exe

- Drag and drop images or click Upload Photos

- Click Start Processing

- Processed passport photos are saved automatically in:  output_passport/


## How to Build from Source

### Requirements
pip install opencv-python pillow tkinterdnd2 pyinstaller

### Build Command

python -m PyInstaller --onefile --windowed \
--icon=app_icon.ico \
--add-data "haarcascade_frontalface_default.xml;." \
passport_app.py

## Intended Users

- SHS administrators

- Private WASSCE candidates

- Schools handling bulk student registrations

- Photo studios preparing student passport photographs

- Individuals without access to professional photo editing software

## Screenshots

![App Interface](screenshots/app_interface.png)
![Upload Photos](screenshots/upload_photos.png)
![Processing](screenshots/processing.png)
![Output Folder](screenshots/output_folder.png)


## Author

Dennis Merrick
IT Student | Python Deve || Full stack dev