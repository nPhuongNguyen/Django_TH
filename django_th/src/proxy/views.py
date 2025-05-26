from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .graphql import create_product, get_graphql_headers, handle_graphql_errors, send_graphql_request
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle
# | Tên                      | Tác dụng chính                                                                |
# | ------------------------ | ----------------------------------------------------------------------------- |
# | `renderer_classes`       | Quy định **định dạng dữ liệu trả về** từ API (JSON, HTML, XML...)             |
# | `parser_classes`         | Quy định **định dạng dữ liệu mà API nhận vào** (JSON, multipart/form-data...) |
# | `authentication_classes` | Xác định **cách kiểm tra danh tính (login)** của người dùng                   |
# | `throttle_classes`       | Giới hạn **tần suất gọi API** của người dùng (chống spam, lạm dụng)           |
# | `permission_classes`     | Quy định **quyền truy cập** API (ai được phép, ai bị từ chối)                 |


# class OncePerDayUserThrottle(UserRateThrottle):
#         rate = '2/minute' 
# @csrf_exempt
# @require_POST
@api_view(['GET','POST'])
# @throttle_classes([OncePerDayUserThrottle])
def proxy_api(request):
    try:
        graphql_query, graphql_variables = create_product(request.body)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    graphql_url = getattr(settings, "GRAPHQL_BACKEND_URL", "http://127.0.0.1:8000/graphql/")
    headers = get_graphql_headers(request)

    try:
        response_data = send_graphql_request(graphql_query, graphql_variables, headers, graphql_url)
    except RuntimeError as e:
        return JsonResponse({"error": str(e)}, status=500)

    error_response = handle_graphql_errors(response_data)
    if error_response:
        return error_response

    product_data = response_data.get("data", {}).get("productCreate", {})
    return JsonResponse(product_data.get("product", {}), status=201)

