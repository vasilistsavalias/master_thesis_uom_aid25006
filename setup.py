import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "2.0.0"

REPO_NAME = "master_thesis_gdm_arch"
AUTHOR_USER_NAME = "your_username" # Replace later if needed
SRC_REPO = "thesis_pipeline"
AUTHOR_EMAIL = "your_email@example.com" # Replace later if needed

setuptools.setup(
    name=f"{SRC_REPO}-{AUTHOR_USER_NAME}",
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package for the ancient Greek artifact restoration thesis pipeline.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
