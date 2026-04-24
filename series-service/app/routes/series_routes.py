from fastapi import APIRouter, HTTPException, Query
from requests.exceptions import RequestException
from app.services.series_service import search_series, get_series_details ,get_popular_series

router = APIRouter(prefix="/api", tags=["Series"])


#Route racine pour vérifier que le service est opérationnel
@router.get("")
def root():
    return {"service": "series-service",
             "status": "running"}

@router.get("/health")
def health():
    return {"status": "UP"}


@router.get("/search")
def search_tv_series(
    q: str = Query(..., min_length=1)
):
    try:
        results = search_series(q)

        return {
            "query": q,
            "count": len(results),
            "results": results
        }

    except RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"External API error: {str(e)}"
        )



@router.get("/popular")
def popular_series():
    try:
        results = get_popular_series()
        return {
            "count": len(results),
            "results": results
        }
    except RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Erreur API externe : {str(e)}"
        )



@router.get("/{series_id}")
def series_details(series_id: int):
    try:
        return get_series_details(series_id)
    except RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erreur API externe : {str(e)}")
    


    