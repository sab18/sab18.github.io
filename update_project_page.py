import os
import yaml
from jinja2 import Template

PROJECT_CONTENT_DIR = 'project_content'
PROJECT_PAGES_DIR = '.'
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
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
        <section>
            <h2 class="section-title">{{ title }}</h2>
            <h3>Date</h3>
            <p>{{ date }}</p>
            <h4>Abstract & Background</h4>
            <p>{{ abstract|safe }}</p>
            <h4>Method & Results</h4>
            <p>{{ method|safe }}</p>
            <h4>Discussion & Learnings</h4>
            <p>{{ discussion|safe }}</p>
            <h4>Gallery</h4>
            <p>Images for this project should be placed in <code>{{ gallery_dir }}</code></p>
        </section>
    </main>
    <script src="menu_data.js"></script>
    <script src="menu.js"></script>
</body>
</html>
'''

def update_project_pages():
    for fname in os.listdir(PROJECT_CONTENT_DIR):
        if fname.endswith('.yaml'):
            with open(os.path.join(PROJECT_CONTENT_DIR, fname), 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            html = Template(TEMPLATE).render(**data)
            html_fname = os.path.join(PROJECT_PAGES_DIR, fname.replace('.yaml', '.html'))
            with open(html_fname, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Updated {html_fname}")

if __name__ == '__main__':
    update_project_pages()
