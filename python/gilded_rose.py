# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Item:
    name: str
    sell_in: int
    quality: int

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
    
class Processor(ABC):
    @abstractmethod
    def update_quality(self, item: Item) -> None:
        ...
        

class Backstage(Processor):
    def update_quality(self, item: Item) -> None:
        if item.quality < 50:
            item.quality = item.quality + 1

            if item.sell_in < 11:
                if item.quality < 50:
                    item.quality = item.quality + 1

            if item.sell_in < 6:
                if item.quality < 50:
                    item.quality = item.quality + 1

        item.sell_in = item.sell_in - 1

        if item.sell_in < 0:
            item.quality = 0

class Sulfuras(Processor):
    def update_quality(self, item: Item) -> None:
        pass  # Sulfuras does not change in quality or sell_in


class AgedBrie(Processor):
    def update_quality(self, item: Item) -> None:
        if item.quality < 50:
            item.quality = item.quality + 1

        item.sell_in = item.sell_in - 1
        if item.sell_in < 0:
            if item.quality < 50:
                item.quality = item.quality + 1

class Standard(Processor):
    def update_quality(self, item: Item) -> None:
        if item.quality > 0:
            item.quality -= 1

        item.sell_in = item.sell_in - 1

        if item.sell_in < 0:
            if item.quality > 0:
                item.quality -= 1

class Conjured(Processor):
    def update_quality(self, item: Item) -> None:
        item.quality = max(item.quality - 2, 0)

        item.sell_in = item.sell_in - 1

        if item.sell_in < 0:
            item.quality = max(item.quality - 2, 0)

registery : dict[str, Processor] = {
    "Aged Brie": AgedBrie,
    "Sulfuras, Hand of Ragnaros": Sulfuras,
    "Backstage passes to a TAFKAL80ETC concert": Backstage,
    "Conjured": Conjured,
}

class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_quality(self) -> None:
        for item in self.items:
            if item.name in registery:
                p : Processor = registery[item.name]()
                p.update_quality(item)
            else:
                p : Processor = Standard()
                p.update_quality(item)


