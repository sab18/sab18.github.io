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
        'update_about_page.py',
        'update_index.py',
        'update_project_page.py',
        'update_site.py',
    ]
    for script in scripts:
        if os.path.exists(script):
            run_script(script)
        else:
            print(f'Warning: {script} not found in root directory.')

if __name__ == '__main__':
    main()
