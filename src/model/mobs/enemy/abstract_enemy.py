from abc import ABCMeta, abstractmethod


class AbstractEnemy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def attack_player(self, field):
        pass
