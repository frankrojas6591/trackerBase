from config import Config, basedir

print("test.appNm", Config.appNm)

print("test.Config", Config.__dict__)

# my_package/__init__.py

# Access the current module's name
package_name = __name__
print(f"The name of this module is: {package_name}")

# You can also use it to define package-level variables or logic
#__version__ = "1.0.0"