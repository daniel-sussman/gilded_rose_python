# -*- coding: utf-8 -*-

"""
Feel free to make any changes to the UpdateQuality method and add any new code as long as everything
still works correctly. However, do not alter the Item class or Items property as those belong to the
goblin in the corner who will insta-rage and one-shot you as he doesn't believe in shared code
ownership (you can make the UpdateQuality method and Items property static if you like, we'll cover
for you).
"""
class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item.degrade()
            item.sell_in -= 1

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class PerishableItem(Item):
    def degrade(self):
        degraded_quality = self.quality - 1 if self.sell_in > 0 else self.quality - 2
        self.quality = max(0, degraded_quality)

class ConjuredItem(Item):
    def degrade(self):
        degraded_quality = self.quality - 2 if self.sell_in > 0 else self.quality - 4
        self.quality = max(0, degraded_quality)

class AgedBrie(Item):
    def degrade(self):
        degraded_quality = self.quality + 1
        self.quality = min(50, degraded_quality)

class Sulfuras(Item):
    def degrade(self):
        pass

class BackstagePasses(Item):
    def degrade(self):
        if self.sell_in <= 0:
            degraded_quality = 0
        elif self.sell_in <= 5:
            degraded_quality = self.quality + 3
        elif self.sell_in <=10:
            degraded_quality = self.quality + 2
        else:
            degraded_quality = self.quality + 1

        self.quality = min(50, degraded_quality)