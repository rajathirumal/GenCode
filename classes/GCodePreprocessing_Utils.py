from tqdm import tqdm
import os


class GCodePreprocessingUtils:
    def __init__(self, source: str) -> None:
        self.sourcefolder = source

    def _calculate_file_size(self, size_in_bytes):
        """
        Translates a byte info into KB, MB and GB.
        """
        size_in_kb = size_in_bytes / 1024
        size_in_mb = size_in_kb / 1024
        size_in_gb = size_in_mb / 1024
        # print(size_in_kb, size_in_mb, size_in_gb)
        return (size_in_kb, size_in_mb, size_in_gb)

 
    def folder_metrics(self ,folder_list: list,batch_number:int):
        """ This retruns a dictionary where the key is the Full path of each files and the valu is a 3-tuple (size in kb, size in mb, size in GB)

        Note: This will ignore the `.git`, `.DS_Store` files/folders if any 
        """
        folder_info: dict = {}

        pwd = os.path.join(os.getcwd(),self.sourcefolder) 
        for folder_name in tqdm(folder_list,desc=f"Running {batch_number}th batch"):
            IGNORABLE = ['.DS_Store','.git']
            folder_path = os.path.join(pwd,folder_name)
            for root, dirs, files in os.walk(folder_path):
                for file_name in files:
                    if not "." in file_name:
                        continue
                    file_path = os.path.join(root, file_name)
                    if any(ignored in file_path for ignored in IGNORABLE):
                        continue
                    else:
                        folder_info[file_path] = self._calculate_file_size(os.path.getsize(file_path))
                        # file_paths.append(file_path)
        return folder_info

def main():
    GUtils = GCodePreprocessingUtils(source="download")
    GUtils.scan_files(scanFilesUnder="download")

if __name__ == "__main__":
    main()