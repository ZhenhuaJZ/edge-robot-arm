import unittest
from hardwareInterface.stm32Interface import RobotAnnoV6


class TestRobotAnnoV6(unittest.TestCase):

    def setUp(self):
        self.robot = RobotAnnoV6("dummy", "dummy")

    def test_set_joint(self):
        mode = self.robot.set_mode("tune")
        self.assertTrue(mode == "\x14")
        status = self.robot.set_joint(0, 0, 0, 0, 0, 0)
        self.assertTrue(status is True)

    def test_set_xyzrpy(self):
        status = self.robot.set_xyzrpy(12, 12, 12, 12, 12, 12)
        self.assertTrue(status is True)

    def test_set_mode(self):
        response = self.robot.set_mode("run")
        self.assertTrue(len(response))
