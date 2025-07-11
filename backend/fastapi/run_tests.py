#!/usr/bin/env python3
"""Execute import tests by importing and running them."""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.getcwd())

# Now run the tests
if __name__ == "__main__":
    import test_imports_manual
    sys.exit(test_imports_manual.main())