import os


SPARROW_CORE_GO_SERVICE = os.environ.get("SC_SPARROW_CORE_GO_SVC", "sparrow-core-go-svc:8001")

SPARROW_CORE_SERVICE = os.environ.get("SC_SPARROW_CORE_SVC", "sparrow-core-svc:8001")

SPARROW_LANYUE_SERVICE = os.environ.get("SC_SPARROW_LANYUE_SVC", "sparrow-lanyue-svc:8001")

SPARROW_PRODUCT_SERVICE = os.environ.get("SC_SPARROW_PRODUCT_SVC", "sparrow-product-svc:8001")
