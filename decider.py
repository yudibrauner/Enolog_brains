from container import *
from data_generator import  *


class Decider:

    def __init__(self, container):
        self.container = container
        self.countProblems = 0
        self.decision_alone = True
        self.limits = {"density_down": 0, "density_up": 1500,
                       "temperature_down": 15, "temperature_up": 35,
                       "color_down": 0, "color_up": 1000,
                       "tannins_down": 1, "tannins_up": 100,
                       "cool_down": 0, "cool_up": 20,
                       "pump_down": 0, "pump_up": 30}
        self.attrNames = self.container.listsAndDicts['attrNames']
        self.matrix = self.container.containerDB

    def decide(self):
        if len(self.matrix) < 3 or len(self.matrix)%2 == 1:
            return
        # self.check_deriative()
        self.check_cool()
        self.check_temperature()
        self.check_limits()

    def check_cool(self):
        if self.matrix[-1]['expected cool acts'] * 1.3 < self.matrix[-1]['cool acts']:
            self.container.setExpectedValue('temperature',
                                            float(self.container.get_ExpectedAttr('temperature')) - 2)
            self.addMessage('too fast fermantation')
            self.container.mistake()
        elif self.matrix[-1]['expected cool acts'] * 1.3 < self.matrix[-1]['cool acts']:
            self.addMessage('the fermantation has slowed')
            self.container.setExpectedValue('temperature',
                                            float(self.container.get_ExpectedAttr('temperature')) + 2)
            self.container.mistake()

    def check_temperature(self):
        x=5
        top_temp = self.matrix[-1]['top temperature sensor']
        bot_temp = self.matrix[-1]['bottom temperature sensor']
        if top_temp - 4 > bot_temp:
            self.addMessage("the top temperature is bigger in more than 4 degrees than the bottom sensor")
            self.container.pumpIt("problem")
            self.container.mistake()

    def check_limits(self):
        for attr in self.attrNames:
            if attr == "cool" or attr == "pump":
                name = attr + " acts"
            else:
                name = "top " + attr + " sensor"
            current = float(self.matrix[-1][name])
            if current < self.limits[attr + "_down"]:
                self.addMessage("the " + attr + " is under the limit. the minimum is " + str(self.limits[attr + "_down"]) + " and it is " + str(current))
                self.container.mistake()
            elif current > self.limits[attr + "_up"]:
                self.addMessage("the " + attr + " is beyond the limit. the maximum is " + str(self.limits[attr + "_up"]) + " and it is " + str(current))
                self.container.mistake()

    def check_deriative(self):
        for attr in self.attrNames:
            sense_deriative = self.calculate_derivative(attr, "sensor")
            expected_deriative = self.calculate_derivative(attr, "expected")
            if sense_deriative == "N/A" or expected_deriative == "N/A":
                return
            if sense_deriative > expected_deriative + (expected_deriative * 0.1):
                    self.addMessage("the deriative in " + attr + " is big in 10%. should be " + str(expected_deriative) + "and it is " + str(sense_deriative))
                    if attr == 'density':
                        self.container.pumpIt("problem")
                        self.container.setExpectedValue('temperature', float(self.container.get_ExpectedAttr('temperature')) + 2)
                        self.container.mistake()
                    if attr == 'tannins':
                        self.container.setExpectedValue('temperature',
                                                        float(self.container.get_ExpectedAttr('temperature')) - 2)
                        self.container.mistake()
            elif sense_deriative > expected_deriative + (expected_deriative * 0.05) \
                or sense_deriative < expected_deriative - (expected_deriative * 0.05):
                self.addMessage("the deriative in " + attr + " is big/small in 5%. should be " + str(expected_deriative) + "and it is " + str(sense_deriative))
                self.container.mistake()
            elif sense_deriative < expected_deriative - (expected_deriative * 0.1):
                self.addMessage("the deriative in " + attr + " is small in 10%. should be " + str(expected_deriative) + "and it is " + str(sense_deriative))
                self.container.mistake()
                if attr == 'color':
                    self.container.setExpectedValue('temperature',
                                                    float(self.container.get_ExpectedAttr('temperature')) + 3)
                    for i in range(0, self.matrix[-1]['expected pump acts']):
                        self.container.pumpIt('problem')
                if attr == 'density':
                    self.container.setExpectedValue('temperature',
                                                    float(self.container.get_ExpectedAttr('temperature')) - 2)
                if attr == 'tannins':
                    self.container.setExpectedValue('temperature',
                                                    float(self.container.get_ExpectedAttr('temperature')) + 3)

    # creates deriative for the comparison, it's better if it will consider the whole 12 last senses (6 hours)
    def calculate_derivative(self, sensorName, kind):
        if sensorName == "cool" or sensorName == "pump":
            sensorName = sensorName + " acts"
        if kind == "expected":
            name = kind + " " + sensorName
        elif kind == "sensor" and sensorName != "cool acts" and sensorName != "pump acts":
            name = "top " + sensorName + " " + kind
        else:
            name = sensorName
        current = self.matrix[-1][name]
        last = self.matrix[-2][name]
        # middle = self.matrix[-6][name]
        # third = self.matrix[-12][name]
        deriative = float(current) - float(last)
        return deriative

    def addMessage(self, message):
        self.container.note.set("container" + str(self.container.id) + ": " + message)
        self.container.shortLogger.info(message)