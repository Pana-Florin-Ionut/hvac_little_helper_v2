SELECT test_offer.id,
    manufactured_generated_test_offer.product_type,
    manufactured_generated_test_offer.characteristics,
    manufactured_generated_test_offer.um,
    manufactured_generated_test_offer.quantity,
    manufactured_generated_test_offer.price_per_um,
    manufactured_generated_test_offer.total_price,
    test_offer.category,
    test_offer.observations
FROM test_offer
    RIGHT JOIN manufactured_generated_test_offer USING (id);
------
CREATE TABLE IF NOT EXIST products AS
SELECT test_offer.id,
    manufactured_generated_test_offer.product_type,
    manufactured_generated_test_offer.characteristics,
    manufactured_generated_test_offer.um,
    manufactured_generated_test_offer.quantity,
    manufactured_generated_test_offer.price_per_um,
    manufactured_generated_test_offer.total_price,
    test_offer.category,
    test_offer.observations
FROM test_offer
    RIGHT JOIN manufactured_generated_test_offer USING (id)