import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Checkbutton, Entry, StringVar, simpledialog, Scrollbar, Frame

# Function to organize files
def organize_files(source_dir, selected_exts, organize_images, organize_videos, organize_docs, organize_audio, image_dir_name, video_dir_name, doc_dir_name, audio_dir_name, custom_dirs):
    # Define the target directories
    image_dir = os.path.join(source_dir, image_dir_name)
    video_dir = os.path.join(source_dir, video_dir_name)
    doc_dir = os.path.join(source_dir, doc_dir_name)
    audio_dir = os.path.join(source_dir, audio_dir_name)

    # Create the target directories if they don't exist
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(doc_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)

    # Function to move files
    def mover(file_list, target_dir):
        for file in file_list:
            source_file = os.path.join(source_dir, file)
            target_file = os.path.join(target_dir, file)
            shutil.move(source_file, target_file)

    # Get the list of files in the source directory
    files = os.listdir(source_dir)

    # Separate files by type
    if organize_images:
        image_files = [f for f in files if f.lower().endswith(tuple(selected_exts['Images']))]
        mover(image_files, image_dir)
    if organize_videos:
        video_files = [f for f in files if f.lower().endswith(tuple(selected_exts['Videos']))]
        mover(video_files, video_dir)
    if organize_docs:
        doc_files = [f for f in files if f.lower().endswith(tuple(selected_exts['Documents']))]
        mover(doc_files, doc_dir)
    if organize_audio:
        audio_files = [f for f in files if f.lower().endswith(tuple(selected_exts['Audio']))]
        mover(audio_files, audio_dir)

    for custom_dir, exts in custom_dirs.items():
        custom_files = [f for f in files if f.lower().endswith(tuple(exts))]
        custom_dir_path = os.path.join(source_dir, custom_dir)
        os.makedirs(custom_dir_path, exist_ok=True)
        mover(custom_files, custom_dir_path)

    messagebox.showinfo('Success', 'Files have been organized successfully!')

# Function to browse and select directory
def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_var.set(directory)

# Function to handle the organize button click
def handle_organize():
    directory = directory_var.get()
    image_dir_name = image_dir_var.get()
    video_dir_name = video_dir_var.get()
    doc_dir_name = doc_dir_var.get()
    audio_dir_name = audio_dir_var.get()

    organize_images = organize_images_var.get()
    organize_videos = organize_videos_var.get()
    organize_docs = organize_docs_var.get()
    organize_audio = organize_audio_var.get()

    selected_exts = {
        'Images': [ext for ext, var in image_vars.items() if var.get()],
        'Videos': [ext for ext, var in video_vars.items() if var.get()],
        'Documents': [ext for ext, var in doc_vars.items() if var.get()],
        'Audio': [ext for ext, var in audio_vars.items() if var.get()]
    }

    # Validate input fields based on the checkboxes
    if not directory:
        messagebox.showerror('Error', 'Please select a directory.')
        return

    if organize_images and not image_dir_name:
        messagebox.showerror('Error', 'Please enter a name for the Images folder.')
        return
    if organize_videos and not video_dir_name:
        messagebox.showerror('Error', 'Please enter a name for the Videos folder.')
        return
    if organize_docs and not doc_dir_name:
        messagebox.showerror('Error', 'Please enter a name for the Documents folder.')
        return
    if organize_audio and not audio_dir_name:
        messagebox.showerror('Error', 'Please enter a name for the Audio folder.')
        return

    custom_dirs = {}
    for custom_dir_name, (custom_var, custom_exts_var, custom_name_var) in custom_dirs_vars.items():
        exts = custom_exts_var.get().split(',')
        exts = [ext.strip() for ext in exts if ext.strip()]
        folder_name = custom_name_var.get().strip()
        if exts and folder_name:
            custom_dirs[folder_name] = exts

    organize_files(directory, selected_exts, organize_images, organize_videos, organize_docs, organize_audio, image_dir_name, video_dir_name, doc_dir_name, audio_dir_name, custom_dirs)

# Function to open pop-up window for selecting extensions
def open_extensions_selector(ext_type, ext_vars):
    def toggle_extensions(ext, var):
        ext_vars[ext] = var

    window = Toplevel(root)
    window.title(f'Select {ext_type} extensions')

    for ext in ext_vars.keys():
        var = ext_vars[ext]
        Checkbutton(window, text=ext, variable=var, command=lambda e=ext, v=var: toggle_extensions(e, v)).pack(anchor='w')

    tk.Button(window, text="Done", command=window.destroy).pack(pady=10)

# Function to open pop-up window for custom extensions
def open_custom_extensions_selector(custom_dir_name):
    custom_exts_var = custom_dirs_vars[custom_dir_name][1]
    window = Toplevel(root)
    window.title(f'Custom Extensions for {custom_dir_name}')

    def add_extension():
        ext = simpledialog.askstring("Input", "Enter a custom extension (e.g., .ext):")
        if ext:
            current_exts = custom_exts_var.get()
            if current_exts:
                custom_exts_var.set(current_exts + ',' + ext)
            else:
                custom_exts_var.set(ext)

    tk.Label(window, text="Enter custom extensions one by one:").pack(pady=10)
    tk.Button(window, text="Add Extension", command=add_extension).pack(pady=10)
    tk.Label(window, textvariable=custom_exts_var).pack(pady=10)
    tk.Button(window, text="Done", command=window.destroy).pack(pady=10)

# Function to add a custom directory
def add_custom_directory():
    custom_dir_name = f"Custom Folder {len(custom_dirs_vars) + 1}"
    custom_var = tk.BooleanVar(value=True)
    custom_exts_var = tk.StringVar()
    custom_name_var = tk.StringVar(value="")
    custom_dirs_vars[custom_dir_name] = (custom_var, custom_exts_var, custom_name_var)

    row = len(custom_dirs_vars) * 4 + 18 
    tk.Label(scrollable_frame, text=f"{custom_dir_name}:", font=('Helvetica', 10, 'bold')).grid(row=row, column=0, padx=10, pady=5, sticky='w')
    tk.Checkbutton(scrollable_frame, text="Organize", variable=custom_var).grid(row=row+1, column=0, padx=30, pady=5, sticky='w')
    tk.Label(scrollable_frame, text="Name").grid(row=row+2, column=0, padx=30, pady=5, sticky='w')
    Entry(scrollable_frame, textvariable=custom_name_var, width=50).grid(row=row+2, column=1, padx=10, pady=5, sticky='w')
    tk.Button(scrollable_frame, text="Custom Extensions", command=lambda: open_custom_extensions_selector(custom_dir_name)).grid(row=row+3, column=0, padx=30, pady=5, sticky='w')

    update_organize_button() 

# Function to update the position of the organize button
def update_organize_button():
    row = len(custom_dirs_vars) * 8 + 18
    organize_button.grid(row=row, column=0, columnspan=3, pady=20)

# Create the main application window
root = tk.Tk()
root.title("File Organizer")
root.geometry("600x700")
root.resizable(False, False)

# Create a canvas and a scrollbar for the frame
canvas = tk.Canvas(root)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Variables to hold user inputs
directory_var = tk.StringVar()
image_dir_var = tk.StringVar()
video_dir_var = tk.StringVar()
doc_dir_var = tk.StringVar()
audio_dir_var = tk.StringVar()

organize_images_var = tk.BooleanVar(value=True)
organize_videos_var = tk.BooleanVar(value=True)
organize_docs_var = tk.BooleanVar(value=True)
organize_audio_var = tk.BooleanVar(value=True)

# Define the file extension for each type
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tiff', '.ico')
video_extensions = ('.mp4', '.mkv', '.webm', '.flv', '.avi', '.mov', '.wmv', '.mpg', '.mpeg', '.3gp')
doc_extensions = ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.csv', '.html', '.xml', '.json')
audio_extensions = ('.mp3', '.wav', '.flac', '.ogg', '.wma', '.m4a', '.aac', '.aiff', '.alac')

image_vars = {ext: tk.BooleanVar(value=True) for ext in image_extensions}
video_vars = {ext: tk.BooleanVar(value=True) for ext in video_extensions}
doc_vars = {ext: tk.BooleanVar(value=True) for ext in doc_extensions}
audio_vars = {ext: tk.BooleanVar(value=True) for ext in audio_extensions}

# Dictionary to hold custom directory variables
custom_dirs_vars = {}

# Create and place the widgets
tk.Label(scrollable_frame, text="Select a directory to organize:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
tk.Entry(scrollable_frame, textvariable=directory_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(scrollable_frame, text="Browse", command=browse_directory).grid(row=0, column=2, padx=10, pady=5)

# Images section
tk.Label(scrollable_frame, text="Images:", font=('Helvetica', 10, 'bold')).grid(row=1, column=0, padx=10, pady=5, sticky='w')
tk.Checkbutton(scrollable_frame, text="Organize", variable=organize_images_var).grid(row=2, column=0, padx=30, pady=5, sticky='w')
tk.Label(scrollable_frame, text="Name").grid(row=3, column=0, padx=30, pady=5, sticky='w')
tk.Entry(scrollable_frame, textvariable=image_dir_var, width=50).grid(row=3, column=1, padx=10, pady=5, sticky='w')
tk.Button(scrollable_frame, text="Select Extensions", command=lambda: open_extensions_selector('Images', image_vars)).grid(row=4, column=0, padx=30, pady=5, sticky='w')

# Videos section
tk.Label(scrollable_frame, text="Videos:", font=('Helvetica', 10, 'bold')).grid(row=5, column=0, padx=10, pady=5, sticky='w')
tk.Checkbutton(scrollable_frame, text="Organize", variable=organize_videos_var).grid(row=6, column=0, padx=30, pady=5, sticky='w')
tk.Label(scrollable_frame, text="Name").grid(row=7, column=0, padx=30, pady=5, sticky='w')
tk.Entry(scrollable_frame, textvariable=video_dir_var, width=50).grid(row=7, column=1, padx=10, pady=5, sticky='w')
tk.Button(scrollable_frame, text="Select Extensions", command=lambda: open_extensions_selector('Videos', video_vars)).grid(row=8, column=0, padx=30, pady=5, sticky='w')

# Documents section
tk.Label(scrollable_frame, text="Documents:", font=('Helvetica', 10, 'bold')).grid(row=9, column=0, padx=10, pady=5, sticky='w')
tk.Checkbutton(scrollable_frame, text="Organize", variable=organize_docs_var).grid(row=10, column=0, padx=30, pady=5, sticky='w')
tk.Label(scrollable_frame, text="Name").grid(row=11, column=0, padx=30, pady=5, sticky='w')
tk.Entry(scrollable_frame, textvariable=doc_dir_var, width=50).grid(row=11, column=1, padx=10, pady=5, sticky='w')
tk.Button(scrollable_frame, text="Select Extensions", command=lambda: open_extensions_selector('Documents', doc_vars)).grid(row=12, column=0, padx=30, pady=5, sticky='w')

# Audio section
tk.Label(scrollable_frame, text="Audio:", font=('Helvetica', 10, 'bold')).grid(row=13, column=0, padx=10, pady=5, sticky='w')
tk.Checkbutton(scrollable_frame, text="Organize", variable=organize_audio_var).grid(row=14, column=0, padx=30, pady=5, sticky='w')
tk.Label(scrollable_frame, text="Name").grid(row=15, column=0, padx=30, pady=5, sticky='w')
tk.Entry(scrollable_frame, textvariable=audio_dir_var, width=50).grid(row=15, column=1, padx=10, pady=5, sticky='w')
tk.Button(scrollable_frame, text="Select Extensions", command=lambda: open_extensions_selector('Audio', audio_vars)).grid(row=16, column=0, padx=30, pady=5, sticky='w')

# Custom folders section
tk.Label(scrollable_frame, text="Custom Folders:", font=('Helvetica', 10, 'bold')).grid(row=17, column=0, padx=10, pady=5, sticky='w')
tk.Button(scrollable_frame, text="Add Custom Folder", command=add_custom_directory).grid(row=17, column=1, padx=10, pady=5, sticky='w')

# Organize button
organize_button = tk.Button(scrollable_frame, text="Organize", command=handle_organize)
organize_button.grid(row=18, column=0, columnspan=3, pady=20)

# Place the canvas and scrollbar in the main window
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Bind the mouse wheel to the canvas for scrolling
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# Start the application
root.mainloop()
