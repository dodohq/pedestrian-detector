# pedestrian-detector

Pedestrian Dectector using tensorflow Object detector API

### Data Collection

139 of the data was taken from [https://motchallenge.net/data/2D_MOT_2015/](https://motchallenge.net/data/2D_MOT_2015/)
, handpicked by me.
I also scraped another 100 images from Google Images with the term `pedestrian walking`,
from which I handpicked 71 images
The images from Google introduces more noise to the training dataset, which can be both a good and
bad thing.
So we have in total 210 images in our training set

**Note**: One of the potential problem is that training data is skewed towards abled pedestrian, it
might not be abled to detect people on wheelchairs etc

### Data Annotation

A package named [labelImg](https://github.com/tzutalin/labelImg) was used for ease of data annotation.

**Note**: to install this package, you must first build `resource.py` and `resource.prc` from source
(following the instruction in accord with your OS) then copy them to python lib folder. Aftwards,
`labelImg` can be easily installed like any other python packages `pip install libImg`
