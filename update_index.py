
import os
import yaml
import importlib.util
import sys

def update_index():
  yaml_path = os.path.join('EDITABLE_CONTENT', 'index.yaml')
  if not os.path.exists(yaml_path):
    print('index.yaml not found!')
    return
  with open(yaml_path, 'r', encoding='utf-8') as yf:
    ydata = yaml.safe_load(yf)
  title = ydata.get('title', 'Homepage')
  body = ydata.get('body', '')
  # Import spotlight_projects_list from projects_list.py
  spec_proj = importlib.util.spec_from_file_location('projects_list', os.path.join(os.getcwd(), 'projects_list.py'))
  projects_list = importlib.util.module_from_spec(spec_proj)
  spec_proj.loader.exec_module(projects_list)
  spotlight_projects = projects_list.spotlight_projects_list

  # Import make_project_card from update_site.py
  spec_site = importlib.util.spec_from_file_location('update_site', os.path.join(os.getcwd(), 'update_site.py'))
  update_site = importlib.util.module_from_spec(spec_site)
  sys.modules['projects_list'] = projects_list  # ensure import in update_site works
  spec_site.loader.exec_module(update_site)
  make_project_card = update_site.make_project_card

  # Render body field as plain HTML (no About header)
  html_content = ''
  in_ul = False
  for line in body.split('\n'):
    if line.strip().startswith('- '):
      if not in_ul:
        html_content += '<ul>'
        in_ul = True
      html_content += f'<li>{line.strip()[2:]}</li>'
    else:
      if in_ul and line.strip() == '':
        html_content += '</ul>'
        in_ul = False
      if line.strip():
        html_content += f'<p>{line.strip()}</p>'
  if in_ul:
    html_content += '</ul>'

  # Spotlight projects: use make_project_card for consistent formatting and sort by date (most recent first)
  def get_project_sort_key(project):
    filename = project["file"]
    file_base = filename.replace('.html', '').lower().replace(' ', '_')
    yaml_path = os.path.join('EDITABLE_CONTENT', f'{file_base}.yaml')
    date_str = ""
    if os.path.exists(yaml_path):
      try:
        with open(yaml_path, 'r', encoding='utf-8') as yf:
          ydata = yaml.safe_load(yf)
          date_str = ydata.get('date', "")
      except Exception:
        date_str = ""
    from datetime import datetime
    try:
      sort_date = datetime.strptime(date_str, "%B %d, %Y")
    except Exception:
      sort_date = datetime.min
    return (sort_date, filename.lower())
  sorted_spotlight = sorted(spotlight_projects, key=get_project_sort_key, reverse=True)
  spotlight_html = ''
  if sorted_spotlight:
    cards = '\n'.join([make_project_card(p) for p in sorted_spotlight])
    spotlight_html = f'<section id="spotlight-projects">\n  <h1 class="section-title">Spotlight</h1>\n  <div class="projects-grid">\n    {cards}\n  </div>\n</section>'

    html = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="style.css">
        </head>
        <body>
        <header>
        <div class="header-content" style="flex-direction:column;align-items:center;gap:0;">
        <div class="header-left" style="justify-content:center;width:100%;gap:12px;">
            <div class="logo">
            <img src="assets/images/logo.png" alt="Logo">
            </div>
            <h1 class="site-name">sab18.github.io</h1>
        </div>
        <nav class="menu-container" id="menu" style="width:100%;margin-top:18px;display:flex;justify-content:center;"></nav>
        </div>
        </header>
        <main>
        {html_content}
        {spotlight_html}
        </main>
        <script src="menu_data.js"></script>
        <script src="menu.js"></script>
        </body>
        </html>'''
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated index.html from index.yaml')

if __name__ == '__main__':
    update_index()
