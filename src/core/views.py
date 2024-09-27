from django.shortcuts import render

# Create your views here.


def index(request):
    return render(
        request,
        'index.html'
    )

# 400 Bad Request
def error_400(request, exception):
    """

    Handles the 400 Bad Request error.

    Args:
        request (HTTPRequest): The HTTP request that caused the error.
        exception (Exception): The exception that triggered the error.

    Returns:
        HttpResponse: A response object rendering the 400 error page with a 400 status code.

    """

    return render(request, "400.html", status=400)


# 403 Forbidden
def error_403(request, exception):
    """
    Custom error handler for HTTP 403 Forbidden error.

    Args:
        request: The HTTP request object.
        exception: The exception that triggered this error handler.

    Returns:
        HttpResponse: Renders the "403.html" template with a 403 status code.
    """

    return render(request, "403.html", status=403)


# 404 Not Found
def error_404(request, exception):
    """

    Handles HTTP 404 errors by rendering the custom 404 error page.

    Parameters:
    request: HttpRequest object
        The request object used to generate this response.
    exception: Exception object
        The exception that triggered this error handler.

    Returns:
    HttpResponse object
        The rendered 404 error page with a 404 HTTP status code.
    """

    return render(request, "404.html", status=404)


# 429 Too Many Requests
def error_429(request, exception):
    """

    error_429(request, exception):
        Custom view to handle HTTP 429 Too Many Requests errors.

        Args:
            request: The HttpRequest object.
            exception: The exception that triggered this error view.

        Returns:
            HttpResponse: A response object rendered with the "429.html" template and a 429 status code.
    """

    return render(request, "429.html", status=429)


# 500 Internal Server Error
def error_500(request, exception):
    """
    Handles 500 Internal Server Error responses.

    This view function is triggered when an unhandled exception occurs within the application that results in a 500 error.
    It renders a custom 500 error HTML page to inform the user that an internal server error has occurred.

    Arguments:
        request: The request object representing the current HTTP request.
        exception: An exception object that contains information about the error.

    Returns:
        HttpResponse: A rendered 500 error HTML page with the appropriate HTTP status code (500).
    """

    return render(request, "500.html", status=500)


# 503 Service Unavailable
def error_503(request, exception):
    """
    Handles the HTTP 503 Service Unavailable error.

    This view is responsible for rendering a custom 503 error page whenever the server
    is temporarily unable to handle the request due to maintenance or overloading issues.

    Parameters:
        request (HttpRequest): The request object that triggered the 503 error.
        exception (Exception): The exception object that caused the 503 error.

    Returns:
        HttpResponse: A response object rendered with the "503.html" template and
                      a status code of 503.
    """

    return render(request, "503.html", status=503)
