import unittest

from honlib.data_structures import linked_list


class LinkedListTestCase(unittest.TestCase):

    def test_clear(self):
        vt = linked_list.LinkedList()
        vt.append(1)
        self.assertEqual((1,), vt.to_tuple())

        vt.clear()
        self.assertEqual(tuple(), vt.to_tuple())

    def test_bool_is_false(self):
        vt = linked_list.LinkedList()

        self.assertFalse(bool(vt))

    def test_bool_is_true(self):
        vt = linked_list.LinkedList()
        vt.append(0)
        self.assertTrue(bool(vt))

    def test_append(self):
        vt = linked_list.LinkedList()

        vt.append(1)
        vt.append(2)
        vt.append(3)

        result = list(vt)

        self.assertEqual(3, len(result))
        self.assertEqual(1, result[0].v)
        self.assertEqual(2, result[1].v)
        self.assertEqual(3, result[2].v)

    def test_to_tuple(self):
        vt = linked_list.LinkedList()

        vt.append(1)
        vt.append(2)
        vt.append(3)

        result = vt.to_tuple()
        self.assertEqual((1, 2, 3), result)


class DoublyLinkedListTestCase(unittest.TestCase):

    def test_clear(self):
        vt = linked_list.DoublyLinkedList()
        vt.append(1)
        self.assertEqual((1,), vt.to_tuple())

        vt.clear()
        self.assertEqual(tuple(), vt.to_tuple())

    def test_bool_is_false(self):
        vt = linked_list.DoublyLinkedList()

        self.assertFalse(bool(vt))

    def test_bool_is_true(self):
        vt = linked_list.DoublyLinkedList()
        vt.append(0)
        self.assertTrue(bool(vt))

    def test_append(self):
        vt = linked_list.DoublyLinkedList()

        vt.append(1)
        vt.append(2)
        vt.append(3)

        result = list(vt)

        self.assertEqual(3, len(result))
        self.assertEqual(1, result[0].v)
        self.assertEqual(2, result[1].v)
        self.assertEqual(3, result[2].v)

    def test_to_tuple(self):
        vt = linked_list.DoublyLinkedList()

        vt.append(1)
        vt.append(2)
        vt.append(3)

        result = vt.to_tuple()
        self.assertEqual((1, 2, 3), result)

    def test_reversed(self):
        vt = linked_list.DoublyLinkedList()

        vt.append(1)
        vt.append(2)
        vt.append(3)

        result = list(reversed(vt))

        self.assertEqual(3, result[0].v)
        self.assertEqual(2, result[1].v)
        self.assertEqual(1, result[1].v)
