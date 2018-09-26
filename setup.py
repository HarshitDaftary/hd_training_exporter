import setuptools

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
    keywords = ['rasa ui', 'rasa','training','export']
)