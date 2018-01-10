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

### Getting it up and running

#### Installation

Install tf models following this [doc](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md)
**Note**: One of the dependency - Protobuf, must be exactly version 2.6.0 for it to work. Otherwise it will throw this error

```python
Traceback (most recent call last):
  File "object_detection/train.py", line 49, in <module>
    from object_detection import trainer
  File "/Users/stanleynguyen/Documents/Projects/tf-models/research/object_detection/trainer.py", line 27, in <module>
    from object_detection.builders import preprocessor_builder
  File "/Users/stanleynguyen/Documents/Projects/tf-models/research/object_detection/builders/preprocessor_builder.py", line 21, in <module>
    from object_detection.protos import preprocessor_pb2
  File "/Users/stanleynguyen/Documents/Projects/tf-models/research/object_detection/protos/preprocessor_pb2.py", line 71, in <module>
    options=None, file=DESCRIPTOR),
TypeError: __init__() got an unexpected keyword argument 'file'
```

#### Training

Command to start training locally (mainly for testing unless we have very powerful
GPUs)

```bash
python3 object_detection/train.py \
--logtostderr \
 --pipeline_config_path=../../pedestrian-detector/training/ssd_inception_v2_coco.local.config \
 --train_dir=../../pedestrian-detector/training/
```

Command to deploy it yo Google ML Engine
**Note**:

* Before deployment, there are some ML Engine problems that need to be
  addressed, please see this [comment](https://github.com/tensorflow/models/issues/2739#issuecomment-351213863)
* The instance type of ML engine should be set to large_model to afford our training

```bash
# copy all training data to gs
gsutil cp -r training gs://pedestrian-detector/training
gsutil cp -r data gs://pedestrian-detector/data
# creating the  required packages
# you must be inside models/research
python3 setup.py sdist && cd slim && python3 setup.py sdist
# copy all config to gs
gsutil cp -r training gs://pedestrian-detector/training
# copy all training data to gs
gsutil cp -r data gs://pedestrian-detector/data
# deploy!
# you are still inside models/research
# running training job
gcloud ml-engine jobs submit training pedestrian_detection_`date +%s` --runtime-version 1.2 --job-dir=gs://pedestrian-detector --packages dist/object_detection-0.1.tar.gz,slim/dist/slim-0.1.tar.gz --module-name object_detection.train --region us-central1 --config ../../pedestrian-detector/training/cloud.yml -- --train_dir=gs://pedestrian-detector --pipeline_config_path=gs://pedestrian-detector/training/ssd_inception_v2_coco.cloud.config
# running eval job
gcloud ml-engine jobs submit training pedestrian_detection_`date +%s` --runtime-version 1.2 --job-dir=gs://pedestrian-detector --packages dist/object_detection-0.1.tar.gz,slim/dist/slim-0.1.tar.gz --module-name object_detection.eval --region us-central1 --scale-tier BASIC_GPU -- --checkpoint_dir=gs://pedestrian-detector/train --eval_dir=gs://pedestrian-detector/eval --pipeline_config_path=gs://pedestrian-detector/training/ssd_inception_v2_coco.cloud.config
  505  history
```

#### Monitoring

```bash
# train
tensorboard --logdir=gs://pedestrian-detector/train --debug
# eval
tensorboard --logdir=gs://pedestrian-detector/eval --debug
```
