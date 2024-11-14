from setuptools import setup, find_packages

setup(
    name='QuantFinance',                    
    version='0.1.0',                        
    author='Diljit Singh',                  
    author_email='diljitsingh22 @Googles email service',
    description='Quantitative finance library for option pricing and analysis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Singh-Diljit/opModels',
    packages=find_packages(),                
    classifiers=[                           
        'Programming Language :: Python :: 3.12.3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                
    install_requires=[                      
        'numpy>=1.26.4',
        'scipy>=1.13.1',
        'matplotlib>=3.9.0'
        'pandas>=2.2.2'
        'yfinance>=0.2.49'
    ],
)
