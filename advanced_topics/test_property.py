#!/usr/bin/python
import logging
logging.getLogger()

class OurClass(object):

    def __init__(self, a):
        self.OurAtt = a

    @property
    def OurAtt(self):
        print('Getting value...')
        return self.__OurAtt

    @OurAtt.setter
    def OurAtt(self, val):
        print('Setting value...')
        if val < 0:
            self.__OurAtt = 0
        elif val > 1000:
            self.__OurAtt = 1000
        else:
            self.__OurAtt = val


class Car(object):
    def __init__(self, velocity=0.0):
        self.velocity = velocity

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if value > 120:
            print('Reaching the maximum velocity limit 120 mph')
            self._velocity = 120
        else:
            self._velocity = value
        print('Set the new velocity = {} (mph)'.format(self._velocity))

    def accelerate(self, ratio=1.5):
        self.velocity *= ratio
        self.velocity += 1


if __name__ == '__main__':

    x = OurClass(-10)
    print(x.OurAtt)

    newCar = Car()
    for i in range(20):
        newCar.accelerate()