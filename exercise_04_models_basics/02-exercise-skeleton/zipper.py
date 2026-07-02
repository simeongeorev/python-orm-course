import os
import zipfile

# Configuration
ZIP_NAME = "project.zip"

# 1. Use lowercase or exact matches for folders you want to skip completely
EXCLUDE_DIRS = {
    ".idea", ".venv", "__pycache__", ".git", ".pytest_cache", 
    "build", "dist", "node_modules"
}

# 2. Exclude specific files or file extensions you don't want
EXCLUDE_FILES = {ZIP_NAME, "zip_project.py", ".DS_Store"}
EXCLUDE_EXTENSIONS = {".pyc", ".pyo", ".zip", ".tar.gz"}

def create_zip():
    # Automatically overwrites the file if it already exists
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Modifying dirs in-place tells os.walk to completely skip entering excluded folders
            # Added .lower() check to make it case-insensitive (e.g., catching "Build" vs "build")
            dirs[:] = [d for d in dirs if d.lower() not in EXCLUDE_DIRS and d not in EXCLUDE_DIRS]
            
            for file in files:
                # Skip explicit files or matching extensions
                if file in EXCLUDE_FILES or os.path.splitext(file)[1] in EXCLUDE_EXTENSIONS:
                    continue
                    
                file_path = os.path.join(root, file)
                # Determine the path inside the zip file (relative to current directory)
                arc_name = os.path.relpath(file_path, '.')
                
                zipf.write(file_path, arc_name)
                
    # FIXED: Removed the invalid 'cls=' keyword argument which causes a TypeError
    print(f"Successfully created {ZIP_NAME}!")

if __name__ == "__main__":
    create_zip()