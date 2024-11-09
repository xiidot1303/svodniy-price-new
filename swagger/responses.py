from swagger import *

personal_data_by_passport_schema_dict = {
    "200": openapi.Response(
        description='',
        schema=openapi.Schema(
            type="object",
            properties={
                "pnfl": openapi.Schema(type="string"), 
                "surname": openapi.Schema(type="string"), 
                "name": openapi.Schema(type="string"), 
                "patronym": openapi.Schema(type="string"), 
                "birth_place": openapi.Schema(type="string"), 
                "nationality": openapi.Schema(type="string"), 
                "doc_give_place": openapi.Schema(type="string"), 
                "date_begin_document": openapi.Schema(type="string"), 

            },
            required=[],  # Specify required properties
        ),
        # examples={
        #     "application/json": {
        #         "key1": "value1",
        #         "key2": 123,
        #     },
        # },
    ),
}

can_order_response = {
    "200": openapi.Response(
        description='',
        schema=openapi.Schema(
            type="object",
            properties={
                "response": openapi.Schema(type="boolen")
            },
            required=["response"]
        )
    )
}

drug_list_response = {
    "200": openapi.Response(
        description='',
        schema=openapi.Schema(
            type='object',
            properties={
                "next": openapi.Schema(type="string"),
                "results": openapi.Schema(
                    type="array",
                    items=[
                        openapi.Schema(
                            type='object',
                            properties={
                                "title": openapi.Schema(type="string"),
                                "title_en": openapi.Schema(type="string"),
                                "term": openapi.Schema(type="string"),
                                "atc": openapi.Schema(type="string"),
                            }
                        )
                    ]

                )
            }
        )
    )
}
