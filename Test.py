class TreeNode:
    def __init__(self, name, is_file=False, parent=None):
        self.name = name
        self.is_file = is_file
        self.children = []
        self.parent = parent

def create_file_system():
    return TreeNode("Root Folder")

# Basic Display menu 
def display_menu():
    print("\nFile Management System Menu:")
    print("------------------------------")
    print("1. Display current directory")
    print("2. List files and subdirectories")
    print("3. Change directory")
    print("4. Create file")
    print("5. Create directory")
    print("6. Go back to previous directory")
    print("7. Rename file/directory")
    print("8. Exit")

def display_current_directory(node):
    path = get_full_path(node)
    print("Current Directory:", path) 

# Function to display files and directories 
def list_files_and_directories(node):
    print("\nFiles and Subdirectories:")
    for child in node.children:
        if child.is_file:
            print(f"File: {child.name}")
        else:
            print(f"Directory: {child.name}")

# Function to change the directory
def change_directory(current_node, target_directory):
    if target_directory == "..":
        return current_node.parent if current_node.parent else current_node

    for child in current_node.children:
        if not child.is_file and child.name == target_directory:
            return child

    raise ValueError(f"{target_directory} not found.")

# creating a basic text file
def create_file(current_node, file_name):
    if '.' in file_name:
        raise ValueError("sInvalid file name. A '.txt' extension will be added automatically.")

    if not file_name.strip():
        raise ValueError("Invalid file name.")

    file_name += '.txt'

    existing_file = next((child for child in current_node.children if child.is_file and child.name == file_name), None)
    
    if existing_file:
        replace_choice = input(f"File '{file_name}' already exists. Do you want to replace it? (yes/no): ").lower()
        if replace_choice != 'yes':
            print("File creation aborted.")
            return
        else:
            current_node.children.remove(existing_file)
            print(f"File '{file_name}' replaced successfully in {get_full_path(current_node)}.")

    new_file = TreeNode(file_name, is_file=True, parent=current_node)
    current_node.children.append(new_file)
    print(f"Text file {file_name} created successfully in {get_full_path(current_node)}.")

#Recursive function to create new directory
def create_directory_recursive(current_node, path_components, index=0):
    if index == len(path_components):
        return current_node

    directory_name = path_components[index]
    found_directory = next((child for child in current_node.children if not child.is_file and child.name == directory_name), None)

    if found_directory is None:
        new_directory = TreeNode(directory_name, parent=current_node)
        current_node.children.append(new_directory)
        found_directory = new_directory

    return create_directory_recursive(found_directory, path_components, index + 1)

def create_directory(current_node, path):
    path_components = path.split("/")
    if path_components[0] == '':
        path_components = path_components[1:]

    create_directory_recursive(current_node, path_components)
    print(f"Directory {path} created successfully.")

def rename_file_or_directory(current_node, old_name, new_name):
    is_file = any(child.name == old_name and child.is_file for child in current_node.children)
    
    for child in current_node.children:
        if child.name == old_name:
            if is_file:
                _, extension = old_name.rsplit('.', 1)
                new_name += f".{extension}"
                
            child.name = new_name
            print(f"Successfully renamed {old_name} to {new_name} in {get_full_path(current_node)}.")
            return
    raise ValueError(f"{old_name} not found in the current directory.")

def get_full_path(node):
    path_components = []
    while node:
        path_components.insert(0, node.name)
        node = node.parent
    return "/" + "/".join(path_components)

def file_management_system(current_node):
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                display_current_directory(current_node)
            elif choice == '2':
                list_files_and_directories(current_node)
            elif choice == '3':
                target_directory = input("Enter the directory name to change: ")
                current_node = change_directory(current_node, target_directory)
            elif choice == '4':
                file_name = input("Enter the file name to create: ")
                create_file(current_node, file_name)
            elif choice == '5':
                directory_name = input("Enter the directory name to create: ")
                create_directory(current_node, directory_name)
            elif choice == '6':
                current_node = current_node.parent if current_node.parent else current_node
                print(f"Moved to the parent directory: {get_full_path(current_node)}")
            elif choice == '7':
                old_name = input("Enter the current name of the file or directory: ")
                new_name = input("Enter new name : ")
                rename_file_or_directory(current_node, old_name, new_name)
            elif choice == '8':
                print("Exiting File Management")
                break
            else:
                print("Invalid Choice!!!")
        except ValueError as e:
            print(f"{e}")


if __name__ == "__main__":
    file_system_root = create_file_system()
    current_directory = file_system_root
    file_management_system(current_directory)
