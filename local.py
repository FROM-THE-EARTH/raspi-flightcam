
from os.path import join, expanduser, abspath, exists
import shutil
import sys


def main(path_pkg: str, path_site: str):
    if exists(path_site):
        shutil.rmtree(path_site)

    shutil.copytree(path_pkg, path_site)
    
    
if __name__ == "__main__":
    
    name_pkg = sys.argv[1]
    path_pkg = abspath(name_pkg)
    name_env = sys.argv[2]
    version_python = "3.8"
    path_site = join(expanduser("~"),
                    ".local",
                    "share",
                    "virtualenvs",
                    name_env,
                    "lib",
                    "python" + version_python, 
                    "site-packages", 
                    name_pkg)

    main(path_pkg, path_site)
