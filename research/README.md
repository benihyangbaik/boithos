# Research for Boithos

_(Work in progress, document may very well be incomplete.)_

Contact: [toar@benihyangbaik.com](mailto:toar@benihyangbaik.com)

## Research Progress

- [ ] Step 1: Recreate the Base Research
  - [ ] Update the codebase
  - [ ] Recreate the base research with 56 Austronesian language
        translations to produce OT translations from scratch on a couple
        of the translations
  - [ ] Instead of producing OT from scratch, produce the rest of NT from scratch
- [ ] Step 2: Improve the Model
  - [ ] Modify Amazon's Sockeye or create a new model with a machine
        learning framework?
  - [ ] Grammar inducement on the encoder?
- [ ] Step 3: Use of Non-Biblical Materials as the Source
- [ ] Step 4: Producing Documents of Grammar Rules of the Target

## Tools and Resources

- [Moses](http://www.statmt.org/moses) for tokenization of the subwords.
- [Amazon Sockeye](https://awslabs.github.io/sockeye/index.html) as the
  sequence-to-sequence translation framework. It includes
  [subword-nmt](https://github.com/rsennrich/subword-nmt) that generates
  subwords as byte pair encoded values.
- [BibleNLP's eBible Corpus](https://github.com/BibleNLP/ebible-corpus)
  for providing the Bible translations and a few other unavailable there
  extracted with tools from the [SIL
  NLP](https://github.com/sillsdev/silnlp) repo with the help of Michael
  Martin from SIL.

## Preparing to Research

_On a personal machine_

1. Create a virtual environment `virtualenv ./env/step_one`
2. Enter the virtual environment with `source ./env/step_one/bin/activate`. If your default shell is not bash, run
   `bash` first. (Maybe it doesn't have to be Bash? Let me know if that's
   the case.)

_On a Google Collab_

1. Prepare the data.

## Steps

The following steps of research are important to track research
development and plan future researches. It should be noted that there
would be documents explaining the research result.

### Step 1: Recreate the Base Research

As this is a new field for us, the first step is to recreate [Sami Liedes'
generalization
approach](https://samiliedes.wordpress.com/2018/03/07/machine-translating-the-bible-into-new-languages/)
on the languages from the Austronesian family. Specifically, for the
complete Bible:

- Amarasi (Kupang, Indonesia), 2014 [aaz-aaz]
- Papuan Malay (Papua, Indonesia), 2020 [pmy-PMY]
- Tagalog (Philippines), 2018 [tgl-tglulb]
- Tonga (Tonga Island), 2014 [ton-ton]
- Ilocano (Phillippines), 2019 [ilo-iloulb]
- Tuwali Ifugao (Ifugao, Northern Luzon, Philippines), 2004 ??? [ifk-ifk]
- Amganad Ifugao (Banaue, Ifugao, Northern Luzon, Philippines), 2014 ??? [ifa-ifa]
- Batad Ifugao (Ifugao, Northern Luzon, Philippines), 2018 ??? [ifb-ifb]
- Matupi Chin (Myanmar), 2019 [hlt-hltmcsb]
- Tuivang Matu Chin, dialect of Matu Chin (Myanmar), 2020 [hlt-hltthb]

And for the incomplete Bible:

- Indonesian (Indonesia), 2021 (NT only) [ind-indags]
- Alune (Seram, Indonesia), 2012 (NT only) [alp-alpNT]
- Ambai (Ambai Islands, Papua, Indonesia), 2010 (incomplete NT only) [amk-amk]
- Auye (Papua, Indonesia), 2020 (incomplete NT only) [data not yet
  retrieved, its codename: auu-auu]
- Balantak (Sulawesi, Indonesia), 2010 (incomplete NT only) [blz-blzNT]
- Bambam (Mamasa, Sulawesi, Indonesia), 2004 (incomplete NT and incomplete
  OT) [*ptu-ptu]
- Pura, dialect of Blagar (Belagar, NTT, Indonesia), 2016 (Gen, Mrk, Acts)
  [beu-beu]
- Rote Dela/Dela-Oenale (Rote Island, NTT, Indonesia), 2016 (NT and Gen)
  [row-row]
- Dhao (Dhao Island, NTT, Indonesia), 2012 (NT and Gen) [nfa-nfa]
- Fordata (Tanimbar, Maluku Tenggara Barat, Maluku, Indonesia), 2018 (NT
  only) [frd-frd]
- Hawu, very similar with Dhao (couple of places around Sumba, NTT,
  Indonesia), 2016 (Mrk) [*hvn-hvn]
- Helong (Kupang; Flores; Semau, NTT, Indonesia), 2011 (NT and Gen)
  [heg-hegNTpo]
- Kisar (Kisar Island, Maluku Barat Daya, Maluku, Indonesia), 2008 (NT
  only) [kje-kjeNT]
- Kupang Malay (Kupang, NTT, Indonesia), 2007 (NT only) [mkn-mkn]
- Rote Lole (Middle Rote Island, NTT, Indonesia), 2004 (NT and Gen) [llg-llg]
- Luang (Leti and Babar Islands, Maluku, Indonesia), 2014 (NT, Gen, Rut,
  Est, and Job) [lex-lex]
- Mai Brat (Semenanjung Doberai, Papua, Indonesia), 2005 (NT+) [ayz-AYZ]
- Mamasa (Mamasa, Western Sulawesi, Indonesia), 2011 (NT only) [mqj-mqjNT]
- Nggem (Nugini Highlands, Papua, Indonesia), 2013 (NT only) [nbq-nbq]
- South Nuaulu (Seram, Indonesia), 2019 (NT+) [nxl-nxl]
- Orya (Papua, Indonesia), 2018 (NT+) [*ury-ury]
- Rote Rikou (Eastern Rote Island, NTT, Indonesia), 2004 (NT and Gen)
  [rgu-rgu]
- Selaru (Selaru and Yamdena Island, Maluku, Indonesia), 2020 (NT only)
  [slu-slu]
- Sentani (Lake Sentani, Papua), 2020 (NT only) [set-set]
- Tetun Belu (Belu, NTT, Indonesia), 2013 (NT and Gen) [tet-tet]
- Rote Tii (Rote Barat Daya, Rote Island, NTT, Indonesia), 2011 (NT and
  Gen) [txq-txq]
- Mek Kosarek (Yahukimo, Papua, Indonesia), 2015 (unknown portions) [kkl-kkl]
- Yawa (Central Yapen, Papua, Indonesia), 2011 (NT only) [yva-yvaNT]
- Caribbean Java (Suriname), 2009 (NT only) [*jvn-jvnNT]
- Banjar (Malaysia), 2019 (John, Rut) [bjn-bjn]
- Contextualized Malay (Malaysia), 2013 (NT only) [zlm-zlmKSZI]
- Agutaynen (Agutaya Island, Palawan, Philippines), 2004 (NT only) [agn-agn]
- Antipolo Ifugao (Ifugao, Philippines), 2009 (NT only)??? [ify-ify]
- Central Cagayan Agta (Agta, Central Cagayan, Philippines), 1992 (NT
  only) [agt-agt]
- Casiguran Dumagat Agta (Agta, Casiguran Dumagat, Philippines), 1979 (NT
  only) [dgc-dgc]
- Dupaninan Agta (Agta, Dupaninan, Philippines), 2001 (NT only) [duo-duo]
- Pamplona Atta (Pamplona, Cagayan, Philippines), 1996 (NT only) [*att-att]
- Ayta Abellen, Sambalic (Tarlac, Philippines), 2020 (NT+) [abp-ABP]
- Mag-antsi Ayta, Sambalic (Zambales; Tarlac; Mabalacat; Angeles City,
  Philippines), 2006 (NT only) [sgb-sgb]
- Ayta Mag-Indi, Sambalic (Pampanga, Philippines), 2020 (unknown portions)
  [blx-blx]
- Tina Sambal, Sambalic (Northern Zambales, Philippines), 1999 (NT only)
  [xsb-xsb]
- Botolan Sambal, Sambalic (Botolan and Cabangan, Philippines), 2005 (NT+)
  [*sbl-sbl]
- Mayoyao Ifugao (Ifugao, Northern Luzon, Philippines), 2003 (NT only)
  [ifu-ifu]
- Zyphe Chin (Zyphe, Myanmar), 2010 (NT only) [zyp-zypNT]
- Siyin Chin (Myanmar), 2020 (NT only) [csy-csy]

All of the above will be used as the source language. Though we're going
to call them "secondary sources", as the actual source is the Greek and
Hebrew text. Which will be:

- the Brenton Septuagint [grc-grcbrent], OR
- the Masoretic Text [hbo-hbo], OR
- the Westminster Leningrad Codex [hbo-hboWLC], and
- Tischendorf's 8th Edition [grc-grc-tisch], OR
- the Majority Text year 2000 revision [grc-grcmt], OR
- the Modern Hebrew Bible [hch-hchNT]

And the target languages will be:

- Indonesian,
- Carribean Java,
- Kisar (Maluku),
- Luang (Maluku),
- Orya (Papua),
- Banjar (Malaysia), and
- possibly some other local language in Indonesian with incomplete
  translations.

We will do this first step in four phases.

**First Phase**

Update the codebase (original research was done 4 years ago) using
Amazon's Sockeye as the author suggested in his [following
article](https://samiliedes.wordpress.com/2018/08/28/recent-developments-and-ideas-on-the-bible-neural-machine-translation-problem/)
and prepare the base research with the mentioned datas.

**Second Phase**

Recreate the base research with a different target language that has no OT
or incomplete OT or incomplete NT with the Brenton Septuagint and
Tischendorf' 8th Edition as the source text.

**Third Phase**

Repeat the second phase with the Masoretic Text and the Modern Hebrew
Bible as the source text.

**Fourth Phase**

Repeat the second phase with the Masoretic Text and Tischendorf's 8th
Edition as the source text. There might be preliminary steps to be taken
to translate from two different languages in the source text.

### Step 2: Improve the Model

**Preliminary Step**

As Sockeye is a translation framework, it might be inflexible for
modifications on the techniques implemented in the Neural Network. So
before making any improvements, we'd have to find out which way is better:
modifying Sockeye or creating a new one with a machine learning framework.

**Grammar Inducement on the Encoder**

There is [research done on an NMT model that could induce grammars which
will improve translation quality](https://arxiv.org/abs/1805.10850) in
2018. The grammar is induced by adding,

> ... a structured self attention encoder that predicts a non-projective
> dependency tree over the source sentence provides a soft structured
> representation of the source sentence that can then be transferred to
> the decoder, which alleviates the burden of capturing target syntax on
> the target side."

...

### Step 3: Use of Non-Biblical Materials as the Source

_(Might be a wild-goose chase or something we've not yet understood.)_

**Non-Biblical Materials on the Target Language**
When starting to train a model, we would need at least some written
materials of the target language. We're expecting cases on only having
non-Bible materials at first. In that case, we would need translations of
the same document in other languages too. Only then that the model would
be able to "learn" the target language from those materials instead.

On a similar note, later on, these non-Bible materials might supplement
the actual Bible translation, as the model would learn alternatives in
conveying certain concepts or ideas.

In this step, we would be doing several iterations, with different
variations of target language material availability. In each iteration, we
would focus on one target language.

...

**Non-Biblical Materials on the Secondary Sources**
There are texts of the Church Fathers,
[writings](https://github.com/OGL-PatrologiaGraecaDev) and
[commentaries](https://github.com/OpenGreekAndLatin/catenae-dev) in HTML
or XML format. Tanakh, Mishnah, Talmud, Midrash, and [other Jewish
texts](https://github.com/Sefaria/Sefaria-Export) in a JSON format. And
[Greek texts in general](https://github.com/OpenGreekAndLatin) that
might have translations in other languages that could be one of the
secondary sources in human-readable formats. The goal of this part of the
research is to _find out if adding these texts and its translations would
help the model to acquire knowledge that would be used when producing
translations._
