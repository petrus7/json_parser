#!/usr/bin/env bash
setup_mode=$1

echo "########INPUT PARAMS#########"
echo $setup_mode
echo "########INPUT PARAMS#########"


echo "########RUN VENV#########"

. ./venv/bin/activate

echo "########INSTALL setuptools#########"
pip install -r requirements.txt

echo "########RUN SETUPTOOLS#########"
if [[ $setup_mode == "develop" ]]; then
  echo "########RUN DEV MODE#########"
  python setup.py develop
else
    echo "########RUN PROD MODE#########"
    python setup.py build
    python setup.py install
fi