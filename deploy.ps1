param (
    [string]$setup_mode = ""
 )

echo "########INPUT PARAMS#########"
echo $setup_mode
echo "########INPUT PARAMS#########"

./venv/Scripts/activate.bat

echo "########INSTALL setuptools#########"
pip install -r requirements.txt

echo "########RUN SETUPTOOLS#########"


If ($setup_mode -eq "develop") {
  echo "########RUN DEV MODE#########"
  python setup.py develop
}
Else {
    echo "########RUN PROD MODE#########"
    python setup.py build
    python setup.py install
}
