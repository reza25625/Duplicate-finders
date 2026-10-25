import os
import hashlib
from datetime import datetime
import shutil

def list_file(file_path):
    all_files = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            full_files = os.path.join(root, file)
            all_files.append(full_files)

    return all_files

# print(list_file("/home/mohamadreza/tf_env"))
# folder_path = "fileManagmenet.py"
# print(os.path.exists(folder_path))

def get_file_hash(file_path):
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(8192)
            while chunk:
                hasher.update(chunk)
                chunk = file.read(8192)
        return hasher.hexdigest()

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def find_duplicates(folder_path):
    all_files = list_file(folder_path)
    hash_map = {}

    for file_path in all_files:
        file_hash = get_file_hash(file_path)
        if file_hash:
            if file_hash not in hash_map:
                hash_map[file_hash] = []
            hash_map[file_hash].append(file_path)

    duplicates = {}
    for file_hash, paths in hash_map.items():
        if len(paths) > 1 :
            duplicates[file_hash] = paths

    return duplicates


def save_duplicates_report(duplicates, filename ="duplicates_report.txt"):
    with open(filename, "w") as file:
        file.write("=== Duplicate file reports ===\n")
        file.write(f"Date time {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        file.write(f"Number of group {len(duplicates)}\n")
        file.write("=" * 40 + "\n\n")

        total_files = 0
        for i,(file_hash, path) in enumerate(duplicates.items(), 1):
            file.write(f"Group {i} ({len(path)} files):\n")
            for p in path:
                file.write(f"  - {p}\n")
            file.write("\n")
            total_files += len(path)
    print(f"Report save to the {filename}")


def move_duplicates(duplicates, target_folder="duplicates"):
    import os
    os.makedirs(target_folder, exist_ok=True)

    moved_count = 0
    for file_hash, paths in duplicates.items():
        # Take the first, and terasfer they Others
        for p in paths[1:]:
            filename = os.path.basename(p)
            new_path = os.path.join(target_folder, filename)

            # If name is repated, give nuber to them
            counter = 1
            while os.path.exists(new_path):
                name, ext = os.path.splitext(filename)
                new_path = os.path.join(target_folder, f"{name}_{counter}{ext}")
                counter +=1

            shutil.move(p, new_path)
            moved_count += 1

    print(f"Move {moved_count} files to {target_folder}/")

folder = "/home/mohamadreza/tf_env/fileManagmenet/"

dups = find_duplicates(folder)

if dups:
    print(f"Found {len(dups)} groups of duplicated files.")
    for file_hash, path in dups.items():
        print(f"\n -- Groups --")
        for p in path:
            print(p)

else:
    print("No duplicated found")

#Save Reports
save_duplicates_report(dups)
move_duplicates(dups)
