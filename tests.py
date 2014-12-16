from __future__ import division

import unittest

from six import StringIO

import csample


HASHES = [
    'xxhash32',
    'spooky32',
]


class CLITest(unittest.TestCase):
    def setUp(self):
        self.data = '\n'.join('%d, user%d' % (i, i % 10) for i in range(0, 100))

    def test_line_mode(self):
        sin = StringIO(self.data)
        sout = StringIO()
        csample.main(['-r 1.0'], sin, sout)
        self.assertEqual(self.data, sout.getvalue())

    def test_column_mode(self):
        sin = StringIO(self.data)
        sout = StringIO()
        csample.main(['-r 1.0', '-c 1'], sin, sout)
        self.assertEqual(self.data, sout.getvalue())

    def test_argument_parsing(self):
        args = csample.parse_arguments(['-r0.5', '-c3', '-stest', '--hash=spooky32', '--sep=x'])
        self.assertEquals(0.5, args.rate)
        self.assertEquals(3, args.col)
        self.assertEquals('test', args.salt)
        self.assertEquals('spooky32', args.hash)
        self.assertEquals('x', args.sep)


class APITest(unittest.TestCase):
    def test_sample_line(self):
        ins = [str(i) for i in range(0, 100)]
        outs = list(csample.sample_line(ins, 0.5))
        self.assertTrue(set(outs).issubset(set(ins)))

    def test_sample_tuple(self):
        ins = [(str(i), i) for i in range(0, 100)]
        outs = list(csample.sample_tuple(ins, 0.5, 0))
        self.assertTrue(set(outs).issubset(set(ins)))
        for k, v in outs:
            self.assertEqual(k, str(v))

    def test_hash_functions(self):
        for funcname in HASHES:
            csample.sample_line(['a', 'b'], 0.5, funcname)

        self.assertRaises(
            ValueError,
            csample.sample_line, ['a', 'b'], 0.5, 'unknown_func'
        )


class HashTest(unittest.TestCase):
    def test_sampling_rate_accuracy(self):
        for funcname in HASHES:
            ins = [str(i) for i in range(0, 30000)]
            rates = [1.0, 0.3, 0.0]

            for rate in rates:
                outs = list(csample.sample_line(ins, rate, funcname))
                self.assertAlmostEqual(rate, len(outs) / len(ins), 2, funcname)

    def test_consistency(self):
        for funcname in HASHES:
            ins = [str(i) for i in range(0, 100)]
            outs1 = list(csample.sample_line(ins, 0.5, funcname))
            outs2 = list(csample.sample_line(ins, 0.5, funcname))
            self.assertEqual(outs1, outs2, funcname)


if __name__ == '__main__':
    unittest.main()
