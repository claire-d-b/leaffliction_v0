which python
/usr/bin/python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip3 install numpy flake8 pandas matplotlib seaborn opencv-python

It's needed to have the same distribution of classes in train and validation tests, otherwise predictions would not be accurate.

To choose what specie (Apple or Grape), change Shared_variables' chosen_category var and sh scripts' shared_variable definition.

./Clean.sh
./Build.sh

./create_random_dataset.py # creates images in Dataset/ folder
./train.py ./Dataset # train on those data.

./create_random_dataset_new_image.py # Before that, delete features\*.csv.
Creates images in New/ folder
./create_csv_from_dataset.py ./New # creates a dataset to classify with new images

./predict.py ./New # applies thetas from the zip to a dataset that contains path_to_image argument
