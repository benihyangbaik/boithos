#!/bin/bash

python -m sockeye.train \
  --prepared-data train-data \
  --validation-source data/bible.prep/valid.src \
  --validation-target data/bible.prep/valid.tgt \
  --use-cpu \
  --output checkpoints/boithos \
  --shared-vocab \
  --max-num-epochs 3
