VENV=${VENV:-.venv}

rm -rf "./dist/"

echo "Copy dependencies"
SITE_PACKAGES=$(find "$VENV" -type d -name site-packages | head -n 1)

if [ -z "$SITE_PACKAGES" ]; then
  echo "Error: no site-packages found in '$VENV'"
  exit 1
fi

cp -r "$SITE_PACKAGES" ./dist

echo "Clean up dist folder"
cd dist

find . | grep __pycache__ | xargs rm -rf
ls -d */ | grep info | xargs rm -rf
ls | egrep "^\_.*" | xargs rm -rf

rm -rf *.so black blackd blib2to3 distutils* pkg_resources pip* setuptools* wheel*

cd ..

echo "Copy source code"
cp -r ./src/* dist

echo "Finished"
echo
