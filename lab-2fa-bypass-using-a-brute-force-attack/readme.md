# 
to intercept python requests with burp we need to set the following environment variables:

REQUESTS_CA_BUNDLE=./cacert.pem
HTTP_PROXY=http://127.0.0.1:8080
HTTPS_PROXY=http://127.0.0.1:8080
