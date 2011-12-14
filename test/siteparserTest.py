import unittest
import siteparser

class TestSequenceFunctions(unittest.TestCase):
	
	def test_getCleanPrice(self):
		parser = siteparser.BaseParser("")
		self.assertEquals(parser.getCleanPriceString("4"), "4")
		self.assertEquals(parser.getCleanPriceString("4,99"), "4")
		self.assertEquals(parser.getCleanPriceString("4.4235"), "4")
		self.assertEquals(parser.getCleanPriceString("  1345 "), "1345")
		self.assertEquals(parser.getCleanPriceString("  134  5 "), "134")
		self.assertEquals(parser.getCleanPriceString("  <test/134,56"), "134")
		self.assertEquals(parser.getCleanPriceString("<span>45.45</span>"), "45")

	def test_fnac(self):
		factory = siteparser.ParserFactory()
		parser = factory.getInstanceForUrl("http://jeux-video.fnac.com/a3402180/Tron-Evolution-Jeu-PlayStation-3")
		self.assertTrue(len(parser.getImageUrls()) >= 1)
		self.assertTrue(float(parser.getPrice()) >= 0)
		self.assertEquals("Tron Evolution", parser.getTitle())
	
	def test_amazon(self):
		factory = siteparser.ParserFactory()
		parser = factory.getInstanceForUrl("http://www.amazon.com/Learning-Python-Powerful-Object-Oriented-Programming/dp/0596158068/ref=sr_1_1?s=books&ie=UTF8&qid=1297974499&sr=1-1")
		self.assertTrue(len(parser.getImageUrls()) >= 1)
		self.assertTrue(float(parser.getPrice()) >= 0)
		self.assertEquals("Learning Python", parser.getTitle()[:15])

if __name__ == '__main__':
    unittest.main()