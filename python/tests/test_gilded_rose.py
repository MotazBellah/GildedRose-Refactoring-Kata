import unittest

from gilded_rose import GildedRose, Item

class TestGildedRose(unittest.TestCase):

    # -------------------------------------------------------------------------
    # Standard Items
    # -------------------------------------------------------------------------
    def test_standard_item_before_sell_by_date(self):
        item = Item("+5 Dexterity Vest", sell_in=10, quality=20)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 19)

    def test_standard_item_on_sell_by_date(self):
        item = Item("Elixir of the Mongoose", sell_in=0, quality=10)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 8)  # Degrades twice as fast once sell_in < 0

    def test_standard_item_passed_sell_by_date(self):
        item = Item("Elixir of the Mongoose", sell_in=-1, quality=10)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, -2)
        self.assertEqual(item.quality, 8)  # Degrades twice as fast

    def test_standard_item_quality_never_negative(self):
        item = Item("Elixir of the Mongoose", sell_in=5, quality=0)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.quality, 0)

    def test_standard_item_quality_never_negative_after_sell_in(self):
        item = Item("Elixir of the Mongoose", sell_in=-1, quality=1)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.quality, 0)

    # -------------------------------------------------------------------------
    # Aged Brie
    # -------------------------------------------------------------------------
    def test_aged_brie_before_sell_by_date(self):
        item = Item("Aged Brie", sell_in=5, quality=10)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, 4)
        self.assertEqual(item.quality, 11)

    def test_aged_brie_after_sell_by_date(self):
        item = Item("Aged Brie", sell_in=0, quality=10)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 12)  # Increases twice as fast after sell_in date

    def test_aged_brie_quality_capped_at_50(self):
        item = Item("Aged Brie", sell_in=5, quality=50)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.quality, 50)

    def test_aged_brie_quality_capped_at_50_after_sell_by_date(self):
        item = Item("Aged Brie", sell_in=-1, quality=49)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.quality, 50)

    # -------------------------------------------------------------------------
    # Sulfuras, Hand of Ragnaros
    # -------------------------------------------------------------------------
    def test_sulfuras_never_changes(self):
        item = Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, 0)
        self.assertEqual(item.quality, 80)

    def test_sulfuras_negative_sell_in_never_changes(self):
        item = Item("Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 80)

    # -------------------------------------------------------------------------
    # Backstage passes
    # -------------------------------------------------------------------------
    def test_backstage_passes_more_than_10_days(self):
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=20)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, 10)
        self.assertEqual(item.quality, 21)

    def test_backstage_passes_10_days_or_less(self):
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 22)  # Increases by 2

    def test_backstage_passes_5_days_or_less(self):
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, 4)
        self.assertEqual(item.quality, 23)  # Increases by 3

    def test_backstage_passes_quality_capped_at_50(self):
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.quality, 50)

    def test_backstage_passes_drops_to_zero_after_concert(self):
        item = Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 0)


if __name__ == "__main__":
    unittest.main()