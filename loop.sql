SELECT * FROM category;
CREATE TABLE category_copy AS SELECT * FROM category;

DO $$
	DECLARE
		category_id category_copy.category_id%TYPE;
		category_name category_copy.category_name%TYPE;
	BEGIN
		category_id := 5;
		category_name := 'TEST MEAL №';
		FOR counter IN 1..10
			LOOP
				INSERT INTO category_copy(category_id, category_name)
				VALUES (category_id + counter, category_name || counter);
			END LOOP;
END;
$$

SELECT * from category_copy;

DROP TABLE category_copy;