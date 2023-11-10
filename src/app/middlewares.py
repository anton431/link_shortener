"""middlewares."""
from fastapi import Request, Response
from opentracing import (InvalidCarrierException,
                         SpanContextCorruptedException, global_tracer,
                         propagation, tags)
from prometheus_client import Counter

requests_num = Counter(
    'adontsov_link_counter_request_number',
    'Count number of requests.',
    ['operation', 'http_status_code'],
)


async def metrics_count_middleware(request: Request, call_next):
    """Middleware для реализации количества запросов.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): The next middleware or endpoint to call.
    Returns:
        Response: The response object returned by the next middleware or endpoint.  # noqa E501
    """
    response: Response = await call_next(request)
    operation = f'{request.method} {request.url.path}'
    requests_num.labels(
        operation,
        response.status_code,
    ).inc()
    return response


async def tracing_middleware(request: Request, call_next):
    """Middleware для реализации трейсинга.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): The next middleware or endpoint to call.

    Returns:
        Awaitable: The result of calling the next middleware or endpoint.
    """
    path = request.url.path
    if path.startswith('/healthz/up') or path.startswith('/metrics/'):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS, request.headers,
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: request.url,
    }
    with global_tracer().start_active_span(
        str(request.url.path), child_of=span_ctx, tags=span_tags,
    ):
        return await call_next(request)
