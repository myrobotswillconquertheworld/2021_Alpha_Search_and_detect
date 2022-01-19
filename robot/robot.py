from ev3dev2.port import LegoPort
from ev3dev2.sensor.lego import UltrasonicSensor, GyroSensor, ColorSensor

from move import MoveDiff
from detection import MetalDetector
from pickup import Pickup
from communication import Client


class Robot(object):
    def __init__(self, robot_length, motor_ports=None, sensor_ports=None, gui_address=None):

        if gui_address:
            self.socket = Client(gui_address["host"], gui_address["port"])
            print("COM TO HOST {0}:{1} INITIALIZED".format(gui_address["host"], gui_address["port"]))

        if motor_ports:
            if "wheel_left" and "wheel_right" in motor_ports:
                # self.move = Move(robot_length, motor_ports["wheel_left"], motor_ports["wheel_right"])
                self.move = MoveDiff(robot_length, motor_ports["wheel_left"], motor_ports["wheel_right"])
            # if "pickup_left" and "pickup_right" in motor_ports:
            #     self.pickup = Pickup(motor_ports["pickup_left"], motor_ports["pickup_right"])
                print("WHEEL MOTORS INITIALIZED")
            if "pickup" in motor_ports:
                self.pickup = Pickup(motor_ports["pickup"])
                print("PICKUP MOTOR INITIALIZED")

        if sensor_ports is not None:
            if "metal_detector" in sensor_ports:
                p1 = LegoPort(sensor_ports["metal_detector"])
                p1.mode = 'nxt-analog'
                p1.set_device = 'lego-nxt-sound'
                self.metal_detector = MetalDetector(sensor_ports["metal_detector"])
                print("METAL DETECTOR INITIALIZED")

            if "ultrasonic_sensor" in sensor_ports:
                self.ultrasonic_sensor = UltrasonicSensor(sensor_ports["ultrasonic_sensor"])
                self.ultrasonic_sensor.mode = 'US-DIST-CM'
                print("ULTRASONIC SENSOR INITIALIZED")

            if "color_sensor" in sensor_ports:
                self.color_sensor = ColorSensor(sensor_ports["color_sensor"])
                print("COLOR SENSOR INITIALIZED")

            if "gyro_sensor" in sensor_ports and hasattr(self, "move"):
                self.move.mdiff.gyro = GyroSensor(sensor_ports["gyro_sensor"])
                self.move.mdiff.gyro.calibrate()
                # self.move.mdiff.odometry_start()
            print("GYRO SENSOR INITIALIZED")

        print("ROBOT INITIALIZED")
