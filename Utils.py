from fastapi import Query
from fastapi_pagination import Params

class Params(Params):
    size: int = Query(20, ge=1, le=1_000, description="Page size")