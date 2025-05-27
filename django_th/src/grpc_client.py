from .config import settings
import grpc
import product_pb2
import product_pb2_grpc
from concurrent import futures
import requests
import json
import graphene


class ProductService(product_pb2_grpc.ProductServiceServicer):
    def GetProduct(self, request, context):
        url = settings.SALEOR_GRAPHQL_URL
        headers = {
            "Authorization": f"Bearer {settings.SALEOR_API_TOKEN}",
            "Content-Type": "application/json",
        }

        query = """
            query GetProduct($id: ID!, $channel: String!) {
                product(id: $id, channel: $channel) {
                    id
                    name
                }
            }
        """

        variables = {
            "id": str(request.id),
            "channel": "default-channel"
        }

        payload = {"query": query, "variables": variables}

        try:
            # Debug request
            print(f"\nSending to Saleor: {json.dumps(payload, indent=2)}")
            
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            
            # Debug response
            print(f"Received from Saleor: {json.dumps(result, indent=2)}")

            if "errors" in result:
                error_msg = result["errors"][0]["message"]
                raise Exception(f"GraphQL Error: {error_msg}")

            product = result.get("data", {}).get("product")
            if not product:
                raise Exception("Product not found in response")

            # Xử lý pricing an toàn
            try:
                price = product["pricing"]["priceRange"]["start"]["gross"]["amount"]
            except (KeyError, TypeError):
                price = 0.0  # Giá trị mặc định nếu không có pricing

            return product_pb2.GetProductResponse(
                id=product["id"],
                name=product["name"],
            )

        except Exception as e:
            print(f"\nERROR DETAILS: {str(e)}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Error: {str(e)}")
            return product_pb2.GetProductResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Server running on port 50051...")
    server.wait_for_termination()

def run_client():
    """Hàm test client tích hợp trong cùng file"""
    channel = grpc.insecure_channel('localhost:50051')
    stub = product_pb2_grpc.ProductServiceStub(channel)
    
    try:
        print("\nTesting GetProduct with ID=1...")
        response = stub.GetProduct(product_pb2.GetProductRequest(id="UHJvZHVjdDoxNjk="))
        print(f"Response received: ID={response.id}, Name={response.name}, Price={response.price}")
    except grpc.RpcError as e:
        print(f"RPC failed: {e.code()}: {e.details()}")

if __name__ == "__main__":
    # Chạy server trong thread riêng để có thể test client cùng lúc
    import threading
    server_thread = threading.Thread(target=serve, daemon=True)
    server_thread.start()
    
    # Chạy client test sau khi server khởi động
    import time
    time.sleep(1)  # Đợi server khởi động
    run_client()
    
    # Giữ chương trình chạy
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")