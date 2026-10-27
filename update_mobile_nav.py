import re

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\assets\restwise-prototype.html', 'r', encoding='utf-8') as f:
    html = f.read()

nav_idx = html.find('<nav class="mobile-nav"')
if nav_idx != -1:
    end_idx = html.find('</nav>', nav_idx)
    nav_content = html[nav_idx:end_idx]

    if 'data-page="sleep"' not in nav_content:
        # Depending on how the newlines break, we just replace data-page="schedule"
        nav_content = nav_content.replace('data-page="schedule"', 'data-page="sleep"><span>☾</span>Sleep</button><button data-page="schedule"')
        html = html[:nav_idx] + nav_content + html[end_idx:]

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\assets\restwise-prototype.html', 'w', encoding='utf-8') as f:
    f.write(html)
