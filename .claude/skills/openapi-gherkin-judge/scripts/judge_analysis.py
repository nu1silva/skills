import yaml, re

spec = yaml.safe_load(open('/Users/nuwan@backbase.com/workbench/nu1silva/projects/skills/resources/sample-api.yaml'))
feature = open('/Users/nuwan@backbase.com/workbench/nu1silva/projects/skills/resources/e-commerce-api.feature').read()

paths = spec.get('paths', {})

print("=== ENDPOINT + METHOD COVERAGE ===")
for path, methods in paths.items():
    for method, op in methods.items():
        codes = list(op.get('responses', {}).keys())
        secured = '[secured]' if op.get('security') else '[open]   '
        body = op.get('requestBody', {})
        required = []
        if body:
            for mt, mc in body.get('content', {}).items():
                required = mc.get('schema', {}).get('required', [])
        print(f"  {secured} {method.upper()} {path} -> {codes} required:{required}")

print("\n=== SCENARIO TYPE COUNTS ===")
happy = len(re.findall(r'\[HAPPY\]', feature))
error = len(re.findall(r'\[ERROR\]', feature))
auth = len(re.findall(r'\[AUTH\]', feature))
validation = len(re.findall(r'\[VALIDATION\]', feature))
total = len(re.findall(r'^\s*Scenario:', feature, re.MULTILINE))
print(f"  Total:{total}  Happy:{happy}  Error:{error}  Auth:{auth}  Validation:{validation}")

print("\n=== SECURED ENDPOINTS - check 401+403 coverage ===")
for path, methods in paths.items():
    for method, op in methods.items():
        if op.get('security'):
            m = method.upper()
            path_tag = path.replace('{', '').replace('}', '').lower()
            unauth = 'unauthenticated request' in feature and path_tag in feature.lower()
            forbidden = 'forbidden for unprivileged' in feature
            print(f"  {m} {path} | unauth_in_file:{unauth} forbidden_in_file:{forbidden}")

print("\n=== DOCUMENTED ERROR/AUTH CODES ===")
for path, methods in paths.items():
    for method, op in methods.items():
        for code, desc in op.get('responses', {}).items():
            if str(code).startswith(('4','5')):
                print(f"  {method.upper()} {path} -> {code}: {desc.get('description','')}")

print("\n=== REQUIRED FIELDS (validation scenarios expected) ===")
for path, methods in paths.items():
    for method, op in methods.items():
        body = op.get('requestBody', {})
        if body:
            for mt, mc in body.get('content', {}).items():
                required = mc.get('schema', {}).get('required', [])
                if required:
                    print(f"  {method.upper()} {path}: {required}")
