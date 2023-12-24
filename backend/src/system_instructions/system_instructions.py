import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# List of system instruction text files
system_messages = {
    "Outliner": os.path.join(base_dir, 'the_outliner.txt'),
    "Drafter": os.path.join(base_dir, 'the_drafter.txt'),
    "Editor": os.path.join(base_dir, 'the_editor.txt'),
}

for key, file_path in system_messages.items():
    with open(file_path, 'r') as file:
        system_messages[key] = file.read()