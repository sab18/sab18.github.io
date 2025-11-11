import os
from datetime import date
import sys
import shutil
import yaml

HTML_TEMPLATE = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <header>
            <div class="header-content">
                <div class="header-left">
                    <div class="logo">
                        <img src="assets/images/logo.jpg" alt="Logo">
                    </div>
                    <h1 class="site-name">sab18.github.io</h1>
                </div>
                <nav class="menu-container" id="menu"></nav>
            </div>
        </header>
    <main>
            <section>
                <h2 class="section-title">{title}</h2>
                <h3>Date</h3>
                <p>{date}</p>
                <h4>Abstract & Background</h4>
                <p>{abstract}</p>
                <h4>Method & Results</h4>
                <p>{method}</p>
                <h4>Discussion & Learnings</h4>
                <p>{discussion}</p>
                <h4>Gallery</h4>
                <p>Images for this project should be placed in <code>{gallery_dir}</code></p>
            </section>
        </main>
        <script src="menu_data.js"></script>
        <script src="menu.js"></script>
    </body>
    </html>
'''

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
        # Build a proper YAML structure and write it using PyYAML to avoid
        # indentation/formatting issues from a hand-rolled multi-line string.
        yaml_data = {
            "title": page_name,
            "date": today,
            "abstract": "",
            "method": "",
            "discussion": "",
            "gallery_dir": f"assets/images/{file_base}",
        }
        try:
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(yaml_data, f, sort_keys=False, default_flow_style=False)
            print(f"Created {yaml_path}")
        except Exception as e:
            print(f"Failed to write YAML to {yaml_path}: {e}")
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

    # 5. Create/overwrite the project's HTML page based on metadata
    # Load the YAML we just created (or existing) to populate the HTML
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            meta = yaml.safe_load(f) or {}
    except Exception:
        meta = {}

    # Use comment placeholders if values are empty
    abstract_html = meta.get('abstract') if meta.get('abstract') else '<!-- Write your abstract and background here -->'
    method_html = meta.get('method') if meta.get('method') else '<!-- Write your methods and results here -->'
    discussion_html = meta.get('discussion') if meta.get('discussion') else '<!-- Write your discussion and learnings here -->'
    gallery_dir = meta.get('gallery_dir', f"assets/images/{file_base}")
    # Match the sample's backslash style on Windows for display
    gallery_display = gallery_dir.replace('/', '\\') if os.name == 'nt' else gallery_dir

    html_content = HTML_TEMPLATE.format(
        title=page_name,
        date=meta.get('date', today),
        abstract=abstract_html,
        method=method_html,
        discussion=discussion_html,
        gallery_dir=gallery_display,
    )

    html_fname = os.path.join('.', f"{file_base}.html")
    try:
        with open(html_fname, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Wrote HTML page: {html_fname}")
    except Exception as e:
        print(f"Failed to write HTML page {html_fname}: {e}")

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