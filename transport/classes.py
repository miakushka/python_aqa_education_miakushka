from abc import ABC, abstractmethod

"""
Classes, that implement a simple functionality of different city transport types
"""

# implemented abstract class, that will be inherited
class Transport(ABC):

    def __init__(self, **kwargs):
        self.model = kwargs["model"]
        self.seats = kwargs["seats"]
        self.factory_number = kwargs["factory_number"]
        self.status = None
        self.route_number = None

    @abstractmethod
    def get_status(self):
        ...

    @abstractmethod
    def set_status(self, status):
        ...

    @abstractmethod
    def set_route(self, route_number):
        ...

    @abstractmethod
    def to_depot(self):
        ...


# implemented class, that will be inherited as well
class RailTransport:
    def __init__(self, **kwargs):
        self.track_width = kwargs["track_width"]

    def track_type(self):
        if self.track_width == 1520:
            print("%d mm is equal to post-Soviet tracks" % self.track_width)
        elif self.track_width == 1450:
            print("%d mm is equal to European tracks" % self.track_width)
        elif self.track_width == 750:
            print("%d mm is equal to narrow gauge tracks" % self.track_width)
        else:
            print("Unknown type of tracks")


# implemented class, that inherits Transport and RailTransport classes (multiple inheritance)
class Tram(Transport, RailTransport):
    def __init__(self, **kwargs):
        Transport.__init__(self, **kwargs)
        RailTransport.__init__(self, **kwargs)
        self.wagons = kwargs["wagons"]
        self.voltage = kwargs["voltage"]

    def get_status(self):
        print("Current tram status is: %s" % self.status)
        return self.status

    def set_status(self, status):
        self.status = status

    def set_route(self, route_number):
        if route_number in ("26", "23") and self.wagons < 2:
            print("Only two-wagon trams are acceptable for this route")
        else:
            self.route_number = route_number
            self.set_status("on route %s" % route_number)

    def to_depot(self):
        self.set_status("in depot")

    def get_voltage(self):
        print("The tram voltage is %d V" % self.voltage)


# implemented class, that inherits Transport
class Trolleybus(Transport):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voltage = kwargs["voltage"]

    def get_status(self):
        print("Current trolleybus status is: %s" % self.status)
        return self.status

    def set_status(self, status):
        self.status = status

    def set_route(self, route_number):
        if route_number in ("2", "4", "8"):
            print("Selected route is temporary closed")
        else:
            self.route_number = route_number
            self.set_status("on route %s" % route_number)

    def to_depot(self):
        self.set_status("in depot")

    def get_voltage(self):
        print("The trolleybus voltage is %d V" % self.voltage)


# implemented class, that inherits Transport
class Bus(Transport):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine_type = kwargs["engine"]

    def get_status(self):
        print("Current bus status is: %s" % self.status)
        return self.status

    def set_status(self, status):
        self.status = status

    def set_route(self, route_number):
        self.route_number = route_number
        self.set_status("on route %s" % route_number)

    def to_depot(self):
        self.set_status("in depot")

    def get_engine_type(self):
        print("The bus engine type is: %s" % self.engine_type)


# implemented class, that inherits Transport and RailTransport classes (multiple inheritance)
class Subway(Transport, RailTransport):
    def __init__(self, **kwargs):
        Transport.__init__(self, **kwargs)
        RailTransport.__init__(self, **kwargs)
        self.wagons = kwargs["wagons"]
        self.voltage = kwargs["voltage"]
        self.depot = kwargs["depot"]

    def get_status(self):
        print("Current train status is: %s" % self.status)
        return self.status

    def set_status(self, status):
        self.status = status

    def set_route(self, route_number):
        if 5 < route_number < 15:
            print("This route is not served by %s depot" % self.depot)
        else:
            self.route_number = route_number
            self.set_status("on route %s" % route_number)

    def to_depot(self):
        self.set_status("in depot")

    def get_voltage(self):
        print("The train voltage is %d V" % self.voltage)

# implemented staticmethod
    @staticmethod
    def print_info():
        print('''Харківський метрополітен — швидкісна позавулична транспортна система Харкова. 
        Має три діючі лінії, експлуатаційна довжина яких станом на 2018 р. сягає близько 38,1 км.
        До послуг пасажирів — 30 станцій із трьома підземними пересадочними вузлами в середмісті.
        Після відкриття 23 серпня 1975 року Харківський став шостим за ліком метрополітеном в СРСР (після московського, 
        ленінградського, київського, тбіліського, бакинського) та другим в Україні.''')


# use some methods of implemented classes
tram = Tram(model="Tatra T6", seats=26, wagons=1, factory_number=4572, voltage=550, track_width=1520)
tram.set_route("26")
tram.get_status()
tram.get_voltage()
tram.track_type()
print("=" * 50)

trolleybus = Trolleybus(model="Skoda 14Tr", seats=29, factory_number=2401, voltage=600)
trolleybus.set_route("34")
trolleybus.get_status()
trolleybus.to_depot()
trolleybus.get_status()
trolleybus.get_voltage()
print("=" * 50)

bus = Bus(model="LAZ-A183", seats=34, factory_number=1528, engine="diesel")
bus.get_engine_type()
print("=" * 50)

train = Subway(model="81-717", seats=100, wagons=5, factory_number=4252, voltage=850, depot="Saltivske",
               track_width=1520)
train.set_route(8)
tram.track_type()

# call static method without creating class object
Subway.print_info()
