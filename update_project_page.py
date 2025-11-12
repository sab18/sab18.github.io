import os
import yaml
import os
import yaml
from jinja2 import Template

PROJECT_CONTENT_DIR = 'EDITABLE_CONTENT'
PROJECT_PAGES_DIR = '.'
TEMPLATE = r'''<!DOCTYPE html>
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
            <h2 class="section-title" style="margin-bottom:0;">{{ title }}</h2>
            <div class="project-date" style="margin-bottom:12px;margin-top:2px;">{{ date }}</div>
            {% if main_image %}
            <div style="height:32px;"></div>
            <div style="margin-bottom:56px;text-align:left;">
                <img src="{{ main_image }}" alt="{{ title }} main image" style="max-width:320px;max-height:220px;object-fit:contain;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;">
            </div>
            {% endif %}
            <h4>Abstract & Background</h4>
            <p>{{ abstract|safe }}</p>
            <div style="height:18px;"></div>
            <h4>Method & Results</h4>
            <p>{{ method|safe }}</p>
            <div style="height:18px;"></div>
            <h4>Discussion & Learnings</h4>
            <p>{{ discussion|safe }}</p>
            <div style="height:18px;"></div>
            <h4>Gallery</h4>
            <p>Images for this project should be placed in <code>{{ gallery_dir }}</code></p>
        </section>
    </main>
    <script src="menu_data.js"></script>
    <script src="menu.js"></script>
    <!-- Figure numbering script removed: captions are expected to contain the desired text (e.g., "Figure 1a"). -->
</body>
</html>
'''


def update_project_pages():
    for fname in os.listdir(PROJECT_CONTENT_DIR):
        if fname.endswith('.yaml') and fname not in ('about.yaml', 'index.yaml'):
            with open(os.path.join(PROJECT_CONTENT_DIR, fname), 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            file_base = fname.replace('.yaml', '')
            gallery_dir = data.get('gallery_dir', '')
            main_image = None
            if gallery_dir:
                header_img = os.path.join(gallery_dir, f'{file_base}_header_image.jpg')
                if os.path.exists(header_img):
                    main_image = header_img.replace('\\', '/').replace('\\', '/')
                else:
                    try:
                        imgs = [f for f in os.listdir(gallery_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
                        if imgs:
                            main_image = os.path.join(gallery_dir, imgs[0]).replace('\\', '/').replace('\\', '/')
                    except Exception:
                        pass
            # Always render HTML, even if no image is found
            html = Template(TEMPLATE).render(**data, main_image=main_image)
            html_fname = os.path.join(PROJECT_PAGES_DIR, fname.replace('.yaml', '.html'))
            with open(html_fname, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Updated {html_fname}")

if __name__ == '__main__':
    update_project_pages()


