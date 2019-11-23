# misc collection of code

## Radiomics feature extraction:  _radiomics_extraction.py_
This function allows to extract features according to the radiomics library. Input are the 2D/3D image and mask in the SimpleITK data format as well as the arguments defining whether the features are to be extracter for some slices or for the volume directly. One can define which features shall be extracted and save them to csv and/or json files.

## Combination of SimpleITK and numpy:  _simpleitk_numpy_image.py_
This class allows to work with an SimpleITK like a numpy array. All SimpleITK functions can still be used and the most common numpy functions as well. This makes life with SimpleITK images much easier.

## Stretch contrast of 16-bit images to a range [0, 255] : _stretch_contrast_bw.py_


## Create a database in SQLite3: _sqlite_database.py_
table creation, insertion, reading, updating and removal of entries
