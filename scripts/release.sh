#!/usr/bin/env bash

set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv is required to build the workflow."
  exit 1
fi

BUNDLEID=$(plutil -extract bundleid raw -o - ./info.plist)
NAME=${BUNDLEID##*.}

VERSION=${1:-$(uv version --short)}
RELEASE_VENV=${RELEASE_VENV:-.venv-release}

uv version "$VERSION" --no-sync
plutil -replace version -string "$VERSION" info.plist

FILENAME="$NAME.v$VERSION.alfredworkflow"

echo "NAME: $NAME"
echo "BUNDLE ID: $BUNDLEID"
echo "VERSION: v$VERSION"
echo


echo "Syncing release environment with uv..."
echo
UV_PROJECT_ENVIRONMENT="$RELEASE_VENV" uv sync --no-dev --quiet
echo


echo "Testing workflow..."
echo

if ! PYTHONPATH=src "$RELEASE_VENV/bin/python" -m unittest discover -s tests; then
  echo "⚠️  TESTS FAILED"
  exit 1
fi


echo "Building binaries..."
echo
VENV="$RELEASE_VENV" ./scripts/build.sh > /dev/null
echo


echo "Building release..."
echo
mkdir -p releases
rm -f "releases/$FILENAME"
zip -r "releases/$FILENAME" dist img *.png info.plist > /dev/null
echo


echo "Released $NAME v$VERSION"
echo " * releases/$FILENAME"
echo

if [ "${NO_OPEN:-0}" != "1" ]; then
  echo "Opening new release"
  open "./releases/$FILENAME"
fi
