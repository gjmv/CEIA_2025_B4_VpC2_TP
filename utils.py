import requests
import os
from zipfile import ZipFile

def download_dataset(target_dir, subset: str | None = None, force: bool = False):
    dataset_url = "https://www.kaggle.com/api/v1/datasets/download/abdallahalidev/plantvillage-dataset"
    dataset_folder = "plantvillage dataset"
    tmp_file = "tmp.zip"

    if not(subset is None or subset.lower() in ["color", "grayscale", "segmented"]):
        raise Exception("subset debe ser None, color, grayscale o segmented")
    
    if os.path.isdir(target_dir) and not force:
        if subset is None:
            print("Dataset folder already exists, nothing downloaded.")
            return
        if os.path.isdir(os.path.join(target_dir, subset)):
            print(f"Folder already exists for subset \"{subset}\", nothing downloaded.")
            return

    try:
        with requests.get(dataset_url, stream=True) as response:
            response.raise_for_status()  # Raise an exception for bad status codes

            with open(tmp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"File '{tmp_file}' downloaded successfully.")
    except requests.exceptions.RequestException as e:
        if (os.path.isfile(tmp_file)):
            os.remove(tmp_file)
        raise(Exception(f"Error downloading file: {e}"))

    try:
        with ZipFile(tmp_file, 'r') as zip_object:
            for member in zip_object.infolist():
                if member.filename.startswith(dataset_folder):
                    member.filename = member.filename[len(dataset_folder)+1:]
                    if subset is None or member.filename.startswith(subset):
                        zip_object.extract(member, target_dir)
        print(f"Successfully extracted '{tmp_file}' to '{target_dir}' for " + ('all subsets' if subset is None else f"{subset} subset") + ".")

    except FileNotFoundError:
        raise(Exception(f"Error: The file '{tmp_file}' was not found."))
    except Exception as e:
        raise(Exception(f"An error occurred: {e}"))
    finally:
        if (os.path.isfile(tmp_file)):
            os.remove(tmp_file)
