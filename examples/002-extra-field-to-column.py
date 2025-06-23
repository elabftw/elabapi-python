#!/usr/bin/env python

###################################################################################################################
# In this example script, we want to grab information from metadata and add it to the Resource as a proper column #
###################################################################################################################

import elabapi_python
import json

# use the locally defined client.py module to get the api_client object, fully configured and ready to be used to instantiate api objects
from client import api_client

# Start by creating our api object to interact with /items endpoint
items_client = elabapi_python.ItemsApi(api_client)

# In this example, this corresponds to "Chemicals". Adapt to your instance.
RESOURCE_CATEGORY_ID = 5
# this value is the same for all eLabFTW instances
CURRENCY_EUROS = 4

# we need to use _preload_content=False here so we can access the metadata properly
response = items_client.read_items(cat=RESOURCE_CATEGORY_ID, limit=9999, _preload_content=False)
items = json.loads(response.data.decode('utf-8'))
for item in items:
    metadata = item.get('metadata', None)
    # they are supposed to all have metadata
    if metadata is None:
        print(f"WARNING: Skipping item with id {item.get('id')} because no metadata is present")
        continue
    meta = json.loads(metadata)
    extra_fields = meta.get('extra_fields', None)
    if extra_fields is not None:
        proc_pack_qty = extra_fields.get("Quantity", {"value": "1"}).get("value")
        proc_price_notax = extra_fields.get("Price", {"value": "0.00"}).get("value")
        # ensure we have a dot separator and a string
        proc_price_notax = str(proc_price_notax).replace(",",".")
        # ensure empty value is 0.00
        if proc_price_notax == "":
            proc_price_notax = "0.00"
        proc_price_tax = float(proc_price_notax) * 1.2
        # no patch the item with these values
        print(f"INFO: Patching item with id {item.get('id')}")
        items_client.patch_item(item.get('id'), body={"proc_pack_qty": proc_pack_qty, "proc_price_notax": proc_price_notax, "proc_price_tax": proc_price_tax, "proc_currency": CURRENCY_EUROS})
