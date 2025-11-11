import os
from datetime import date
import sys
import shutil

def append_to_projects_list(page_file, list_name, date_str=None):
    """Append the project dict to the specified list in projects_list.py if not already present."""
    projects_list_path = 'projects_list.py'
    with open(projects_list_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Find the list
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith(list_name + "=["):
            start_idx = i
            # Find the closing bracket
            for j in range(i+1, len(lines)):
                if lines[j].strip().startswith("]"):
                    end_idx = j
                    break
            break
    if start_idx is not None and end_idx is not None:
        # Check if already present
        already = any(page_file in l for l in lines[start_idx:end_idx])
        if not already:
            # Insert before closing bracket
            if date_str is None:
                from datetime import date
                date_str = date.today().strftime("%B %d, %Y")
            lines.insert(end_idx, f'    {{"file": "{page_file}", "date": "{date_str}"}},\n')
            with open(projects_list_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Added {page_file} to {list_name} in projects_list.py")
        else:
            print(f"{page_file} already in {list_name}")
    else:
        print(f"Could not find {list_name} in projects_list.py")


def create_portfolio_page(page_name, page_type):
    # 1. Format file and folder names
    file_base = page_name.strip().lower().replace(' ', '_')
    file_name = f"{file_base}.html"
    image_folder = os.path.join("assets", "images", file_base)
    today = date.today().strftime("%B %d, %Y")

    # 2. Create YAML content file for the project
    yaml_path = os.path.join('project_content', f'{file_base}.yaml')
    if not os.path.exists('project_content'):
        os.makedirs('project_content', exist_ok=True)
    if not os.path.exists(yaml_path):
        yaml_content = f"""title: {page_name}
        date: {today}
            abstract: ''
            method: ''
            discussion: ''
            gallery_dir: assets/images/{file_base}
        """
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        print(f"Created {yaml_path}")
    else:
        print(f"YAML content file already exists: {yaml_path}")

    # 3. Create image folder if it doesn't exist
    if not os.path.exists(image_folder):
        os.makedirs(image_folder, exist_ok=True)
        print(f"Created image folder: {image_folder}")
    else:
        print(f"Image folder already exists: {image_folder}")

    # 4. Copy initial_project_header_image.jpg if it doesn't exist in folder
    src_img = "assets/images/initial_project_header_image.jpg"
    dest_img = os.path.join(image_folder, f"{file_base}_header_image.jpg")
    if not os.path.exists(dest_img):
        if os.path.exists(src_img):
            shutil.copyfile(src_img, dest_img)
            print(f"Copied {src_img} to {dest_img}")
        else:
            print(f"{src_img} not found, no header image copied.")
    else:
        print(f"Header image already exists: {dest_img}")

    # 5. Append to correct projects_list.py list if not already present
    added_to_project_list = False
    if page_type in ["irl_projects_list", "digital_projects_list"]:
        projects_list_path = 'projects_list.py'
        with open(projects_list_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        start_idx = None
        end_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith(page_type + "=["):
                start_idx = i
                for j in range(i+1, len(lines)):
                    if lines[j].strip().startswith("]"):
                        end_idx = j
                        break
                break
        already = False
        if start_idx is not None and end_idx is not None:
            already = any(file_name in l for l in lines[start_idx:end_idx])
            if not already:
                lines.insert(end_idx, f'    {{"file": "{file_name}", "date": "{today}"}},\n')
                with open(projects_list_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"Added {file_name} to {page_type} in projects_list.py")
                added_to_project_list = True
            else:
                print(f"{file_name} already in {page_type}")
        else:
            print(f"Could not find {page_type} in projects_list.py")

    # 6. Only append to spotlight_projects_list if not already in designated project list
    if added_to_project_list:
        append_to_projects_list(file_name, "spotlight_projects_list", today)
    else:
        print(f"Not adding {file_name} to spotlight_projects_list (already in project list or not designated)")

if __name__ == "__main__":

    all_prog_dict={
        "Dresser":"irl_projects_list",
        "Backpack":"irl_projects_list",
        "Watch":"irl_projects_list",
        "Tent":"irl_projects_list",
        "Table":"irl_projects_list",
        "Newsletter":"digital_projects_list",
    }

    #delete existing test page if exists
    for page_name in all_prog_dict.keys():
        file_base = page_name.strip().lower().replace(' ', '_')
        file_name = f"{file_base}.html"
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Deleted existing {file_name} for testing.")

    for page_name, page_type in all_prog_dict.items():
        # page_name="Watch"
        # page_type= "irl_projects_list"  #irl_projects_list, digital_projects_list
        create_portfolio_page(page_name, page_type)