from lib.gilded_rose import *

def fetch_items():
    items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
            Item(name="Aged Brie", sell_in=2, quality=0),
            Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
            Item(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
        ]
    return items

def fetch_items_excluding_sulfuras():
    items = [
            Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
            Item(name="Aged Brie", sell_in=2, quality=0),
            Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
            Item(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
        ]
    return items

"""
Introduction to our system:

    All items have a SellIn value which denotes the number of days we have to sell the items
    All items have a Quality value which denotes how valuable the item is
    At the end of each day our system lowers both values for every item
"""

def test_all_items_have_a_sell_in_value():
    for item in fetch_items():
        assert type(item.sell_in) is int

def test_all_items_have_a_quality_value():
    for item in fetch_items():
        assert type(item.quality) is int

def test_at_end_of_each_day_system_lowers_both_values_for_vest():
    items = fetch_items()
    vest = items[0]
    gilded_rose = GildedRose(items)
    initial_sell_in = vest.sell_in
    initial_quality = vest.quality
    for days in range(10):
        assert vest.sell_in == initial_sell_in - days
        assert vest.quality == initial_quality - days
        gilded_rose.update_quality()
"""
Pretty simple, right? Well this is where it gets interesting:

    Once the sell by date has passed, Quality degrades twice as fast
    The Quality of an item is never negative
    "Aged Brie" actually increases in Quality the older it gets
    The Quality of an item is never more than 50
    "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
    "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
        Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but
        Quality drops to 0 after the concert

"""
def test_once_sell_by_date_passed_quality_degrades_twice_as_fast():
    items = fetch_items()
    vest = items[0]
    vest.sell_in = 0
    gilded_rose = GildedRose(items)
    initial_quality = vest.quality
    for days in range(5):
        assert vest.quality == initial_quality - days * 2
        gilded_rose.update_quality()

def test_the_quality_of_an_item_is_never_negative():
    items = fetch_items()
    gilded_rose = GildedRose(items)
    for _ in range(20):
        gilded_rose.update_quality()
    assert not any(item for item in items if item.quality < 0)

def test_aged_brie_increases_in_quality_older_it_gets():
    items = fetch_items()
    aged_brie = items[1]
    gilded_rose = GildedRose(items)
    for _ in range(5):
        quality_of_previous_day = aged_brie.quality
        gilded_rose.update_quality()
        assert aged_brie.quality > quality_of_previous_day

def test_the_quality_of_an_item_is_never_more_than_50():
    items = fetch_items_excluding_sulfuras()
    gilded_rose = GildedRose(items)
    for _ in range(20):
        gilded_rose.update_quality()
    assert not any(item for item in items if item.quality > 50)

def test_sulfuras_never_has_to_be_sold_or_decreases_in_quality():
    items = fetch_items()
    first_sulfuras = items[3]
    first_sulfuras_initial_quality = first_sulfuras.quality
    second_sulfuras = items[4]
    second_sulfuras_initial_quality = second_sulfuras.quality
    gilded_rose = GildedRose(items)
    for _ in range(5):
        gilded_rose.update_quality()
    assert first_sulfuras.quality == first_sulfuras_initial_quality
    assert second_sulfuras.quality == second_sulfuras_initial_quality

def test_backstage_passes_increasn_quality_as_its_sell_in_value_approaches():
    items = fetch_items()
    backstage_passes = items[5]
    gilded_rose = GildedRose(items)
    for _ in range(5):
        quality_of_previous_day = backstage_passes.quality
        gilded_rose.update_quality()
        assert backstage_passes.quality == quality_of_previous_day + 1

def test_backstage_passes_quality_increases_by_2_when_there_are_10_days_or_less():
    backstage_passes = Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)
    gilded_rose = GildedRose([backstage_passes])
    for _ in range(5):
        quality_of_previous_day = backstage_passes.quality
        gilded_rose.update_quality()
        assert backstage_passes.quality == quality_of_previous_day + 2

def test_backstage_passes_quality_increases_by_3_when_there_are_5_days_or_less():
    backstage_passes = Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)
    gilded_rose = GildedRose([backstage_passes])
    for _ in range(5):
        quality_of_previous_day = backstage_passes.quality
        gilded_rose.update_quality()
        assert backstage_passes.quality == quality_of_previous_day + 3

def test_backstage_passes_quality_increases_by_3_when_there_are_5_days_or_less():
    backstage_passes = Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=4, quality=25)
    gilded_rose = GildedRose([backstage_passes])
    for _ in range(5):
        gilded_rose.update_quality()
    assert backstage_passes.quality == 0
"""

We have recently signed a supplier of conjured items. This requires an update to our system:

    "Conjured" items degrade in Quality twice as fast as normal items

"""
def test_conjured_items_degrade_in_quality_twice_as_fast_as_normal_items():
    conjured_item = Item(name="Conjured Mana Cake", sell_in=3, quality=50)
    gilded_rose = GildedRose([conjured_item])
    for _ in range(3):
        quality_of_previous_day = conjured_item.quality
        gilded_rose.update_quality()
        assert conjured_item.quality == quality_of_previous_day - 2
    for _ in range(3):
        quality_of_previous_day = conjured_item.quality
        gilded_rose.update_quality()
        assert conjured_item.quality == quality_of_previous_day - 4