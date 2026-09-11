import os
import glob
import re

STATION_DIR = "app/templates/station"

REPLACEMENTS = [
    # Explicit texts to replace
    (r"Bharati Modular Core", r"{{ station.name }} Modular Core"),
    (r"Larsemann Hills \(Bharati Station\)", r"{{ station.region }} ({{ station.name }} Station)"),
    (r"AWS-01 \(Bharati Primary\)", r"AWS-01 ({{ station.name }} Primary)"),
    (r"Bharati Station", r"{{ station.name }} Station"),
    (r"BHARATI-CORE", r"{{ station.name|upper }}-CORE"),
    # Broad replacements
    (r"\bBharati\b", r"{{ station.name }}"),
    (r"\bBHARATI\b", r"{{ station.name|upper }}"),
    (r"Larsemann Hills", r"{{ station.region }}"),
    (r"hydraulic stilts", r"{{ station.foundation }}"),
]

for filename in glob.glob(os.path.join(STATION_DIR, "*.html")):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    for pattern, repl in REPLACEMENTS:
        content = re.sub(pattern, repl, content)

    if content != original_content:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filename}")
