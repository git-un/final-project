import unittest
from SI507F17_finalproject import *


class TestFinalProject(unittest.TestCase):

    # test 1
    def test_Album(self):
        x = Album({
            'name' :'name',
            'genre' :'name',
            'collectionId': 9693,
            'artistName': 'kjs',
            'albumart': 'jhjdh',
            'price': 7.88,
            'artistId': 'kjsd',
            'genre': 'yu',
            'link':'ghj'
            })
        self.assertEqual(type(x), Album, 'type check of Album')

        # test 2

    def test_AlbumString(self):
        x = Album({
            'name' :'name',
            'genre' :'name',
            'collectionId': 9693,
            'artistName': 'kjs',
            'albumart': 'jhjdh',
            'price': 7.88,
            'artistId': 'kjsd',
            'genre': 'yu',
            'link':'ghj'
            })
        self.assertEqual(type(x.__repr__()), str, 'str')

    def test_AlbumArt(self):
        x = Album({
            'name' :'name',
            'genre' :'name',
            'collectionId': 9693,
            'artistName': 'kjs',
            'albumart': 'jhjdh',
            'price': 7.88,
            'artistId': 'kjsd',
            'genre': 'yu',
            'link':'ghj'
            })
        self.assertContains(x.__repr__(), 'albumart', 'see if accepting albumart')

    def test_AlbumGenre(self):
        x = Album({
            'name' :'name',
            'genre' :'name',
            'collectionId': 9693,
            'artistName': 'kjs',
            'albumart': 'jhjdh',
            'price': 7.88,
            'artistId': 'kjsd',
            'genre': 'yu',
            'link':'ghj'
            })
        self.assertContains(x.__repr__(), 'genre', 'see if accepting genre')


    def test_AlbumPrice(self):
        x = Album({
            'name' :'name',
            'genre' :'name',
            'collectionId': 9693,
            'artistName': 'kjs',
            'albumart': 'jhjdh',
            'price': 7.88,
            'artistId': 'kjsd',
            'genre': 'yu',
            'link':'ghj'
            })
        self.assertContains(x.__repr__(), 'price', 'see if accepting price')

    def test_Artist(self):
        x = Album({
            'artistId' : 112,
            'artistName' : 'djed',
            })
        self.assertContains(x.__repr__(), 112, 'see if accepting id')

    def test_Artist_Name(self):
        x = Album({
            'artistId' : 112,
            'artistName' : 'djed',
            })
        self.assertContains(x.__repr__(), 'djed', 'see if accepting <name></name>')




if __name__ == '__main__':
    unittest.main(verbosity=2)
