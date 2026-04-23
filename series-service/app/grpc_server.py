import grpc
from concurrent import futures
from requests.exceptions import HTTPError, RequestException

# Fichiers générés par gRPC
from grpc_files import series_pb2
from grpc_files import series_pb2_grpc

# Ta propre fonction qui interroge TVMaze !
from app.services.series_service import get_series_details

class SeriesValidatorServicer(series_pb2_grpc.SeriesValidatorServicer):
    
    def CheckSeriesExists(self, request, context):
        try:
            # On demande à TVMaze si l'ID existe en utilisant ta fonction
            get_series_details(request.series_id)
            
            # Si aucune exception n'est levée, la série existe !
            return series_pb2.SeriesResponse(exists=True)
            
        except HTTPError as e:
            # Si TVMaze renvoie une erreur HTTP 404, la série n'existe pas
            if e.response is not None and e.response.status_code == 404:
                return series_pb2.SeriesResponse(exists=False)
            
            # Si TVMaze renvoie une autre erreur (ex: 500), on bloque par sécurité
            return series_pb2.SeriesResponse(exists=False)
            
        except RequestException:
            # Si TVMaze est hors ligne ou inaccessible
            return series_pb2.SeriesResponse(exists=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    series_pb2_grpc.add_SeriesValidatorServicer_to_server(SeriesValidatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()