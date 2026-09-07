import sys
import os
sys.path.insert(0, os.path.abspath("."))

import main
openapi_schema = main.app.openapi()
print("Paths in openapi schema:")
for path, methods in openapi_schema.get("paths", {}).items():
    print(f"{list(methods.keys())} : {path}")
