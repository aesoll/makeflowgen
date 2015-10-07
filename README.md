# makeflow-gen
Program used to generate makeflow files for processing FITS files using fitssub

## Dependencies 
1. cfitsio - http://heasarc.gsfc.nasa.gov/fitsio/fitsio.html
2. fitssub - https://bitbucket.org/jaredmales/fitssub.git
3. Python 2.7
4. Pandas
5. Numpy

## Install Instructions
Install all dependencies and clone the repository. 

## Usage
If sudo is available,

    sudo pip install -e /path/to/pyAIR
    
If sudo is not avialable, and pip is installed to .local in your home dir

    sudo pip install -e /path/to/pyAIR --install-option="--prefix=/path/to/your/home/.local"
    
Then

    cd /path/to/pyAIR/bin
    ./reduce_images
