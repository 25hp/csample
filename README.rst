csample: Consistent sampling library for Python
===============================================

|travismaster|

.. |travismaster| image:: https://secure.travis-ci.org/box-and-whisker/csample.png?branch=master
   :target: http://travis-ci.org/box-and-whisker/csample

Consistent sampling is a sampling method using a hash function as a selection
criterion.

Following list describes some features of the method:

*   Since there are no randomness involved at all, the same data set with the
    same sampling rate (and also with the same salt value) always yields
    exactly the same result.
*   The size of population doesn't need to be specified beforehand. It means
    that the sampling process can be applied to data stream with unknown size
    such as system logs

RFC5475 "Sampling and Filtering Techniques for IP Packet Selection" is a
well-known application of the consistent sampling.


Usage
=====

Two sampling functions are provided for a convenience.

``sample_line()`` accepts ``iterable`` type containing ``str``s::

    data = [
        'alan',
        'brad',
        'cate',
        'david',
    ]
    samples = csample.sample_line(data, 0.5)

``sample_tuple()`` expects ``tuple``s instead of ``str``s as a content of
``iterable``. The third argument ``0`` indicates a column index::

    data = [
        ('alan', 10, 5),
        ('brad', 53, 7),
        ('cate', 12, 6),
        ('david', 26, 5),
    ]
    samples = csample.sample_tuple(data, 0.5, 0)

In both cases, the function returns immediately with sampled ``iterable``.

Full documentation can be found on `Read the Docs`_.

.. _Read the Docs: http://readthedocs.org/docs/csample/en/latest/


Installation
============

Installing csample is easy::

    pip install csample

or download the source and run::

    python setup.py install
