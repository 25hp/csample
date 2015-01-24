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

    def test_line_based_hash_sampling(self):
        sin = StringIO(self.data)
        sout = StringIO()
        csample.main(['-r 1.0'], sin, sout)
        self.assertEqual(self.data, sout.getvalue())

    def test_column_based_hash_sampling(self):
        sin = StringIO(self.data)
        sout = StringIO()
        csample.main(['-r 1.0', '-c 1'], sin, sout)
        self.assertEqual(self.data, sout.getvalue())

    def test_reservoir_sampling(self):
        sin = StringIO(self.data)
        sout = StringIO()
        csample.main(['-r 100', '--method=reservoir'], sin, sout)
        self.assertEqual(self.data, sout.getvalue())

    def test_argument_parsing(self):
        args = csample.parse_arguments(['-r0.5', '-c3', '-stest', '--hash=spooky32', '--sep=.', '--order'])
        self.assertEquals(0.5, args.rate)
        self.assertEquals(3, args.col)
        self.assertEquals('test', args.seed)
        self.assertEquals('spooky32', args.hash)
        self.assertEquals('hash', args.method)
        self.assertEquals('.', args.sep)
        self.assertEquals(True, args.order)


class FunctionBasedAPITest(unittest.TestCase):
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


class ClassBasedAPITest(unittest.TestCase):
    def setUp(self):
        self.sampler = csample.HashSampler(funcname='xxhash32', seed='DEFAULT_SEED')

    def test_should_sample(self):
        ins = [str(i) for i in range(0, 100)]
        outs = list(i for i in ins if self.sampler.should_sample(i, 0.5))
        self.assertTrue(set(outs).issubset(set(ins)))

    def test_assign(self):
        n_sample = 10000
        ins = [str(i) for i in range(0, n_sample)]
        ratios = (0.2, 0.3, 0.5)
        counts = [0, 0, 0]
        assigner = self.sampler.assign_for(ratios)
        for data in ins:
            index = assigner(data)
            counts[index] += 1

        self.assertAlmostEqual(ratios[0], counts[0] / n_sample, 2)
        self.assertAlmostEqual(ratios[1], counts[1] / n_sample, 2)
        self.assertAlmostEqual(ratios[2], counts[2] / n_sample, 2)


class SamplingTest(unittest.TestCase):
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

    def test_reservoir_sampling(self):
        n_pop = 4
        n_sample = 2
        trials = 200000

        population = list(range(n_pop))
        counters = [0] * n_pop
        for _ in range(trials):
            samples = csample.reservoir(population, n_sample)
            for s in samples:
                counters[s] += 1

        ratios = [round(c / trials, 2) for c in counters]
        for ratio in ratios:
            self.assertEqual(n_sample / n_pop, ratio)

    def test_seeded_reservoir_sampling(self):
        population = list(range(10000))
        n_sample = 10

        noseed_0 = csample.reservoir(population, n_sample)
        noseed_1 = csample.reservoir(population, n_sample)
        seed_a0 = csample.reservoir(population, n_sample, 'a')
        seed_a1 = csample.reservoir(population, n_sample, 'a')
        seed_b = csample.reservoir(population, n_sample, 'b')

        self.assertNotEqual(noseed_0, noseed_1)
        self.assertEqual(seed_a0, seed_a1)
        self.assertNotEqual(seed_a0, seed_b)

    def test_order_preserving_reservoir_sampling(self):
        population = list(range(100))
        sampled = csample.reservoir(population, 10, keep_order=True)
        self.assertEqual(sorted(sampled), sampled)

        population = reversed(list(range(100)))
        sampled = csample.reservoir(population, 10, keep_order=True)
        self.assertEqual(sorted(sampled, reverse=True), sampled)

    def test_partitioning(self):
        ins = [str(i) for i in range(0, 10000)]
        partitions = csample.partition_line(ins, [0.2, 0.3, 0.5])
        partitions = [list(p) for p in partitions]

        self.assertEqual(3, len(partitions))
        self.assertEqual(set(ins), set(partitions[0]).union(set(partitions[1])).union(set(partitions[2])))
        self.assertAlmostEqual(len(partitions[0]) / len(ins), 0.2, 2)
        self.assertAlmostEqual(len(partitions[1]) / len(ins), 0.3, 2)
        self.assertAlmostEqual(len(partitions[2]) / len(ins), 0.5, 2)


if __name__ == '__main__':
    unittest.main()
