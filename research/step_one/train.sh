#!/bin/bash

python -m sockeye.train \
  --prepared-data train-data \
  --validation-source data/bible.prep/valid.src \
  --validation-target data/bible.prep/valid.tgt \
  --use-cpu \
  --output checkpoints/boithos \
  --shared-vocab \
  --max-num-epochs 3

python -m sockeye.translate \
    -m checkpoints/boithos \
    --beam-size 120 \
    --input data/src.indindags.txt \
    --output data/res.indindags.txt

cp data/res.indindags.txt data/res.indindags.clean.txt

sed -i -r 's/@@( |$)//g' data/res.indindags.clean.txt
