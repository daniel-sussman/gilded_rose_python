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
            item.quality = Degrader(item).degraded()
            item.sell_in -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class Degrader:
    def __init__(self, item, floor = 0, ceiling = 50):
        self.item = item
        self.floor = floor
        self.ceiling = ceiling
        self.__degrade_methods = {
            "Aged Brie": self.__degrade_aged_brie,
            "Sulfuras": self.__degrade_sulfuras,
            "Backstage passes": self.__degrade_backstage_passes,
            "Conjured": self.__degrade_conjured_item
        }
        self.degraded = self.__select_degrade_method()
    
    def __select_degrade_method(self):
        for key in self.__degrade_methods:
            if key in self.item.name:
                return self.__degrade_methods[key]
        return self.__degrade_perishable_item

    def __floor(self, value):
        return max(self.floor, value)
    
    def __ceiling(self, value):
        return min(self.ceiling, value)

    def __degrade_perishable_item(self):
        degraded_quality = self.item.quality - 1 if self.item.sell_in > 0 else self.item.quality - 2
        return self.__floor(degraded_quality)

    def __degrade_aged_brie(self):
        return self.__ceiling(self.item.quality + 1)

    def __degrade_sulfuras(self):
        return self.item.quality

    def __degrade_conjured_item(self):
        degraded_quality = self.item.quality - 2 if self.item.sell_in > 0 else self.item.quality - 4
        return self.__floor(degraded_quality)

    def __degrade_backstage_passes(self):
        if self.item.sell_in <= 0:
            return 0
        elif self.item.sell_in <= 5:
            return self.__ceiling(self.item.quality + 3)
        elif self.item.sell_in <=10:
            return self.__ceiling(self.item.quality + 2)
        else:
            return self.__ceiling(self.item.quality + 1)