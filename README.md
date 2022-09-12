# βοηθός (Boithos, helper)

(_The software doesn't exist yet, early research is in progress and frequent
update can be seen in `./research`._)

Software for neural machine translating the Bible to languages with scarce
written/digitized materials.

## What does it do?

- Neural machine translates an incomplete Bible
- Produces grammar documents of the target language

## Why is this feasible?

An article by Utkarsh Kant, titled [Here’s why Deep Learning is not the
Silver Bullet for
NLP?](https://medium.com/@utkarsh.kant/heres-why-deep-learning-is-not-the-silver-bullet-for-nlp-f0e1c767680e)
lists a couple of reasons that actually would give the reverse conclusion
for Biblical NLP. Here are the ones that would yield the reverse
conclusion:

- _Require large datasets_ - according to [Wycliffe Bible Translators
  Annual Progress Report 2021 to
  2022](https://wycliffe.org.uk/wp-content/uploads/2022/08/Wycliffe-Annual-Progress-Report-2021-to-2022.pdf)
  we now have 717 languages with a whole Bible, 1.582 with NT,
  1.196 with portions of the Bible, and 2.899 in progress. That's a
  large parallel corpus.
- _Overfitting_ - the size of training data is large, hence overfitting
  can be avoided.
- _Lack of few-shot learning techniques_ - a method of multi-source Deep
  Learning NLP paired with related families of languages might be a
  _few-shot learning technique_.
- _Domain specialization_ - we specialize on the biblical text.
- _Common knowledge and context_ - there is many research done about _the
  common worldy knowledge_ of the biblical times, hence we only need to
  gather and integrate them into DL networks.

He lists 7 and 5 of them concludes that DL is the _Silver Bullet_ for
Biblical NLP. That's very promising.
