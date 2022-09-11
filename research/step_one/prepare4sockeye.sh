#!/bin/bash

python data/prepare_bible.py

rm -rf train-data

python -m sockeye.prepare_data \
  --source data/bible.prep/train.src \
  --target data/bible.prep/train.tgt \
  --output train-data \
  --shared-vocab

echo "Bible corpus is prepared and ready to be used on Amazon's Sockeye."
echo "Either:"
echo "- Run prepare4outsource.sh to gather the necessary data for training and translating in Google Collab, Kaggle, or similar environment."
echo "- Run train.sh for training and translating locally. Don't forget to remove --use-cpu if there is GPU available."
