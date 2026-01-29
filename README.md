which python
/usr/bin/python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip3 install numpy flake8 pandas matplotlib seaborn opencv-python

It's needed to have the same distribution of classes in train and validation tests, otherwise predictions would not be accurate.

To choose what specie (Apple or Grape), change Shared_variables' chosen_category var and To_test.sh shared_variable definition.

./Clean.sh if needed
./Build.sh
./create_folders.py
./To_test.sh
