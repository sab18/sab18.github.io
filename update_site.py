import os
import yaml
from projects_list import menu_list, irl_projects_list, digital_projects_list, spotlight_projects_list

def make_label(filename):
    label = filename.replace('.html', '').replace('_', ' ')
    # Always capitalize IRL
    label = label.replace('Irl', 'IRL').replace('irl', 'IRL')
    # Use 'Spotlight' not 'Spotlight Projects'
    if label.strip().lower() == 'spotlight projects':
        label = 'Spotlight'
    # Use 'Homepage' for index.html
    if filename.strip().lower() == 'index.html':
        return 'Homepage'
    return label.title().replace('Irl', 'IRL')

def make_project_card(project):
    # project is a dict: {"file": ...}
    filename = project["file"]
    file_base = filename.replace('.html', '').lower().replace(' ', '_')
    img_path = f"assets/images/{file_base}/{file_base}_header_image.jpg"
    label = make_label(filename)
    # Read date from YAML file if it exists
    yaml_path = os.path.join('project_content', f'{file_base}.yaml')
    date_str = ""
    if os.path.exists(yaml_path):
        try:
            with open(yaml_path, 'r', encoding='utf-8') as yf:
                ydata = yaml.safe_load(yf)
                date_str = ydata.get('date', "")
        except Exception:
            date_str = ""
    img_tag = f'<img src="{img_path}" alt="{label} header" class="project-image">' if os.path.exists(img_path) else ''
    date_html = f'<div class="project-date">{date_str}</div>' if date_str else ''
    return f'<a href="{filename}" class="project-card">{img_tag}<div class="project-name">{label}{date_html}</div></a>'

def update_menu_js():
    menu_js = 'const menuList = [\n' + \
        ',\n'.join([f'  {{ file: "{f}", label: "{make_label(f)}" }}' for f in menu_list]) + '\n];\n'
    with open('menu_data.js', 'w', encoding='utf-8') as f:
        f.write(menu_js)
    print('Updated menu_data.js')

def update_projects_page(page, projects):
    # Sort projects by date (oldest first), then by project name if dates are equal
    def get_project_sort_key(project):
        filename = project["file"]
        file_base = filename.replace('.html', '').lower().replace(' ', '_')
        yaml_path = os.path.join('project_content', f'{file_base}.yaml')
        date_str = ""
        if os.path.exists(yaml_path):
            try:
                import yaml
                with open(yaml_path, 'r', encoding='utf-8') as yf:
                    ydata = yaml.safe_load(yf)
                    date_str = ydata.get('date', "")
            except Exception:
                date_str = ""
        # Parse date as YYYY-MM-DD for sorting, fallback to empty string
        from datetime import datetime
        try:
            sort_date = datetime.strptime(date_str, "%B %d, %Y")
        except Exception:
            sort_date = datetime.min
        return (sort_date, make_label(filename).lower())

    # Only sort for IRL and Digital Projects pages
    if page in ["irl_projects.html", "digital_projects.html"]:
        sorted_projects = sorted(projects, key=get_project_sort_key)
    else:
        sorted_projects = projects
    cards = '\n'.join([make_project_card(p) for p in sorted_projects])
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{make_label(page)}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="header-content">
            <div class="header-left">
                <div class="logo">
                    <img src="assets/images/logo.png" alt="Logo">
                </div>
                <h1 class="site-name">sab18.github.io</h1>
            </div>
            <nav class="menu-container" id="menu"></nav>
        </div>
    </header>
    <main>
        <h1 class="section-title">{make_label(page)}</h1>
        <div class="projects-grid">
            {cards}
        </div>
    </main>
    <script src="menu_data.js"></script>
    <script src="menu.js"></script>
</body>
</html>'''
    with open(page, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Updated {page}')

def inject_spotlight_section_into_index():
    # Read index.html
    if not os.path.exists('index.html'):
        print('index.html not found!')
        return
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Generate spotlight section HTML
    cards = '\n'.join([make_project_card(p) for p in spotlight_projects_list])
    spotlight_html = f'<section id="spotlight-projects">\n  <h1 class="section-title">Spotlight</h1>\n  <div class="projects-grid">\n    {cards}\n  </div>\n</section>'
    # Replace or insert the spotlight section
    import re
    if '<section id="spotlight-projects">' in content:
        # Replace existing
        content = re.sub(r'<section id="spotlight-projects">.*?</section>', spotlight_html, content, flags=re.DOTALL)
    else:
        # Insert after <body>
        content = content.replace('<body>', '<body>\n' + spotlight_html, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Injected Spotlight Projects section into index.html')

def main():
    update_menu_js()
    update_projects_page('irl_projects.html', irl_projects_list)
    update_projects_page('digital_projects.html', digital_projects_list)
    inject_spotlight_section_into_index()

if __name__ == '__main__':
    main()
