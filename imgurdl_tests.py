import unittest
import imgurdl

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

        self.imgur = imgurdl.ImgurDL()
        
    def test_parse_id_for_albums(self):
        """ Make sure imgur album paths are correctly parsed. """
        for token in self.test_albums:
            for test_case in self.test_albums[token]:
                self.assertEqual(self.imgur.parse_token(test_case), token)

    def test_parse_id_for_images(self):
        """ Make sure imgur image paths are correctly parsed. """
        for token in self.test_images:
            for test_case in self.test_images[token]:
                self.assertEqual(self.imgur.parse_token(test_case), token)
        
    def test_is_album(self):
        """ Try to identify an album from the URL. """
        # First check the albums.
        for album in self.test_albums:
            for case, status in zip(self.test_albums[album], self.test_albums_status[album]):
                response = self.imgur.is_album(case)
                self.assertEqual(response, status)

        # Now check the images.
        for cases in self.test_images.values():
            for case in cases:
                self.assertFalse(self.imgur.is_album(case))


if __name__ == '__main__':
    unittest.main()
