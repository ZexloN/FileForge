from pathlib import Path
import shutil
import sys


# ==========================================
# FileForge
# Automatic File Organizer
# ==========================================

VERSION = "1.0.0"


CATEGORIES = {
    "Images": {
        ".jpg", ".jpeg", ".png", ".gif", ".webp",
        ".bmp", ".svg", ".ico", ".tiff"
    },

    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov",
        ".wmv", ".webm", ".flv"
    },

    "Audio": {
        ".mp3", ".wav", ".flac", ".aac",
        ".ogg", ".m4a", ".wma"
    },

    "Documents": {
        ".pdf", ".doc", ".docx", ".txt",
        ".rtf", ".odt", ".md"
    },

    "Spreadsheets": {
        ".xls", ".xlsx", ".csv", ".ods"
    },

    "Presentations": {
        ".ppt", ".pptx", ".odp"
    },

    "Archives": {
        ".zip", ".rar", ".7z", ".tar",
        ".gz", ".bz2", ".xz"
    },

    "Applications": {
        ".exe", ".msi", ".apk", ".deb",
        ".rpm", ".appimage"
    },

    "Code": {
        ".py", ".js", ".ts", ".html",
        ".css", ".java", ".cpp", ".c",
        ".h", ".cs", ".php", ".json",
        ".xml", ".sql", ".sh", ".bat"
    },

    "Fonts": {
        ".ttf", ".otf", ".woff", ".woff2"
    }
}


def print_banner():
    print()
    print("=" * 50)
    print("              FILEFORGE")
    print("       Automatic File Organizer")
    print("=" * 50)
    print(f"Version {VERSION}")
    print()


def get_category(extension):
    extension = extension.lower()

    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_path(destination):
    """
    Prevent overwriting files with the same name.
    """

    if not destination.exists():
        return destination

    counter = 1

    while True:

        new_name = (
            f"{destination.stem}"
            f"_{counter}"
            f"{destination.suffix}"
        )

        new_path = destination.parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1


def organize_folder(folder):
    folder = Path(folder).expanduser().resolve()

    if not folder.exists():
        print(f"[ERROR] Folder does not exist:")
        print(folder)
        return

    if not folder.is_dir():
        print("[ERROR] The selected path is not a folder.")
        return

    print(f"[INFO] Organizing:")
    print(folder)
    print()

    moved = 0
    skipped = 0

    # Only process files directly inside the selected folder.
    files = [
        item for item in folder.iterdir()
        if item.is_file()
    ]

    if not files:
        print("[INFO] No files found.")
        return

    for file in files:

        # Ignore this script if it is located
        # inside the folder being organized.
        if file.name == Path(__file__).name:
            skipped += 1
            continue

        category = get_category(file.suffix)

        destination_folder = folder / category

        destination_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        destination = (
            destination_folder / file.name
        )

        destination = get_unique_path(destination)

        try:

            shutil.move(
                str(file),
                str(destination)
            )

            print(
                f"[OK] {file.name}"
                f" -> {category}/"
            )

            moved += 1

        except PermissionError:
            print(
                f"[ERROR] Permission denied:"
                f" {file.name}"
            )

            skipped += 1

        except OSError as error:
            print(
                f"[ERROR] Could not move"
                f" {file.name}: {error}"
            )

            skipped += 1

    print()
    print("-" * 50)
    print("Finished!")
    print(f"Moved : {moved}")
    print(f"Skipped: {skipped}")
    print("-" * 50)


def show_categories():
    print()
    print("Supported categories:")
    print()

    for category, extensions in CATEGORIES.items():

        extensions_text = ", ".join(
            sorted(extensions)
        )

        print(
            f"{category:<15} "
            f"{extensions_text}"
        )

    print()


def main():

    print_banner()

    if len(sys.argv) > 1:

        command = sys.argv[1].lower()

        if command in ("--help", "-h"):

            print("Usage:")
            print()
            print("  python fileforge.py")
            print("  python fileforge.py <folder>")
            print("  python fileforge.py --categories")
            print()

            return

        if command in (
            "--categories",
            "-c"
        ):

            show_categories()
            return

        folder = sys.argv[1]

    else:

        print("Enter the folder you want to organize.")
        print("Example: C:\\Users\\User\\Downloads")
        print()

        folder = input("> ").strip()

        if not folder:
            print("[ERROR] No folder selected.")
            return

    print()

    organize_folder(folder)


if __name__ == "__main__":
    main()
