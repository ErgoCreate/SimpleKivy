import setuptools

def readme():
    try:
        with open('README.md',encoding='utf-8') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="SimpleKivy",
    version="0.0.2",
    author="ErgoCreate",
    author_email="miguel_nunez95@hotmail.com",
    description="A new way to make user interfaces using a PySimpleGUI approach and with all the power of Kivy",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="GUI UI kivy wrapper simple easy beginner novice student android app",
    url="https://github.com/ErgoCreate/SimpleKivy",
    packages=setuptools.find_packages(include=['SimpleKivy', 'SimpleKivy.*']),
    include_package_data=True,  # For non-Python files
    package_data={
        'SimpleKivy': [
            'skdata/**/*',  # Recursive glob (all files/subdirs)
        ],
    },

    install_requires=[
        "kivy"
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ),
)
