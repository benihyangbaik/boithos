#!/bin/bash

# Install,
# - Amazon's Sockeye translation framework that's based on PyTorch
# - Subword NMT, data preprocessor that segment texts into subword units
# - Unidecode, decoding unicode alphabet characters to ASCII
pip install -r requirements.txt

cd ../lib

if [ ! -d "mosesdecoder" ]; then
  # Clone Moses Statistical MT system, we're only using its decoder's
  # tokenizer with a little modification
  git clone depth 1 https://github.com/moses-smt/mosesdecoder
  # Apply the modification
  sed -z "$(echo s/#no\ change/\$word\ =\ \$pre\.\"\ \.\"\;/{2..1}\;)" mosesdecoder/scripts/tokenizer/tokenizer.perl
fi
