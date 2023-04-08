# Your name: 
# Your student id:
# Your email:
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import numpy as np
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    outer_dict = {}
    name_lst = []
    dict_lst = []
    lst_of_rows = []
    cur.execute('SELECT name, category_id, building_id, rating FROM restaurants')
    for element in cur:
        lst_of_rows.append(element)
    for row in lst_of_rows:
        new_dict = {}
        name_lst.append(row[0])
        cat1 = row[1]
        buil1 = row[2]
        category = cur.execute('SELECT category FROM categories WHERE categories.id = ?', [cat1]).fetchone()[0]
        building = cur.execute('SELECT building FROM buildings WHERE buildings.id = ?', [buil1]).fetchone()[0]
        new_dict['category'] = category
        new_dict['building'] = building
        new_dict['rating'] = row[-1]
        dict_lst.append(new_dict)
    for item in range(len(name_lst)):
        key = name_lst[item]
        value = dict_lst[item]
        outer_dict[key] = value
    return outer_dict


def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    dict = {}
    categories_lst = []
    cur.execute('SELECT * FROM categories')
    for item in cur:
        categories_lst.append(item)
    for row in categories_lst:
        category = row[-1]
        id = row[0]
        count = cur.execute('SELECT COUNT(category_id) FROM restaurants WHERE restaurants.category_id = ?', [id]).fetchone()[0]
        dict[category] = count
    flipper = sorted(dict.items(), key=lambda x: x[1])
    y = []
    x = []
    for tup in flipper:
        y.append(tup[0])
        x.append(tup[-1])
    y_axis = np.array(y)
    x_axis = np.array(x)
    plt.figure(figsize=(18,5))
    plt.barh(y_axis, x_axis)
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Restaurant Categories')
    plt.title('Types of Restaurant on South University Ave')
    plt.show()
    return dict


def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    restaurant_lst = []
    building_id = cur.execute('SELECT id FROM buildings WHERE buildings.building = ?', [building_num]).fetchone()[0]
    restaurants = cur.execute('SELECT name, rating FROM restaurants WHERE restaurants.building_id = ? ORDER BY rating', [building_id]).fetchall()
    index = len(restaurants)
    while index >= len(restaurant_lst):
        for tup in restaurants:
            highest_score = tup[-1]
            highest_name = tup[0]
            if highest_score < tup[-1]:
                highest_score = tup[-1]
                highest_name = tup[0]
        restaurant_lst.append(highest_name)
        index = restaurants.index((highest_name, highest_score))
        del restaurants[index]
    restaurant_lst.append(restaurants[0][0])
    return restaurant_lst



#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    loaded_data = load_rest_data('South_U_Restaurants.db')
    rest_categories = plot_rest_categories('South_U_Restaurants.db')
    find_building = find_rest_in_building(1140, 'South_U_Restaurants.db')

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
