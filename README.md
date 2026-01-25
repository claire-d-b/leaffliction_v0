python3.12 -m pip install --upgrade pip
/usr/bin/python -m venv venv or python3-intel64 -m venv venv
source venv/bin/activate
pip3 install numpy flake8 pandas matplotlib seaborn opencv-python

It's needed to have the same distribution of classes in train and validation tests, otherwise predictions would not be accurate.

./Clean.sh if needed
./Build.sh
./create_folders.py
./To_test.sh change Grape to Apple as needed
