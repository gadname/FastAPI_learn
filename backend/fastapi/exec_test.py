import sys
import os
sys.path.insert(0, os.getcwd())

print("Direct import test execution")

# Execute the imports directly
exec(open('direct_test.py').read())