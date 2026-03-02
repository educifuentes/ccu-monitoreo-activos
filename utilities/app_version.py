import subprocess

def get_app_version():
    try:
        tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode('utf-8').strip()
        return tag
    except Exception:
        return "v1.0.0"
