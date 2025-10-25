#!/usr/bin/env python
import elabapi_python
from client import api_client

# define which category's items are patched
RESOURCE_CATEGORY_ID = 3

# Synchronize metadata of the item_type with existing items
# See: https://github.com/elabftw/elabftw/issues/3524

# create an instance of Items api
itemsApi = elabapi_python.ItemsApi(api_client)

metadata = '{"elabftw": {"extra_fields_groups": [{"id": 1,"name": "Drug settings"},{"id": 2,"name": "Mice info"}]},"extra_fields": {"Drug addition": {"type": "datetime-local","value": "","group_id": 1,"required": true,"description": "Time when drug is added"},"Drug concentration": {"type": "number","unit": "mM","units": ["mM","μM","nM"],"value": "","group_id": 1,"required": true},"Mouse sex": {"type": "select","value": "Male","options": ["Male","Female"],"group_id": 2}}}'

for item in itemsApi.read_items(cat=RESOURCE_CATEGORY_ID, limit=9999):
    # skip items with metadata already
    if not item.metadata:
        print(f'Patching item {item.id}')
        itemsApi.patch_item(item.id, body={'metadata': metadata})
