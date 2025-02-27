import http.server
import ssl
import json

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    # For response Aggregate APISerivce request
    def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "kind": "APIResourceList",
                "apiVersion": "v1",
                "groupVersion": "ops-debug.ctyun.cn/v1alpha1",
                "resources": [
                    {
                    "name": "backups",
                    "singularName": "",
                    "namespaced": True,
                    "kind": "Backup",
                    "verbs": [
                        "create",
                        "delete",
                        "deletecollection",
                        "get",
                        "list",
                        "patch",
                        "update",
                        "watch"
                    ],
                    "storageVersionHash": "IWRSucd/Dbc="
                    },
                    {
                        "name": "backups/status",
                        "singularName": "",
                        "namespaced": True,
                        "kind": "Backup",
                        "verbs": [
                            "get",
                            "patch",
                            "update"
                    ]
                    }
                ]
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            request_json = json.loads(post_data.decode('utf-8'))
            pretty_json = json.dumps(request_json, ensure_ascii=False, indent=4, sort_keys=True)
            print(f"Mutate Request: {pretty_json}")
            uid = request_json["request"]["uid"]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "apiVersion": "admission.k8s.io/v1",
                "kind": "AdmissionReview",
                "response": {
                    "uid": uid,
                    "allowed": True
                }
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        # TODO: fix here
        except json.JSONDecodeError as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'error',
                'message': str(e)
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))


def run_https_server(port, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile='/certs/server.key',
                                   certfile='/certs/server.crt',
                                   server_side=True)
    print(f'Starting HTTPS server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    PORT = 6443 
    run_https_server(PORT)
