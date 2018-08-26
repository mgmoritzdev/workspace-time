import unittest
import engine
import mock_container
from time import sleep

slow_engine_inteval = 1
fast_engine_interval = 0.05


class EngineBaseTestCase(unittest.TestCase):
    """ This class implements the common structure of every test class. """

    def setUp(self):
        self.longMessage = True
        self.engine = engine.Engine(slow_engine_inteval)
        self.engine.append_container(mock_container.MockContainer())


class EngineFastIntervalBaseTestCase(unittest.TestCase):
    """ This class implements the common structure of every test class. """

    def setUp(self):
        self.longMessage = True
        self.engine = engine.Engine(fast_engine_interval)
        self.engine.append_container(mock_container.MockContainer())


class EngineNoContainersBaseTestCase(unittest.TestCase):
    """ This class implements the common structure of every test class. """

    def setUp(self):
        self.longMessage = True
        self.engine = engine.Engine(slow_engine_inteval)


class EngineNotRunningTestCase(EngineBaseTestCase):
    def runTest(self):
        self.assertEqual(self.engine.is_running,
                         False,
                         'The engine should NOT be running')


class EngineRunningTestCase(EngineBaseTestCase):
    def runTest(self):
        self.engine.start()
        self.assertEqual(self.engine.is_running,
                         True,
                         'The engine should be running')
        self.engine.stop()


class EngineAppendContainerTestCase(EngineNoContainersBaseTestCase):
    def runTest(self):

        self.assertEqual(len(self.engine.containers),
                         0,
                         'Should not contain any container in the beginning')

        c = mock_container.MockContainer()
        self.engine.append_container(c)

        self.assertEqual(len(self.engine.containers),
                         1,
                         'A container should be added to the engine')

        self.assertIs(c,
                      self.engine.containers[0],
                      'The container in the engine should be the same added')


class EngineRemoveContainerTestCase(EngineNoContainersBaseTestCase):
    def runTest(self):

        self.assertEqual(len(self.engine.containers),
                         0,
                         'Should not contain any container in the beginning')

        c = mock_container.MockContainer()
        self.engine.append_container(c)

        self.assertEqual(len(self.engine.containers),
                         1,
                         'A container should be added to the engine')

        self.engine.remove_container(c)
        self.assertEqual(len(self.engine.containers),
                         0,
                         'The container should have been removed')


class SetupContainersTestCase(EngineBaseTestCase):
    def runTest(self):
        self.engine.start()
        c = self.engine.containers[0]
        self.assertEqual(c.count_setups,
                         1,
                         'The container should have counted a setup execution')
        self.engine.stop()


class UpdateContainersTestCase(EngineFastIntervalBaseTestCase):
    def runTest(self):
        self.engine.start()
        sleep(5 * fast_engine_interval)
        c = self.engine.containers[0]
        self.assertTrue(c.count_updates > 1,
                        'The container should have counted some updates')
        self.engine.stop()


if __name__ == '__main__':
    unittest.main()
