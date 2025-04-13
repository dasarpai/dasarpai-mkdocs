import importlib
import sys

print("Python paths:", sys.path)

try:
    # Try to import the module dynamically
    module = importlib.import_module('macros1')
    
    print("Module loaded successfully!")
    print("Module attributes:", dir(module))
    
    if hasattr(module, 'define_env'):
        print("define_env function exists in module")
    else:
        print("define_env function NOT found in module")
        
    # Get the actual file that was loaded
    print(f"Module file: {module.__file__}")
    
except Exception as e:
    print(f"Failed to import module: {e}")