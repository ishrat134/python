import unittest
from agents import agentAvailibility


class MyTestCase(unittest.TestCase):
    def test_list_init(self):
        agentData = [
            {'Name': 'Stuart', 'is_available': 'True', 'available_since': 2, 'Roles': ['sales', 'support']},
            {'Name': 'Howard', 'is_available': 'True', 'available_since': 3, 'Roles': ['spanish speaker', 'support']},
            {'Name': 'Sheldon', 'is_available': 'False', 'available_since': 0, 'Roles': ['technical', 'support']},
            {'Name': 'Leonard', 'is_available': 'True', 'available_since': 1, 'Roles': ['technical', 'sales']},
            {'Name': 'Penny', 'is_available': 'False', 'available_since': 0, 'Roles': ['sales', 'support']},
            {'Name': 'Rajesh', 'is_available': 'False', 'available_since': 0, 'Roles': ['spanish speaker', 'sales']},
            {'Name': 'Amy', 'is_available': 'True', 'available_since': 2, 'Roles': ['technical', 'spanish speaker']},
            {'Name': 'Bernie', 'is_available': 'False', 'available_since': 0, 'Roles': ['health', 'support']},
            {'Name': 'Denise', 'is_available': 'True', 'available_since': 7, 'Roles': ['sales', 'support']},
            {'Name': 'Birt', 'is_available': 'True', 'available_since': 1, 'Roles': ['technical', 'sales']},
        ]
        available_one = agentAvailibility(agentData, "least busy", ["sales"])
        available_two = agentAvailibility(agentData, "all_available", ["sales","support"])

        self.assertEqual(available_one,["Denise"])
        self.assertEqual(available_two, ["Stuart", "Denise"])



if __name__ == '__main__':
    unittest.main()
