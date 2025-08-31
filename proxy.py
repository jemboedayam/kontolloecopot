from mitmproxy import http

def response(flow: http.HTTPFlow):
    # Example: detect if download triggered from a PHP resource
    if flow.request.pretty_url.endswith(".php"):
        print("[MITM] Intercepted PHP-triggered download:", flow.request.pretty_url)

        # You can modify headers if you want
        if "Content-Disposition" in flow.response.headers:
            filename = flow.response.headers["Content-Disposition"]
            print("[MITM] Download filename:", filename)

        # Example: replace file with dummy text (instead of real file)
        # flow.response.content = b"Fake file contents for testing"