import json
import requests

from django.http import JsonResponse
# Chuyển "key":"value"->key:"value"
def format_arg_value(value):
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, dict):
        return "{" + ", ".join(f'{k}: {format_arg_value(v)}' for k, v in value.items()) + "}"
    elif isinstance(value, list):
        return "[" + ", ".join(format_arg_value(v) for v in value) + "]"
    else:
        return str(value)
    
def build_fields(fields):
    if isinstance(fields, str):
        return fields
    if isinstance(fields, dict):
        return " ".join(f"{k} {{ {build_fields(v)} }}" for k, v in fields.items())
    if isinstance(fields, list):
        return " ".join(build_fields(f) for f in fields)
    return str(fields)

def grapql(request_body: bytes):
    try:
        data = json.loads(request_body)
        gql_type = data.get("type")
        function = data.get("function")
        args = data.get("args", {})
        fields = data.get("fields")
        if not function:
            raise ValueError("Missing function name")
        if not fields:
            raise ValueError("Missing fields")
    except Exception as e:
        raise ValueError("Invalid JSON or missing data") from e

    args_str = ", ".join(f'{k}: {format_arg_value(v)}' for k, v in args.items())
    fields_str = build_fields(fields)
    graphql_query = {
        "query": f'''
            {gql_type} {{
                {function}({args_str}) {{
                    {fields_str}
                }}
            }}
        '''
    }
    return graphql_query

def create_product(request_body: bytes):
    data = json.loads(request_body)

    for k, v in data.items():
        if isinstance(v, dict):
            data[k] = json.dumps(v, ensure_ascii=False)

    required_fields = ["name", "productType", "category"]
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Missing required field: {field}")

    query = """
        mutation ($input: ProductCreateInput!) {
            productCreate(input: $input) {
                product { id name description}
                errors { field message }
            }
        }
    """
    variables = {
        "input": data
    }
    return query, variables


def get_graphql_headers(request):
    headers = {"Content-Type": "application/json"}
    auth = request.headers.get("Authorization")
    if auth:
        headers["Authorization"] = auth
    return headers


def send_graphql_request(query, variables, headers, url):
    response = requests.post(
        url,
        json={"query": query, "variables": variables},
        headers=headers
    )
    response.raise_for_status()
    return response.json()

def handle_graphql_errors(response_data):
    # Kiểm tra lỗi GraphQL tổng thể
    if "errors" in response_data:
        return JsonResponse({"error": response_data["errors"]}, status=400)
    # Kiểm tra lỗi mutation cụ thể
    product_data = response_data.get("data", {}).get("productCreate", {})
    if product_data.get("errors"):
        return JsonResponse({"error": product_data["errors"]}, status=400)
    return None