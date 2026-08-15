from pathlib import Path
import ast,sys
r=Path(__file__).parents[1]; bad="sk"+"yom"; failures=[]
for p in r.rglob("*.py"):
 try: ast.parse(p.read_text())
 except SyntaxError as e: failures.append(str(e))
for p in r.rglob("*"):
 if p.is_file() and p.suffix in {".py",".md",".toml",".yml"} and bad in p.read_text().lower(): failures.append(str(p))
print("public-boundary: ok" if not failures else failures); sys.exit(bool(failures))
