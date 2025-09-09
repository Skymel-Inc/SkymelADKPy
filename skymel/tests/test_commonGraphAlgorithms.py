from unittest import TestCase

from ..commonGraphAlgorithms import CommonGraphAlgorithms


class TestCommonGraphAlgorithms(TestCase):
    def test_remove_duplicate_node_ids_from_list_returns_empty_list_for_invalid_or_empty_inputs(self):
        empty_list = []
        self.assertEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(None), empty_list)
        self.assertEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list({}), empty_list)
        self.assertEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(set()), empty_list)
        self.assertEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list("set()"), empty_list)
        self.assertEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list([]), empty_list)

    def test_remove_duplicate_node_ids_from_list_returns_same_list_for_non_duplicate_inputs(self):
        non_duplicate_string_inputs = ['1', '2', '3']
        self.assertListEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(non_duplicate_string_inputs),
                             non_duplicate_string_inputs)
        non_duplicate_int_inputs = [1, 2, 3]
        self.assertListEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(non_duplicate_int_inputs),
                             non_duplicate_int_inputs)
        non_duplicate_string_and_int_inputs = ['1', 2, '3', 4]
        self.assertListEqual(
            CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(non_duplicate_string_and_int_inputs),
            non_duplicate_string_and_int_inputs)

    def test_remove_duplicate_node_ids_from_list_returns_deduplicated_list_for_duplicate_inputs(self):
        duplicated_string_inputs = ['1', '1', '1', '2', '3', '3']
        deduplicated_string_inputs = ['1', '2', '3']
        self.assertListEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(duplicated_string_inputs),
                             deduplicated_string_inputs)
        duplicated_int_inputs = [1, 2, 2, 3, 3, 3]
        deduplicated_int_inputs = [1, 2, 3]
        self.assertListEqual(CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(duplicated_int_inputs),
                             deduplicated_int_inputs)
        duplicated_string_and_int_inputs = ['1', 2, 2, '3', '3', '3', 4, 4, 4, 4]
        deduplicated_string_and_int_inputs = ['1', 2, '3', 4]
        self.assertListEqual(
            CommonGraphAlgorithms.remove_duplicate_node_ids_from_list(duplicated_string_and_int_inputs),
            deduplicated_string_and_int_inputs)
