import unittest
import imgurdl as imgur

class ImgurDownlaoderTests(unittest.TestCase):

    def setUp(self):
        # format the test cases as a dict, with string key as the expected answer
        # and value as the permutations of the different URLs/IDs.
        self.test_albums = { "Dhjed": ["https://imgur.com/a/Dhjed", "https://imgur.com/a/Dhjed/",
                                  "http://imgur.com/a/Dhjed", "http://imgur.com/a/Dhjed/",
                                  "https://www.imgur.com/a/Dhjed", "https://www.imgur.com/a/Dhjed/",
                                  "http://www.imgur.com/a/Dhjed", "http://www.imgur.com/a/Dhjed/",
                                  "imgur.com/a/Dhjed", "imgur.com/a/Dhjed/",
                                  "imgur.com/a/Dhjed", "imgur.com/a/Dhjed/",
                                  "www.imgur.com/a/Dhjed", "www.imgur.com/a/Dhjed/",
                                  "www.imgur.com/a/Dhjed", "www.imgur.com/a/Dhjed/",
                                  "Dhjed"]
                            }
        self.test_albums_status = {"Dhjed": [True, True, True, True, True, True, True, True, 
                                            True, True, True, True, True, True, True, True, 
                                            False]
                                  }

        self.test_images = { "r4KjYry": ["https://imgur.com/r4KjYry", "https://imgur.com/r4KjYry/",
                                    "https://www.imgur.com/r4KjYry", "https://www.imgur.com/r4KjYry/",
                                    "http://imgur.com/r4KjYry", "http://imgur.com/r4KjYry/",
                                    "http://www.imgur.com/r4KjYry", "http://www.imgur.com/r4KjYry/",
                                    "imgur.com/r4KjYry", "imgur.com/r4KjYry/",
                                    "www.imgur.com/r4KjYry", "www.imgur.com/r4KjYry/",
                                    "imgur.com/r4KjYry", "imgur.com/r4KjYry/",
                                    "www.imgur.com/r4KjYry", "www.imgur.com/r4KjYry/",
                                    "r4KjYry"]
                            }

        
    def test_parse_id_for_albums(self):
        """ Make sure imgur album paths are correctly parsed. """
        for answer, cases in self.test_albums.items():
            for case in cases:
                self.assertEqual(imgur.parse_id(case), answer)

    def test_parse_id_for_images(self):
        """ Make sure imgur image paths are correctly parsed. """
        for answer, cases in self.test_images.items():
            for case in cases:
                self.assertEqual(imgur.parse_id(case), answer)

    def test_is_album(self):
        """ Try to identify an album from the URL. """
        
        # First check the albums.
        for album in self.test_albums.keys():
            for case, status in zip(self.test_albums[album], self.test_albums_status[album]):
                self.assertEqual(imgur.is_album(case), status)

        # Now check the images.
        for cases in self.test_images.values():
            for case in cases:
                self.assertFalse(imgur.is_album(case))


if __name__ == '__main__':
    unittest.main()
