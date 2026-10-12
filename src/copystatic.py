import os
import shutil


def delete_dest(destination):
    shutil.rmtree(destination, ignore_errors=True)
    os.mkdir(destination)


def copystatic(source, destination):
    for item in os.listdir(source):
        if os.path.isfile(os.path.join(source, item)):
            print(f"moving {item} from {source} to {destination}")
            shutil.copy(os.path.join(source, item), destination)

        else:
            os.mkdir(os.path.join(destination, item))
            copystatic(os.path.join(source, item), os.path.join(destination, item))
