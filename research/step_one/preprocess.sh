#!/bin/bash

rm -rf train-data

python -m sockeye.prepare_data \
  --source data/bible.prep/train.src \
  --target data/bible.prep/train.tgt \
  --output train-data \
  --shared-vocab
