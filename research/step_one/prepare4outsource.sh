#!/bin/bash

mkdir -p outsource
mkdir -p outsource/valid-data
mkdir -p outsource/test-data
mkdir -p outsource/trans-raw

# Zip validation data for training and testing data for scoring
tar -czf outsource/valid-data/src.gz data/bible.prep/valid.src
tar -czf outsource/valid-data/tgt.gz data/bible.prep/valid.tgt
tar -czf outsource/test-data/src.gz data/bible.prep/test.src
tar -czf outsource/test-data/tgt.gz data/bible.prep/test.tgt

# Copy training data
cp -r train-data ./outsource
cp data/bible.prep/code ./outsource

# Copy translation template
cp data/bible.prep/src-template ./outsource/trans-raw
