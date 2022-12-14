#!/bin/bash

# Install,
# - Amazon's Sockeye translation framework that's based on PyTorch
# - Subword NMT, data preprocessor that segment texts into subword units
# - Unidecode, decoding unicode alphabet characters to ASCII
# - Universal Tokenizer by Ulf Hermjakob, it might be used to replace
#   Moses' decoder's tokenizer, as of now it is only used to detokenize a
#   translated text
pip install -r requirements.txt

cd ../lib

# Moses Statistical MT system, we're only using its decoder's tokenizer
# with a little modification
if [ ! -d "mosesdecoder" ]; then
  git clone depth 1 https://github.com/moses-smt/mosesdecoder
  # Apply the modification
  sed -z "$(echo s/#no\ change/\$word\ =\ \$pre\.\"\ \.\"\;/{2..1}\;)" mosesdecoder/scripts/tokenizer/tokenizer.perl
fi

# Unecessary for now.
# SIL's "... set of pipelines for performing experiments on various NLP
# tasks with a focus on resource-poor and minority languages."
# if [ ! -d "silnlp" ]; then
#   git clone depth 1 https://github.com/sillsdev/silnlp
# fi

cd ../

if [ ! -d "corpus"]; then
  # Get and unzip the corpus for step one research
  mkdir corpus && cd corpus
  wget https://bnmt.benihyangbaik.com/corpus/step_one_corpus.zip
  unzip step_one_corpus.zip
fi
