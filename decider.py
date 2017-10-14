from container import *
from data_generator import  *


class Decider:

    def __init__(self, container):
        self.container = container
        self.countProblems = 0
        self.decision_alone = True
        self.limits = {"density_down": 0, "density_up": 1500,
                       "temperature_down": 20, "temperature_up": 35,
                       "color_down": 0, "color_up": 1000,
                       "tannins_down": 1, "tannins_up": 100,
                       "cool_down": 0, "cool_up": 20,
                       "pump_down": 0, "pump_up": 30}
        self.attrNames = self.container.listsAndDicts['attrNames']

    def decide(self):
        self.matrix = self.container.containerDB
        # if len(self.matrix) < 3:
        #     return
        # self.check_deriative()
        # self.check_limits()

    def check_limits(self):
        for attr in self.attrNames:
            if attr == "cool" or attr == "pump":
                name = attr + " acts"
            else:
                name = "top " + attr + " sensor"
            current = float(self.matrix[-1][name])
            if current < self.limits[attr + "_down"]:
                self.container.mesBox("the " + attr + " is under the limit")
            elif current > self.limits[attr + "_up"]:
                self.container.mesBox("the " + attr + " is beyond the limit")

    def check_deriative(self):
        for attr in self.attrNames:
            sense_deriative = self.calculate_derivative(attr, "sensor")
            expected_deriative = self.calculate_derivative(attr, "expected")
            if sense_deriative == "N/A" or expected_deriative == "N/A":
                return
            if sense_deriative > expected_deriative + (expected_deriative * 0.1):
                self.container.mesBox("the deriative in " + attr + " is bigger than 10%", "warning decision")
            elif sense_deriative > expected_deriative + (expected_deriative * 0.05) \
                    or sense_deriative < expected_deriative - (expected_deriative * 0.05):
                self.container.mesBox("the deriative in " + attr + " is bigger than 5%", "warning decision")
            elif sense_deriative < expected_deriative - (expected_deriative * 0.1):
                self.container.mesBox("the deriative in " + attr + " is smaller than 10%", "warning decision")

    # creates deriative for the comparison, it's better if it will consider the whole 12 last senses (6 howers)
    def calculate_derivative(self, sensorName, kind):
        if sensorName == "cool" or sensorName == "pump":
            sensorName = sensorName + " acts"
        if kind == "expected":
            name = kind + " " + sensorName
        elif kind == "sensor" and (sensorName != "cool acts" or sensorName != "pump acts"):
            name = "top " + sensorName + " " + kind
        else:
            name = sensorName
        current = self.matrix[-1][name]
        last = self.matrix[-2][name]
        # middle = self.matrix[-6][name]
        # third = self.matrix[-12][name]
        deriative = float(current) - float(last)
        return deriative
