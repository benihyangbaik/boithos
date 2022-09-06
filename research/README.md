# Research for Boithos

## Preparing to Research

On your personal machine:
1. Create a virtual environment `virtualenv ./env/step_one`
2. Enter the virtual environment with `source
   ./env/step_one/bin/activate`. If your default shell is not bash, run
   `bash` first. (Maybe it doesn't have to be Bash? Let me know if that's
   the case.)

On a Jupyter Notebook environment
1. Prepare the data.

## Steps

The following steps of research are important to track research
development and plan future researches. It should be noted that there
would be documents explaining the research result.

### Step 1: Get Familiar with the Base Research

As this is a new field for us, the first step is to get familiar with the
base research by reimplementing Sami Liedes' Convolutional Neural Network
(CNN) generalization model on the languages from the Austronesian family.
Specifically, for the complete Bible:
- Hiri Motu, translation from 1994 
- Indonesian, "Indonesian Bible for All" from 2021 
- Kupang Malay, translation from 2007 
- Malagasy, translation from 1865 
- Tagalog, Philippine Bible Society's translation from 1905;
    and from 2018 
- Tonga, "Revised West Version" from 2014
- Vietnamese, "Easy Reading Version" from 2011

And for the NT only:
- Hawaiian, translation from 1868 
- Malay, KSZI, Contextualized Malay NT from 2013 
- Maori, translation from ?? 
- Sentani, translation from 2020 
- Tetum, translation from 2013 

(This list is basically constructed out of the availability of resources in
the Sword project. It might be supplemented with more in the future.)

All of the will be used as the source language. Though we're going to call
them, "secondary sources", as the actual source is the Greek text, which
would be the Byzantine Majority Text and the Westminster Leningrad Codex. And the
target languages would be Indonesian, Kupang Malay, Sentani, and Tetum.

We will do this first step in two phases. 

The first phase is to update the codebase (original research was done 4
years ago) and recreate the base research with the mentioned datas.

The second phase is to recreate the base research with a different target
language that has an incomplete NT.

Tools used:
  - `fconv_wmt_en_ro` of [Facebook's
    Fairseq](https://github.com/facebookresearch/fairseq) in Python for
    the CNN of 20 layers with 512 neurons each, connected by 3x3
    convolutions.
  - [Moses](http://www.statmt.org/moses) for tokenization of the subwords.
  - [Subword Neural Machine
    Translation](https://github.com/rsennrich/subword-nmt) for creating
    the subwords as a byte pair encoded values.
  - Sword project for providing the Bible translations.

### Step 2: Incorporate Non-Bible Materials

When starting to train a model, we would need at least some written
materials of the target language. We're expecting many cases on only
having non-Bible materials at first. In that case, we would need
translations of the same document in other languages too. Only then that
the model would be able to "learn" the target language from those
materials instead.

On a similar note, later on, these non-Bible materials might supplement
the actual Bible translation, as the model would learn alternatives in
conveying certain concepts or ideas.

In this step, we would be doing several iterations, with different
variations of target language material availability. In each iteration, we
would focus on one target language
