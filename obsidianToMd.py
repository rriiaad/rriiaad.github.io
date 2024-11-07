import os
import re

def update_image_paths_in_md(file_path):
    # Read the content of the markdown file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define a regex pattern to match the image syntax and capture the image name
    pattern = r'!\[\[(Pasted image [\d]+\.png)\]\]'
    
    # Replace with the new format
    updated_content = re.sub(
        pattern,
        r'![img-description](assets/img/screenshots/\1)',
        content
    )

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    print(f"Updated image paths in {file_path}")

# Define the folder containing .md files
folder_path = '_posts'  

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.md'):
        file_path = os.path.join(folder_path, filename)
        update_image_paths_in_md(file_path)
