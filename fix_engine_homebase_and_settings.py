with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Pass homeBase = homeBaseIata to buildDualCurveTimeline and evaluateNextDutyAlertness
text = text.replace("homeBaseIata = homeBaseIata", "homeBase = homeBaseIata")

# 2. Fix SettingsSectionBody definition and call
# Let's inspect SettingsSectionBody in MainActivity.kt
import re

# Add parameters to SettingsSectionBody call
old_call = """                                    homeCommuteDraft = homeCommuteDraft,
                                    onHomeCommuteChange = { homeCommuteDraft = it }," """

# Let's check how SettingsSectionBody is called around line 1628
# Let's read lines 1610 to 1640 of MainActivity.kt
with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(1610, min(1645, len(lines))):
    print(f"{idx+1}: {lines[idx]}", end="")
