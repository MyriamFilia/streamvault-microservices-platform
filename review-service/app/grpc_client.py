import os
import grpc
from fastapi import HTTPException

from grpc_files import series_pb2
from grpc_files import series_pb2_grpc

SERIES_GRPC_ADDR = os.getenv("SERIES_SERVICE_ADDR", "localhost:50051")

def check_series_exists(series_id: int) -> bool:
    try:
        with grpc.insecure_channel(SERIES_GRPC_ADDR) as channel:
            stub = series_pb2_grpc.SeriesValidatorStub(channel)
            request = series_pb2.SeriesRequest(series_id=series_id)
            response = stub.CheckSeriesExists(request)
            
            return response.exists

    except grpc.RpcError as e:
        print(f"error network gRPC : {e}")
        raise HTTPException(
            status_code=503, 
            detail="not able to connect to series-service"
        )
