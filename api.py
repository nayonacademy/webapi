from webob import Request, Response
from parse import parse
import inspect
class API:
    def __init__(self):
        self.routes = {}

    def __call__(self, environ, star_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, star_response)

    def route(self, path):
        if path in self.routes:
            raise AssertionError("Already exists")

        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)
        if handler is not None:
            if inspect.isclass(handler):
                handler_function = getattr(handler(), request.method.lower(), None)
                if handler_function is None:
                    raise AttributeError("Method not allow ", request.method)
                handler_function(request, response, **kwargs)
            else:
                handler(request, response, **kwargs)
        else:
            self.default_handler(request, response, **kwargs)
        return response
    
    def default_handler(self, response):
        response.status_code = 404
        response.text = "Not Found"