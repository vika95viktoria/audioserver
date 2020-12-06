import os, logging


def list_all_files_with_ext(ext):
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(ext)]
    files.sort(key=os.path.getctime)
    return files


def delete_file_from_disk(file_path):
    logging.info(f"deleting file {file_path}")
    os.remove(file_path)


def delete_files(files):
    for f in files:
        delete_file_from_disk(f)
