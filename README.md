# makeflowgen
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

If sudo is not available, and pip is installed to .local in your home dir

    pip install -e /path/to/makeflowgen --install-option="--prefix=/path/to/your/home/.local"

Then

    cd /path/to/makeflowgen/bin

Modify reduce_images test_data_path to point to the fits data directory (e.g.

     test_data_path = path.join(path.sep, 'home', 'u28', 'dsidi', 'projects', 'extrasolar_planets_image_analysis', 'data', 'bPic_zp_sat_001')

Now run the reduction (assuming you are still in the bin directory)

    chmod u+x ./reduce_images
    ./reduce_images
