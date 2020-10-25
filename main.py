from hardwareInterface.stm32Interface import RobotAnnoV6


def main():
    robot = RobotAnnoV6("/dev/ttyUSB0", "rs232")
    response = robot.set_mode("tune")
    print(response)
    status = robot.set_xyzrpy(200, 200, 100, 0, 0, 0)
    print(status)

    pass


if __name__ == "__main__":
    main()
