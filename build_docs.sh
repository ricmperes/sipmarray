#!/bin/bash

rm -r ./docs/*
pdoc --force --html --output-dir ./docs sipmarray
mv ./docs/sipmarray/* ./docs/
rm -r ./docs/sipmarray

echo "Docs built with pdoc3!"