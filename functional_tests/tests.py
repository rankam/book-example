from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

class NewVisitorTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        LiveServerTestCase.setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            LiveServerTestCase.tearDownClass()


    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row_text in row.text for row in rows),
            "Could not find row with text %r, table text was:\n%s" % (
                row_text, table.text
            )

        )


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, she is taken to a new URL,
        # and now the page lists "1: Buy peacock feathers" as an item in a
        # to-do list table
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegexpMatches(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Now a new user, Francis, comes along to the site.
        self.browser.quit()
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegexpMatches(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)


    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_tag_name('input')
        window_width = self.browser.get_window_size()['width']
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            window_width / 2,
            delta=3
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_tag_name('input')
        window_width = self.browser.get_window_size()['width']
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            window_width / 2,
            delta=3
        )


    def test_adding_notes(self):
        # Edith starts a new list
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys("Buy milk\n")
        self.check_for_row_in_list_table("1: Buy milk")

        # She notices a link next to her first new item that says "edit notes"
        # so she clicks it
        self.browser.find_element_by_link_text("edit notes").click()

        # She is presented with a form that allows her to write in some notes
        self.browser.find_element_by_name('notes').send_keys(
            "You can find milk in a shop"
        )

        # She cicks submit and the note now shows up in the list
        self.browser.find_element_by_css_selector('input[type=submit]').click()
        self.assertIn(
            "You can find milk in a shop",
            self.browser.find_element_by_tag_name('body').text
        )
        self.fail('finish me')

        # She enters a second item, and edits it to add a second,
        # longer note

        # Now when she clicks submit she sees that the text of
        # her second note is abbreviated.

        # She sees a "more" link, which she clicks, which takes
        # her to a page with the full note content.

        # She wonders whether there is a page for shorter notes
        # too, and realises that list items are clickable.


