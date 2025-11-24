import subprocess
import sys
import os

def run_script(script):
    print(f'Running {script}...')
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

def main():
    scripts = [
        'z_update_site.py',
        'z_update_about_page.py',
        'z_update_index.py',
        'z_update_project_page.py',
    ]
    for script in scripts:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f'Warning: {script} not found in root directory.')

if __name__ == '__main__':
    main()
