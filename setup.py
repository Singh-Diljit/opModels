from setuptools import setup, find_packages

setup(
    name='QuantFinance',                    
    version='0.1.0',                        
    author='Diljit Singh',                  
    author_email='diljitsingh22 @Googles email service',
    description='A quantitative finance library for option pricing and analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Singh-Diljit/opModels',
    packages=find_packages(),                
    classifiers=[                           
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                
    install_requires=[                      
        'numpy>=1.26.0',
        'scipy>=1.11.3',
        'pickle5>=1.0.2',
    ],
)
