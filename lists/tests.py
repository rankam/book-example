from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import Client, TestCase
from django.http import HttpRequest

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertMultiLineEqual(response.content, expected_html)


    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.all().count(), 0)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        client = Client()
        response = client.post(
                '/lists/new',
                data={'item_text': 'A new list item'}
        )

        self.assertEqual(List.objects.all().count(), 1)
        new_list = List.objects.all()[0]
        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.list, new_list)

        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))


class NewItemTest(TestCase):

    def test_saving_a_POST_request_to_an_existing_list(self):
        list = List.objects.create()
        other_list = List.objects.create()
        client = Client()
        response = client.post(
            '/lists/%d/new_item' % (list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, list)
        self.assertRedirects(response, '/lists/%d/' % (list.id,))


class ListViewTest(TestCase):

    def test_list_view_displays_all_items(self):
        list = List.objects.create()
        Item.objects.create(text='itemey 1', list=list)
        Item.objects.create(text='itemey 2', list=list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        client = Client()
        response = client.get('/lists/%d/' % (list.id,))

        self.assertIn('itemey 1', response.content)
        self.assertIn('itemey 2', response.content)
        self.assertNotIn('other list item 1', response.content)
        self.assertNotIn('other list item 2', response.content)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(response.context['list'], list)



class EditNotesViewTest(TestCase):

    def test_edit_notes_view_renders_form_to_edit_notes(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(text='itemey 1', list=list1)
        item2 = Item.objects.create(text='itemey 2', list=list1)

        client = Client()
        response = client.get(
            '/lists/%d/item/%d/edit_notes/' % (list1.id, item2.id)
        )

        self.assertEqual(response.context['item'], item2)
        self.assertIn(
            'action="/lists/%d/item/%d/notes"' % (list1.id, item2.id),
            response.content
        )
        self.assertIn('<input name="notes" type="textfield"', response.content)



class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list = List()
        list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list
        second_item.save()

        saved_lists = List.objects.all()
        self.assertEqual(saved_lists.count(), 1)
        self.assertEqual(saved_lists[0], list)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list)


    def test_notes(self):
        item = Item()
        self.assertEqual(item.notes, '')

