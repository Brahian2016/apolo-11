from setuptools import setup, find_packages

setup(
    name='apolo-11',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'script = apolo11.main:mostrar_menu'
        ]
    },
    install_requires=[
        'tkinter',
        'pandas',
        'pyyaml'
        
    ],
    extras_require={
        'lint': ['flake8'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
