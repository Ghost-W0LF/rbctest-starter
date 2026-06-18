# Oracle Mining Report

- Endpoint: `GET /shop/2/category/4/items/?start=0&limit=10&language_code=en`
- Mining source: `llm(llama-3.3-70b-versatile)`
- Constraints checked: 98
- PASS: 86
- FAIL: 12
- Unique mismatch fields: 11

## Mismatches (spec vs reality)

### Mismatch #1
- Field: `serializer_data.total_size`
- Rule: Field 'serializer_data.total_size' must be of type 'string'.
- Detail: expected string, got int (value=7)

### Mismatch #2
- Field: `serializer_data.limit`
- Rule: Field 'serializer_data.limit' must be of type 'string'.
- Detail: expected string, got int (value=10)

### Mismatch #3
- Field: `serializer_data.page`
- Rule: Field 'serializer_data.page' must exist in response.
- Detail: missing field 'serializer_data.page'

### Mismatch #4
- Field: `serializer_data.serializer_data[0].id`
- Rule: Field 'serializer_data.serializer_data[*].id' must be of type 'integer'.
- Detail: expected integer, got str (value='5')

### Mismatch #5
- Field: `serializer_data.serializer_data[1].code`
- Rule: Field 'serializer_data.serializer_data[*].code' must be of type 'string'.
- Detail: expected string, got int (value=16000438408)

### Mismatch #6
- Field: `serializer_data.serializer_data[0].quantity`
- Rule: Field 'serializer_data.serializer_data[*].quantity' must be of type 'number'.
- Detail: expected number, got str (value='23')

### Mismatch #7
- Field: `serializer_data.serializer_data[1].sell_price`
- Rule: Field 'serializer_data.serializer_data[*].sell_price' must be of type 'number'.
- Detail: expected number, got str (value='15.0')

### Mismatch #8
- Field: `serializer_data.serializer_data[1].shop`
- Rule: Field 'serializer_data.serializer_data[*].shop' must be of type 'integer'.
- Detail: expected integer, got str (value='2')

### Mismatch #9
- Field: `serializer_data.serializer_data[2].unit.id`
- Rule: Field 'serializer_data.serializer_data[*].unit.id' must be of type 'integer'.
- Detail: expected integer, got str (value='3')

### Mismatch #10
- Field: `serializer_data.serializer_data[0].unit.size`
- Rule: Field 'serializer_data.serializer_data[*].unit.size' must be of type 'integer'.
- Detail: expected integer, got str (value='5')

### Mismatch #11
- Field: `serializer_data.serializer_data[1].category.id`
- Rule: Field 'serializer_data.serializer_data[*].category.id' must be of type 'integer'.
- Detail: expected integer, got str (value='4')

## All checks

- [FAIL] `serializer_data.total_size` :: expected string, got int (value=7)
- [FAIL] `serializer_data.limit` :: expected string, got int (value=10)
- [FAIL] `serializer_data.page` :: missing field 'serializer_data.page'
- [FAIL] `serializer_data.serializer_data[0].id` :: expected integer, got str (value='5')
- [FAIL] `serializer_data.serializer_data[1].code` :: expected string, got int (value=16000438408)
- [FAIL] `serializer_data.serializer_data[0].quantity` :: expected number, got str (value='23')
- [FAIL] `serializer_data.serializer_data[1].sell_price` :: expected number, got str (value='15.0')
- [FAIL] `serializer_data.serializer_data[1].shop` :: expected integer, got str (value='2')
- [FAIL] `serializer_data.serializer_data[2].unit.id` :: expected integer, got str (value='3')
- [FAIL] `serializer_data.serializer_data[0].unit.size` :: expected integer, got str (value='5')
- [FAIL] `serializer_data.serializer_data[1].category.id` :: expected integer, got str (value='4')
- [PASS] `serializer_data` :: pass
- [PASS] `serializer_data.start` :: pass
- [PASS] `serializer_data.serializer_data` :: pass
- [PASS] `serializer_data.total_size` :: pass
- [PASS] `serializer_data.limit` :: pass
- [PASS] `serializer_data.start` :: pass
- [PASS] `serializer_data.serializer_data` :: pass
- [PASS] `serializer_data.serializer_data[0].id` :: pass
- [PASS] `serializer_data.serializer_data[1].id` :: pass
- [PASS] `serializer_data.serializer_data[2].id` :: pass
- [PASS] `serializer_data.serializer_data[1].id` :: pass
- [PASS] `serializer_data.serializer_data[2].id` :: pass
- [PASS] `serializer_data.serializer_data[0].name` :: pass
- [PASS] `serializer_data.serializer_data[1].name` :: pass
- [PASS] `serializer_data.serializer_data[2].name` :: pass
- [PASS] `serializer_data.serializer_data[0].name` :: pass
- [PASS] `serializer_data.serializer_data[1].name` :: pass
- [PASS] `serializer_data.serializer_data[2].name` :: pass
- [PASS] `serializer_data.serializer_data[0].name_en` :: pass
- [PASS] `serializer_data.serializer_data[1].name_en` :: pass
- [PASS] `serializer_data.serializer_data[2].name_en` :: pass
- [PASS] `serializer_data.serializer_data[0].code` :: pass
- [PASS] `serializer_data.serializer_data[1].code` :: pass
- [PASS] `serializer_data.serializer_data[2].code` :: pass
- [PASS] `serializer_data.serializer_data[0].code` :: pass
- [PASS] `serializer_data.serializer_data[2].code` :: pass
- [PASS] `serializer_data.serializer_data[1].quantity` :: pass
- [PASS] `serializer_data.serializer_data[2].quantity` :: pass
- [PASS] `serializer_data.serializer_data[0].image` :: pass
- [PASS] `serializer_data.serializer_data[1].image` :: pass
- [PASS] `serializer_data.serializer_data[2].image` :: pass
- [PASS] `serializer_data.serializer_data[0].sell_price` :: pass
- [PASS] `serializer_data.serializer_data[1].sell_price` :: pass
- [PASS] `serializer_data.serializer_data[2].sell_price` :: pass
- [PASS] `serializer_data.serializer_data[0].sell_price` :: pass
- [PASS] `serializer_data.serializer_data[2].sell_price` :: pass
- [PASS] `serializer_data.serializer_data[0].actual_price` :: pass
- [PASS] `serializer_data.serializer_data[1].actual_price` :: pass
- [PASS] `serializer_data.serializer_data[2].actual_price` :: pass
- [PASS] `serializer_data.serializer_data[0].discount_price` :: pass
- [PASS] `serializer_data.serializer_data[1].discount_price` :: pass
- [PASS] `serializer_data.serializer_data[2].discount_price` :: pass
- [PASS] `serializer_data.serializer_data[0].discounted_quantity` :: pass
- [PASS] `serializer_data.serializer_data[1].discounted_quantity` :: pass
- [PASS] `serializer_data.serializer_data[2].discounted_quantity` :: pass
- [PASS] `serializer_data.serializer_data[0].shop` :: pass
- [PASS] `serializer_data.serializer_data[1].shop` :: pass
- [PASS] `serializer_data.serializer_data[2].shop` :: pass
- [PASS] `serializer_data.serializer_data[0].shop` :: pass
- [PASS] `serializer_data.serializer_data[2].shop` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[2].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[2].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[2].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.size` :: pass
- [PASS] `serializer_data.serializer_data[2].unit.size` :: pass
- [PASS] `serializer_data.serializer_data[0].vat_category.id` :: pass
- [PASS] `serializer_data.serializer_data[1].vat_category.id` :: pass
- [PASS] `serializer_data.serializer_data[2].vat_category.id` :: pass
- [PASS] `serializer_data.serializer_data[0].vat_category.id` :: pass
- [PASS] `serializer_data.serializer_data[1].vat_category.id` :: pass
- [PASS] `serializer_data.serializer_data[2].vat_category.id` :: pass
- [PASS] `serializer_data.serializer_data[0].vat_category.name` :: pass
- [PASS] `serializer_data.serializer_data[1].vat_category.name` :: pass
- [PASS] `serializer_data.serializer_data[2].vat_category.name` :: pass
- [PASS] `serializer_data.serializer_data[0].vat_category.name` :: pass
- [PASS] `serializer_data.serializer_data[1].vat_category.name` :: pass
- [PASS] `serializer_data.serializer_data[2].vat_category.name` :: pass
- [PASS] `serializer_data.serializer_data[0].category.id` :: pass
- [PASS] `serializer_data.serializer_data[1].category.id` :: pass
- [PASS] `serializer_data.serializer_data[2].category.id` :: pass
- [PASS] `serializer_data.serializer_data[0].category.id` :: pass
- [PASS] `serializer_data.serializer_data[2].category.id` :: pass
- [PASS] `serializer_data.serializer_data[0].category.name` :: pass
- [PASS] `serializer_data.serializer_data[1].category.name` :: pass
- [PASS] `serializer_data.serializer_data[2].category.name` :: pass
- [PASS] `serializer_data.serializer_data[0].category.name` :: pass
- [PASS] `serializer_data.serializer_data[1].category.name` :: pass
- [PASS] `serializer_data.serializer_data[2].category.name` :: pass