import shutil
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class OrganizeFiles:
    """
    This class is used to orgnize files in a directory by
    moving files into directories based on extension.
    """
    def __init__(self, extension_dest:dict=None):
        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extensions_dest = {}
        if extension_dest is None:
            for dir_name, ext_list in ext_dirs.items():
                for ext in ext_list:
                    self.extensions_dest[ext] = dir_name
        else:
            if type(extension_dest) is not dict:
                raise TypeError(f"{extension_dest} is not a dictionary")
            self.extensions_dest = extension_dest


    def __call__(self, directory: Union[str, Path]):
        """Organize files in a directory by moving them
         to sub directories based on extensions.
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory} does not exist")

        logger.info(f"Organizeing files in {directory} ...")
        file_extensions = []

        for file_path in directory.iterdir():

            # ignore directories
            if file_path.is_dir():
                continue

            # ignore hidden files
            if file_path.name.startswith('.'):
                continue

            # move files
            file_extensions.append(file_path.suffix)
            if file_path.suffix not in self.extensions_dest:
                DEST_DIR = directory / 'other'
            else:
                DEST_DIR = directory / self.extensions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f"Moving {file_path} to {DEST_DIR} ...")
            shutil.move(str(file_path), str(DEST_DIR))



if __name__ == "__main__":
    org_files = OrganizeFiles()
    org_files('/mnt/c/Users/OMID/Downloads/Telegram Desktop')
    logger.info("Done!")
