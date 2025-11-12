import os
import yaml

def update_about_page():
    yaml_path = os.path.join('EDITABLE_CONTENT', 'about.yaml')
    if not os.path.exists(yaml_path):
        print('about.yaml not found!')
        return
    with open(yaml_path, 'r', encoding='utf-8') as yf:
        ydata = yaml.safe_load(yf)
    title = ydata.get('title', 'About')
    content = ydata.get('content', '')
    # Convert newlines to <br> and handle lists
    html_content = ''
    for line in content.split('\n'):
        if line.strip().startswith('- '):
            if not html_content.endswith('<ul>'):
                html_content += '<ul>'
            html_content += f'<li>{line.strip()[2:]}</li>'
        else:
            if html_content.endswith('</li>'):
                html_content += '</ul>'
            if line.strip():
                html_content += f'<p>{line.strip()}</p>'
    if html_content.endswith('</li>'):
        html_content += '</ul>'
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
    <section id="about-section">
<h1 class="section-title">{title}</h1>
<div>
{html_content}
</div>
    </section>
  </main>
  <script src="menu_data.js"></script>
  <script src="menu.js"></script>
</body>
</html>'''
    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated about.html from about.yaml')

if __name__ == '__main__':
    update_about_page()
