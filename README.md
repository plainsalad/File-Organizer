# File Organizer

This project is a file organizer application that uses a graphical user interface (GUI) to sort and organize files into different folders based on their extensions. It supports images, videos, documents, audio files, and custom categories.

## Files

- `organizer.py`: The main Python script containing the file organizer code.

## Requirements

- Python 3.x
- Tkinter (comes pre-installed with Python)
- shutil (part of the Python Standard Library)

## Installation

1. Clone the repository or download the `organizer.py` file.
2. No additional libraries need to be installed as Tkinter and shutil come pre-installed with Python.

## Usage

1. Run the `organizer.py` script:

    ```sh
    python organizer.py
    ```

2. The GUI will open. Follow these steps to organize your files:
    - Click on the "Browse" button to select the directory you want to organize.
    - Check the boxes for the types of files you want to organize (Images, Videos, Documents, Audio).
    - Enter the names for the destination folders for each file type.
    - Optionally, add custom folders with specific extensions.
    - Click the "Organize" button to start organizing the files.

## Features

- **Organize by File Type**: Automatically moves files into folders based on their extensions.
- **Custom Folders**: Allows users to define custom folders and associated extensions.
- **Graphical User Interface**: Easy-to-use GUI built with Tkinter.

## Creating an Executable (Optional)

To create an executable file from the Python script, you can use a tool like `pyinstaller`.

1. Install `pyinstaller`:

    ```sh
    pip install pyinstaller
    ```

2. Generate the executable:

    ```sh
    pyinstaller --onefile organizer.py
    ```

    This will create an executable file in the `dist` directory.
