import json
import os
import urllib.request


def main() -> None:
    url = "https://raw.githubusercontent.com/iconify/icon-sets/master/json/lucide.json"
    print(f"Downloading Lucide icons from: {url} ...")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching icons: {e}")
        return

    print("Successfully downloaded icon data.")

    # Extraire les corps SVG pour chaque icône
    # Le format d'Iconify JSON contient :
    # {
    #   "prefix": "lucide",
    #   "icons": {
    #     "home": { "body": "<path .../>" },
    #     ...
    #   }
    # }
    import re

    icons_dict = {}
    for name, icon_info in data.get("icons", {}).items():
        if "body" in icon_info:
            body = icon_info["body"]
            # Strip default styling attributes so they inherit from the parent <svg>
            body = re.sub(r"\s+fill=\"[^\"]*\"", "", body)
            body = re.sub(r"\s+stroke=\"[^\"]*\"", "", body)
            body = re.sub(r"\s+stroke-width=\"[^\"]*\"", "", body)
            body = re.sub(r"\s+stroke-linecap=\"[^\"]*\"", "", body)
            body = re.sub(r"\s+stroke-linejoin=\"[^\"]*\"", "", body)
            icons_dict[name] = body

    # Extraire et résoudre les alias (ex: home -> house)
    for alias_name, alias_info in data.get("aliases", {}).items():
        parent = alias_info.get("parent")
        if parent in icons_dict:
            icons_dict[alias_name] = icons_dict[parent]


    print(f"Processed {len(icons_dict)} icons (including aliases).")

    # Enregistrer dans le dossier data de la bibliothèque
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "asok_lucide", "data")
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "lucide-icons.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(icons_dict, f, indent=2)

    print(f"Saved icons dictionary to: {output_path}")


if __name__ == "__main__":
    main()
