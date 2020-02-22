from setuptools import find_packages, setup
import integv

with open("README.md", "r") as fh:
    # Drop the test sample files in dist so there's no need for acknowledgment
    long_description = fh.read().split("# Acknowledgment")[0]

setup(
    name='integv',
    version=integv.__version__,
    packages=find_packages(include=['integv', 'integv.*'], exclude=['test']),
    url='https://github.com/tetrau/integv',
    license='GPLv3',
    author='tetrau',
    author_email='tetrau01@gmail.com',
    description='A file integrity verifier based on the format of the file.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]

)
