#!/bin/bash

rm -rf outsource
mkdir -p outsource
mkdir -p outsource/valid-data
# Unecessary for now
# mkdir -p outsource/test-data
mkdir -p outsource/trans-raw

# Zip validation data for training and testing data for scoring
# Some are unecessary for now
# tar -czf outsource/test-data/src.gz data/bible.prep/test.src
# tar -czf outsource/test-data/tgt.gz data/bible.prep/test.tgt
# tar -czf outsource/valid-data/src.gz data/bible.prep/tmp/valid.src
# tar -czf outsource/valid-data/tgt.gz data/bible.prep/tmp/valid.tgt
cp data/bible.prep/tmp/valid.src outsource/valid-data/src.txt
cp data/bible.prep/tmp/valid.tgt outsource/valid-data/tgt.txt

# Copy the BPE code and target vocab
cp data/bible.prep/code outsource/bpe.code
cp data/bible.prep/tmp/bpe.vocab.both outsource

# Copy training data
cp -r train-data outsource

# Copy translation template
cp data/bible.prep/src-template outsource/trans-raw

# Copy the Jupyter Notebook script
cp step_one.ipynb outsource
