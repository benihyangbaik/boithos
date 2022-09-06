#!/bin/bash

mkdir -p checkpoints/boithos

python -m sockeye.train \
  --prepared-data train-data-bin \
  --validation-source data/bible.prep/valid.src \
  --validation-target data/bible.prep/valid.tgt \
  --output checkpoints/boithos \
  --max-num-epochs 3
