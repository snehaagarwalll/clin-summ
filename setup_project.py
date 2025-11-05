"""
Quick setup script to configure the project directory
"""
import os
import shutil

def setup_project():
    print("=" * 60)
    print("Clinical Text Summarization - Project Setup")
    print("=" * 60)
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Suggest project directory
    default_project_dir = os.path.join(os.path.dirname(current_dir), "clin-summ-data")
    
    print(f"\nCurrent repository: {current_dir}")
    print(f"\nDefault project directory: {default_project_dir}")
    print("\nThis directory will store:")
    print("  - Input data")
    print("  - Trained models")
    print("  - Generated outputs")
    
    user_input = input(f"\nPress Enter to use default, or enter a different path: ").strip()
    
    if user_input:
        project_dir = user_input
    else:
        project_dir = default_project_dir
    
    # Create project directory
    os.makedirs(project_dir, exist_ok=True)
    print(f"\n✓ Created project directory: {project_dir}")
    
    # Copy data if not already there
    data_src = os.path.join(current_dir, "data")
    data_dst = os.path.join(project_dir, "data")
    
    if os.path.exists(data_src) and not os.path.exists(data_dst):
        print(f"\n✓ Copying data from {data_src} to {data_dst}...")
        shutil.copytree(data_src, data_dst)
        print("  Data copied successfully!")
    elif os.path.exists(data_dst):
        print(f"\n✓ Data already exists at {data_dst}")
    
    # Update constants.py
    constants_file = os.path.join(current_dir, "src", "constants.py")
    
    with open(constants_file, 'r') as f:
        content = f.read()
    
    # Replace the DIR_PROJECT line
    old_line = 'DIR_PROJECT = "/your/project/directory/here/"'
    new_line = f'DIR_PROJECT = r"{project_dir}"'
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        with open(constants_file, 'w') as f:
            f.write(content)
        
        print(f"\n✓ Updated src/constants.py with project directory")
    else:
        print(f"\n⚠ Could not automatically update constants.py")
        print(f"  Please manually set: DIR_PROJECT = r\"{project_dir}\"")
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print(f"\nProject directory: {project_dir}")
    print("\nNext steps:")
    print("  1. Verify the setup by checking src/constants.py")
    print("  2. Run a test: python src/run.py --help")
    print("  3. For OpenAI models, configure Azure credentials in src/constants.py")
    print("\n")

if __name__ == "__main__":
    setup_project()
