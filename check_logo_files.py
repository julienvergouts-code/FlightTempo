import os

res_dir = r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\res'

for root, dirs, files in os.walk(res_dir):
    for f in files:
        if 'restwise' in f.lower() or 'launcher' in f.lower():
            full = os.path.join(root, f)
            size = os.path.getsize(full)
            print(f"{os.path.relpath(full, res_dir)} -> {size} bytes")
