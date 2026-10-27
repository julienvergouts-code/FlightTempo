from PIL import Image
import os

res_dir = r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\res'
source_3d_png = os.path.join(res_dir, 'drawable', 'restwise_logo_3d.png')

if os.path.exists(source_3d_png):
    img = Image.open(source_3d_png)
    width, height = img.size
    print(f"Original size: {width}x{height}")

    # Crop top 82% of the image to keep ONLY the 3D dial mark and remove bottom RESTWISE text
    cropped = img.crop((0, 0, width, int(height * 0.825)))

    # Save cropped dial mark as restwise_mark.png
    target_mark_png = os.path.join(res_dir, 'drawable-nodpi', 'restwise_mark.png')
    cropped.save(target_mark_png)

    # Also save as restwise_dial.png in drawable/
    target_dial_png = os.path.join(res_dir, 'drawable', 'restwise_dial.png')
    cropped.save(target_dial_png)

    print(f"Cropped size: {cropped.size}, saved successfully!")
