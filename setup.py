from setuptools import setup, find_packages

setup(name="host_sockets",
      version="0.0.2",
      description="Host socket stats",
      author="Dynatrace",
      packages=find_packages(),
      python_requires=">=3.10",
      include_package_data=True,
      install_requires=["dt-extensions-sdk"],
      extras_require={"dev": ["dt-extensions-sdk[cli]"]},
      )
