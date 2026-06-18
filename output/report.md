# Oracle Mining Report

- Endpoint: `GET /shop/2/category/4/items/?start=0&limit=10&language_code=en`
- Mining source: `llm(llama-3.3-70b-versatile)`
- Constraints checked: 108
- PASS: 96
- FAIL: 12
- Unique mismatch fields: 12

## Schema mismatches (spec vs reality)

### Schema mismatch #1
- Field: `serializer_data.serializer_data[1].code`
- Rule: Field 'serializer_data.serializer_data[*].code' must be of type 'string'.
- Detail: expected string, got int (value=16000438408)

### Schema mismatch #2
- Field: `serializer_data.serializer_data[0].quantity`
- Rule: Field 'serializer_data.serializer_data[*].quantity' must be of type 'number'.
- Detail: expected number, got str (value='23')

### Schema mismatch #3
- Field: `serializer_data.serializer_data[1].sell_price`
- Rule: Field 'serializer_data.serializer_data[*].sell_price' must be of type 'number'.
- Detail: expected number, got str (value='15.0')

## Downstream assumption mismatches (nullable field assumed present)

### Downstream mismatch #1
- Field: `serializer_data.serializer_data[0].name_en`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].name_en' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

### Downstream mismatch #2
- Field: `serializer_data.serializer_data[1].name_en`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].name_en' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

### Downstream mismatch #3
- Field: `serializer_data.serializer_data[2].name_en`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].name_en' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

### Downstream mismatch #4
- Field: `serializer_data.serializer_data[0].image`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].image' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

### Downstream mismatch #5
- Field: `serializer_data.serializer_data[1].image`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].image' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

### Downstream mismatch #6
- Field: `serializer_data.serializer_data[0].discount_price`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].discount_price' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

### Downstream mismatch #7
- Field: `serializer_data.serializer_data[1].discount_price`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].discount_price' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

### Downstream mismatch #8
- Field: `serializer_data.serializer_data[0].discounted_quantity`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].discounted_quantity' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

### Downstream mismatch #9
- Field: `serializer_data.serializer_data[1].discounted_quantity`
- Rule: Downstream assumes 'serializer_data.serializer_data[*].discounted_quantity' is present and non-null (spec marks it nullable).
- Detail: nullable in spec but downstream assumes present (value=None)

## All checks

- [FAIL] `serializer_data.serializer_data[1].code` :: expected string, got int (value=16000438408)
- [FAIL] `serializer_data.serializer_data[0].quantity` :: expected number, got str (value='23')
- [FAIL] `serializer_data.serializer_data[1].sell_price` :: expected number, got str (value='15.0')
- [FAIL] `serializer_data.serializer_data[0].name_en` :: nullable in spec but downstream assumes present (value=None)
- [FAIL] `serializer_data.serializer_data[1].name_en` :: nullable in spec but downstream assumes present (value=None)
- [FAIL] `serializer_data.serializer_data[2].name_en` :: nullable in spec but downstream assumes present (value=None)
- [FAIL] `serializer_data.serializer_data[0].image` :: nullable in spec but downstream assumes present (value=None)
- [FAIL] `serializer_data.serializer_data[1].image` :: nullable in spec but downstream assumes present (value=None)
- [FAIL] `serializer_data.serializer_data[0].discount_price` :: nullable in spec but downstream assumes present (value=None)
- [FAIL] `serializer_data.serializer_data[1].discount_price` :: nullable in spec but downstream assumes present (value=None)
- [FAIL] `serializer_data.serializer_data[0].discounted_quantity` :: nullable in spec but downstream assumes present (value=None)
- [FAIL] `serializer_data.serializer_data[1].discounted_quantity` :: nullable in spec but downstream assumes present (value=None)
- [PASS] `serializer_data` :: pass
- [PASS] `serializer_data.total_size` :: pass
- [PASS] `serializer_data.limit` :: pass
- [PASS] `serializer_data.start` :: pass
- [PASS] `serializer_data.serializer_data` :: pass
- [PASS] `serializer_data.total_size` :: pass
- [PASS] `serializer_data.limit` :: pass
- [PASS] `serializer_data.start` :: pass
- [PASS] `serializer_data.serializer_data` :: pass
- [PASS] `serializer_data.serializer_data[0].id` :: pass
- [PASS] `serializer_data.serializer_data[1].id` :: pass
- [PASS] `serializer_data.serializer_data[2].id` :: pass
- [PASS] `serializer_data.serializer_data[0].id` :: pass
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
- [PASS] `serializer_data.serializer_data[1].shop` :: pass
- [PASS] `serializer_data.serializer_data[2].shop` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[2].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[2].unit.id` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[2].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[1].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[2].unit.name` :: pass
- [PASS] `serializer_data.serializer_data[0].unit.size` :: pass
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
- [PASS] `serializer_data.serializer_data[1].category.id` :: pass
- [PASS] `serializer_data.serializer_data[2].category.id` :: pass
- [PASS] `serializer_data.serializer_data[0].category.name` :: pass
- [PASS] `serializer_data.serializer_data[1].category.name` :: pass
- [PASS] `serializer_data.serializer_data[2].category.name` :: pass
- [PASS] `serializer_data.serializer_data[0].category.name` :: pass
- [PASS] `serializer_data.serializer_data[1].category.name` :: pass
- [PASS] `serializer_data.serializer_data[2].category.name` :: pass
- [PASS] `serializer_data.serializer_data[2].image` :: pass
- [PASS] `serializer_data.serializer_data[2].discount_price` :: pass
- [PASS] `serializer_data.serializer_data[2].discounted_quantity` :: pass