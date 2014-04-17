import unittest
from . import BaseTests

import goless
from goless.backends import current as be


class GoTests(BaseTests):

    def setUp(self):
        BaseTests.setUp(self)

        oldpanic = goless.on_panic
        self.panic_calls = []
        goless.on_panic = lambda *a: self.panic_calls.append(a)

        def restore_panic():
            goless.on_panic = oldpanic
        self.addCleanup(restore_panic)

        self.addCleanup(be.yield_)

    def test_starts_stuff(self):
        items = []
        goless.go(lambda: items.append(1))
        be.yield_()
        self.assertEqual(items, [1])

    def test_exc(self):
        def raiseit():
            raise RuntimeError('ha!')
        goless.go(raiseit)
        be.yield_()
        self.assertEqual(len(self.panic_calls), 1)
