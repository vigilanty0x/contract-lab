import unittest
from webhook_sandbox import inspect_webhook, probe
class Tests(unittest.TestCase):
 def test_accept(self): self.assertTrue(inspect_webhook({"method":"POST","path":"/hook","headers":{},"body":"ok"})["accepted"])
 def test_fail_closed(self): self.assertFalse(inspect_webhook({"method":"GET","path":"../x","headers":{},"body":""})["accepted"])
 def test_limit(self): self.assertFalse(inspect_webhook({"method":"POST","path":"/x","headers":{},"body":"xx"},1)["accepted"])
 def test_probe(self): self.assertTrue(probe()["ok"])
if __name__=="__main__": unittest.main()
