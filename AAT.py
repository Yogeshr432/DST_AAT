class TreeNode:
    def __init__(self, name, is_file=False, parent=None):
        self.name = name
        self.is_file = is_file
        self.children = []
        self.parent = parent

def create_file_system():
    return TreeNode("Root")

def display_menu():
    print("\nFile Management System Menu:")
    print("1. Display current directory")
    print("2. List files and subdirectories")
    print("3. Change directory")
    print("4. Create file")
    print("5. Create directory")
    print("6. Go back to previous directory")
    print("7. Exit")

def display_current_directory(node):
    path = get_full_path(node)
    print("Current Directory:", path) 

def list_files_and_directories(node):
    print("\nFiles and Subdirectories:")
    for child in node.children:
        if child.is_file:
            print(f"File: {child.name}")
        else:
            print(f"Directory: {child.name}")

def change_directory(current_node, target_directory):
    if target_directory == "..":
        return current_node.parent if current_node.parent else current_node

    for child in current_node.children:
        if not child.is_file and child.name == target_directory:
            return child

    print(f"Error: {target_directory} not found.")
    return current_node

def create_file(current_node, file_name):
    new_file = TreeNode(file_name, is_file=True, parent=current_node)
    current_node.children.append(new_file)
    print(f"File {file_name} created successfully in {get_full_path(current_node)}.")

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
            print("Exiting File Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    file_system_root = create_file_system()
    current_directory = file_system_root
    file_management_system(current_directory)
