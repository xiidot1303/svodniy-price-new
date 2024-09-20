from swagger import *

drug_id_schema = openapi.Schema(
    type="object",
    properties={
        "id": openapi.Schema(type="integer")
    },
    required=['id']
)