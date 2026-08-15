import unittest
from schema_contract_tester.core import test_records
class T(unittest.TestCase):
 def test_ok(self): self.assertEqual(test_records([{"x":"a"}],{"x":{"type":"string","required":True}})["status"],"compatible")
 def test_missing(self): self.assertEqual(test_records([{}],{"x":{"type":"string","required":True}})["errors"][0]["error"],"missing")
 def test_type(self): self.assertEqual(test_records([{"x":1}],{"x":{"type":"string"}})["status"],"blocked")
 def test_nullable(self): self.assertEqual(test_records([{"x":None}],{"x":{"type":"string","nullable":True}})["status"],"compatible")
 def test_bool_integer(self): self.assertEqual(test_records([{"x":True}],{"x":{"type":"integer"}})["status"],"blocked")
if __name__=="__main__": unittest.main()

