#! /bin/bash

# Retag:
docker tag rcdiana-amd64-python  rcdiana/python:amd64 \
&& docker tag rcdiana-amd64-dicom   rcdiana/dicom:amd64

# Upload
docker push rcdiana/python:amd64 \
&& docker push rcdiana/python:armv7hf

# Manifest
docker manifest create rcdiana/python rcdiana/python:amd64 rcdiana/python:armv7hf \
&& docker manifest annotate rcdiana/python rcdiana/python:amd64 --arch amd64 \
&& docker manifest annotate rcdiana/python rcdiana/python:armv7hf --arch arm --variant v7 \
&& docker manifest annotate rcdiana/python rcdiana/python:armv7hf --arch arm64 --variant v8
# trick resin compiler

# Retag
docker tag rcdiana-arm7hf-python rcdiana/python:armv7hf \
&& docker tag rcdiana-arm7hf-dicom  rcdiana/dicom:armv7hf 

# Upload
docker push rcdiana/dicom:amd64 \
&& docker push rcdiana/dicom:armv7hf

# Manifest
docker manifest create rcdiana/dicom rcdiana/dicom:amd64 rcdiana/dicom:armv7hf \
&& docker manifest annotate rcdiana/dicom rcdiana/dicom:amd64 --arch amd64 \
&& docker manifest annotate rcdiana/dicom rcdiana/dicom:armv7hf --arch arm --variant v7 \
&& docker manifest annotate rcdiana/dicom rcdiana/dicom:armv7hf --arch arm64 --variant v8
# trick resin compiler

# Push
docker manifest push rcdiana/dicom \
&& docker manifest push rcdiana/python

