import os
import shutil

def move_all_files_to_current_directory():
    current_dir = os.getcwd()
    
    # Traverse all subdirectories in the current directory
    for root, _, files in os.walk(current_dir):
        # Skip the current directory itself
        if root == current_dir:
            continue
        
        for file in files:
            source_path = os.path.join(root, file)
            
            try:
                # Move file to the current directory
                shutil.move(source_path, current_dir)
                print(f"Moved: {file}")
            except Exception as e:
                print(f"Failed to move {file}: {e}")

move_all_files_to_current_directory()
