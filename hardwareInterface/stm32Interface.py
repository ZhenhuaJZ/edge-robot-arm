import numpy as np
import serial
import time


class DummyInterface(object):

    def __init__(self):
        self.last_message = ''
        pass

    def query_response(self):
        return self.last_message

    def send_message(self, message):
        self.last_message = message
        time.sleep(0.005)

    def close_port():
        pass

    def open_port():
        pass


class Rs232Interface(object):

    def __init__(self, port, test=False):
        self.ser = serial.Serial(port=port,
                                 baudrate=115200,
                                 bytesize=8,
                                 stopbits=1,
                                 timeout=3)
        if not self.ser.isOpen():
            self.ser.open()

    def query_response(self):
        out = ''
        data = 'start'
        while len(data) is not 0:
            data = self.ser.readline()
            out += data.decode()
        return out

    def send_message(self, message):
        message = message.encode('utf-8')
        byte_gcode = serial.to_bytes(message)
        self.ser.write(message)
        time.sleep(0.01)

    def close_port():
        self.ser.close()

    def open_port():
        self.ser.open()


class RobotAnnoV6(object):
    """
        API for control the RobotAnnoV6 robot

        example:
            robot = RobotAnnoV6('/dev/ttyUSB0', 'rs232')
            robot.set_joint(0, 0, 0, 0, 0, 0)  # Controll robot by setting all 6 joints to 0 degree
            robot.set_single_joint(1, 0)  # Set joint 1 to 0 degree
            robot.set_xyzrpy(300, 200, 200, 0, 0, 0)  # Control robot by setting coordinate 
    """

    def __init__(self, port: str, interface: str):
        self.modes = {"idle": "\x10", "run": "\x13", "tune": "\x14",
                      "query": "\x05", "file": "\x11", "rezero": "\x15"}
        if interface == 'rs232':
            self.interface = Rs232Interface(port)
        elif interface == 'dummy':
            self.interface = DummyInterface()
        else:
            raise NotImplementedError

    def set_joints(self, j1: int, j2: int, j3: int,
                  j4: int, j5: int, j6: int):
        gcode = f'G00 J1={j1} J2={j2} J3={j3} J4={j4} J5={j5} J6={j6}\n'
        self.interface.send_message(gcode)
        response = self.interface.query_response()
        if response:
            return True
        else:
            return False

    def set_single_joint(self, joint_idx: int, degree: int):
        gcode = f'G00 J{joint_idx}={degree}\n'
        self.interface.send_message(gcode)
        response = self.interface.query_response()
        if response:
            return True
        else:
            return False

    def set_xyzrpy(self, x, y, z, rx, ry, rz):
        gcode = f'G20 X={x} Y={y} Z={z} A={rx} B={ry} C={rz} D=0\n'
        self.interface.send_message(gcode)
        response = self.interface.query_response()
        if response:
            return True
        else:
            return False

    def set_mode(self, mode):
        self.interface.send_message(self.modes[mode])
        response = self.interface.query_response()
        return response
