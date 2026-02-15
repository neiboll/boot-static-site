import os
import shutil

source_path = "static"
filename = "index.css"


def copy_files_recursive(source_path, dest_path):
    for filename in os.listdir(source_path):
        from_path = os.path.join(source_path, filename)
        to_path = os.path.join(dest_path, filename)
        print(f" * {from_path} -> {to_path}")

        if os.path.isfile(from_path):
            copy = shutil.copy(from_path, to_path)
        else:
            print("It's a directory") 
            os.mkdir(to_path)
            copy_files_recursive(from_path, to_path)



    
