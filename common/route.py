from common.controller import Controller


def Route(name):
    def wrapper(type):
        print("Route %s registered by %s" % (name,type))
        Controller.registerController(name,type)
        pass

    return  wrapper
