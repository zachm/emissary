import importlib
import random

from emissary import app


class Choice(object):
    """ Actually, you don't get a choice *per se*.
        Take a weighted random email provider and return its class.
    """
    weights = None
    classes = None

    def __init__(self):
        self.weights = []
        self.classes = []

        for _, details in app.config['emissary']['providers'].items():
            self.weights.append(details['enabled'])
            self.classes.append(details['class'])

    @classmethod
    def class_for_name(cls, full_class_string):
        """ Given a full module.submodule.class string, return an actual class object.
            :param full_class_string: Like some.module.submodule.ClassName
            :return: The actual class object denoted by the input.
        """
        pieces = full_class_string.split('.')
        class_name = pieces[-1]
        module_name = '.'.join(pieces[:-1])

        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def choose(self):
        """ Chooser that actually gives back a class to instantiate/use.
            :return: Python class matching up to one of the strings in self.classes.
        """
        return self.class_for_name(self._choose())

    def _choose(self):
        """ Internal chooser for testing purposes.
            :return: string, one of the values in self.classes.
        """
        # pick a value [0, 1]
        rando = random.random()
        # for each class in the list
        for i in range(len(self.classes)):
            # if you're within the weight range, that's the class
            if rando <= self.weights[i]:
                return self.classes[i]
            # otherwise, move onto the next range
            rando -= self.weights[i]
