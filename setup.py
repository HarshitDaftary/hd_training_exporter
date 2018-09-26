import setuptools

arr_install_requiers = [
    "pandas>=0.23.4",
    "chardet>=2.3.0",
    "pathlib>1.0.1"
]

setuptools.setup(
     name='hd-training-exporter',    # This is the name of your PyPI-package.
     version='0.1',                          # Update the version number for new releases
     description="Generate Rasa training data from a csv file.",
     packages=setuptools.find_packages(),
     author='Harshit Daftary',
     author_email='daftaryharshit@yahoo.co.in',
     scripts=['rasa_exporter'],                  # The name of your scipt, and also the command you'll be using for calling it
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requiers = arr_install_requiers, 
    keywords = ['rasa ui', 'rasa','training','export']
)