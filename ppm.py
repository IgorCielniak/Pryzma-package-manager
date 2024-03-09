import os
import json
import argparse
import urllib.request
import shutil
import zipfile

class PackageManager:
    def __init__(self):
        self.user_packages_path = "C:/packages"
        self.package_urls = {
            "math": "https://github.com/IgorCielniak/Pryzma-packages/archive/refs/heads/math.zip",
            "std": "https://github.com/IgorCielniak/Pryzma-packages/archive/refs/heads/std.zip"
            # Add more package name-URL associations as needed
        }

    def initialize_repository(self):
        if not os.path.exists(self.user_packages_path):
            os.makedirs(self.user_packages_path)
            print("Repository initialized at:", self.user_packages_path)
        else:
            print("Repository already exists at:", self.user_packages_path)

    def add_package(self, package_name, package_version, package_files):
        package_dir = os.path.join(self.user_packages_path, package_name)
        package_metadata = {
            "name": package_name,
            "version": package_version,
            "files": package_files
        }

        if not os.path.exists(package_dir):
            os.makedirs(package_dir)
        with open(os.path.join(package_dir, "metadata.json"), "w") as metadata_file:
            json.dump(package_metadata, metadata_file)
        for file in package_files:
            with open(os.path.join(package_dir, file), "w") as f:
                pass
        print("Package", package_name, "added successfully.")

    def remove_package(self, package_name):
        package_dir = os.path.join(self.user_packages_path, package_name)
        if os.path.exists(package_dir):
            shutil.rmtree(package_dir)
            print("Package", package_name, "removed successfully.")
        else:
            print("Package", package_name, "not found.")

    def list_packages(self):
        packages = os.listdir(self.user_packages_path)
        print("Available packages:")
        for package in packages:
            print("-", package)

    def install_package(self, package_name):
        package_url = self.package_urls.get(package_name)
        if package_url:
            print("Downloading package:", package_name)
            package_file_path = os.path.join(self.user_packages_path, package_name + ".zip")
            urllib.request.urlretrieve(package_url, package_file_path)
            with zipfile.ZipFile(package_file_path, 'r') as zip_ref:
                zip_ref.extractall(self.user_packages_path)
            os.remove(package_file_path)
            print("Package", package_name, "downloaded and installed successfully.")
        else:
            print("Package", package_name, "not found in the repository.")

    def update_package(self, package_name=None):
        if package_name:
            self.install_package(package_name)
        else:
            packages = os.listdir(self.user_packages_path)
            for package in packages:
                self.install_package(package)

    def prompt_download_dependencies(self, dependencies):
        print("This package has the following dependencies:")
        for dependency in dependencies:
            print("-", dependency)
        response = input("Do you want to download these dependencies? (yes/no): ").lower()
        if response == "yes":
            for dependency in dependencies:
                self.install_package(dependency)
        else:
            print("Dependencies not downloaded.")

    def get_package_index_url(self, package_name):
        package_url = self.package_urls.get(package_name)
        if package_url:
            return package_url
        else:
            print("Failed to determine package index URL for package", package_name)
            return None
        
    import os

    def delete_prefix(self, directory_path):
        # Check if the specified directory exists
        if not os.path.exists(directory_path):
            return
        
        # List all directories in the specified directory
        directories = os.listdir(directory_path)
        
        # Iterate through each directory
        for dir_name in directories:
            # Check if the directory starts with 'gg'
            if dir_name.startswith("Pryzma-packages-"):
                # Get the full path of the directory
                full_path = os.path.join(directory_path, dir_name)
                # Check if it's a directory
                if os.path.isdir(full_path):
                    # Remove 'gg' prefix
                    new_name = dir_name[16:]
                    # Construct the new path with the modified directory name
                    new_full_path = os.path.join(directory_path, new_name)
                    # Rename the directory
                    os.rename(full_path, new_full_path)


def main():
    parser = argparse.ArgumentParser(description="Package Manager")
    parser.add_argument("command", choices=["init", "add", "remove", "list", "install", "update"], help="Action to perform")
    parser.add_argument("package_name", nargs="?", help="Name of the package")
    parser.add_argument("package_version", nargs="?", help="Version of the package")
    parser.add_argument("package_files", nargs="*", help="Files in the package")
    args = parser.parse_args()

    pm = PackageManager()

    if args.command == "init":
        pm.initialize_repository()
    elif args.command == "add":
        if not args.package_version or not args.package_files:
            print("Error: You need to specify package version and files.")
        else:
            pm.add_package(args.package_name, args.package_version, args.package_files)
    elif args.command == "remove":
        pm.remove_package(args.package_name)
        pm.delete_prefix("C:/packages/")
    elif args.command == "list":
        pm.list_packages()
    elif args.command == "install":
        pm.install_package(args.package_name)
        pm.delete_prefix("C:/packages/")
    elif args.command == "update":
        pm.update_package(args.package_name)
        pm.delete_prefix("C:/packages/")


if __name__ == "__main__":
    main()
