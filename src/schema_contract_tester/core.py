TYPES={"string":str,"integer":int,"number":(int,float),"boolean":bool,"object":dict,"array":list}
def test_records(records,schema):
 if len(records)>100000: raise ValueError("record limit")
 errors=[]
 for i,row in enumerate(records):
  for field,spec in schema.items():
   if field not in row:
    if spec.get("required",False): errors.append({"row":i,"field":field,"error":"missing"})
    continue
   value=row[field]
   if value is None and spec.get("nullable",False): continue
   typ=TYPES.get(spec["type"])
   if typ is None or not isinstance(value,typ) or spec["type"]=="integer" and isinstance(value,bool): errors.append({"row":i,"field":field,"error":"type"})
 return {"status":"compatible" if not errors else "blocked","errors":errors,"records":len(records)}
def run(data): return test_records(**data)

