import os

def detect_stack(repo_path):
    files = os.listdir(repo_path)

    if "requirements.txt" in files:
        requirements_path = os.path.join(repo_path, "requirements.txt")
        content = open(requirements_path).read().lower()
        if "flask" in content:
            return "flask"
        else:
            return "python-script"

    if "package.json" in files:
        package_path = os.path.join(repo_path, "package.json")
        content = open(package_path).read().lower()
        if "express" in content:
            return "express"

    if "index.html" in files:
        return "static"

    return "unknown"
