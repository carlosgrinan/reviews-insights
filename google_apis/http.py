class BatchHttpRequestCustom:
    """
    Wrapper of ``BatchHttpRequest`` that returns a list with the responses on ``execute()``.
    """

    def __init__(self, batch_http_request):
        """
        Args:
            batch_http_request: a ``BatchHttpRequest`` created with ``service.new_batch_http_request()``, not directly with its constructor, because of the internal ``batch_uri`` attribute that the former method provides.
        """
        self._batch_http_request = batch_http_request
        self.responses = []

        self._batch_http_request._callback = (
            lambda request_id, response, exception: self.responses.append(response)
            if exception is None
            else print(exception)
        )

    def add(self, request):
        self._batch_http_request.add(request)

    def execute(self, http=None):
        self._batch_http_request.execute(http=http)
        return self.responses


# Note: Mocking batch requests is not implemented by googleapiclient. I haven't tested this solution yet. See https://github.com/googleapis/google-api-python-client/issues/154
# import collections
# import itertools
# class MockBatchHttpRequest(object):
#     """An object that represents an HTTP request from the batch api."""

#     def __init__(self, callback=None):
#         self._callback = callback
#         self._callbacks = collections.OrderedDict()
#         self._counter = itertools.count()
#         self._request_list = []

#     def _new_id(self):
#         """Generate a new id."""
#         return next(self._counter)

#     def add(self, request, callback=None, request_id=None):
#         """Add a request to be executed as part of the batch."""
#         request_id = request_id or self._new_id()
#         self._callbacks[request_id] = callback
#         self._request_list.append(request)

#     def execute(self, http=None):
#         """Execute the request."""
#         for request, request_id in zip(self._request_list, self._callbacks):
#             response, exception = None, None
#             try:
#                 response = request.execute(http=http)
#             except Exception as e:
#                 exception = e

#             callback = self._callbacks.get(request_id)
#             if callback:
#                 callback(request_id, response, exception)
#             if self._callback:
#                 self._callback(request_id, response, exception)
