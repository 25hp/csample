from __future__ import division

import unittest
import csample


class TestCase(unittest.TestCase):
    def test_sampling_rate_accuracy(self):
        ins = [str(i) for i in range(0, 10000)]
        rates = [1.0, 0.3, 0.0]

        for rate in rates:
            outs = list(csample.sample_line(ins, rate))
            self.assertAlmostEqual(rate, len(outs) / len(ins), 2)

    def test_consistency(self):
        ins = [str(i) for i in range(0, 100)]
        outs1 = list(csample.sample_line(ins, 0.5))
        outs2 = list(csample.sample_line(ins, 0.5))
        self.assertEqual(outs1, outs2)


if __name__ == '__main__':
    unittest.main()
