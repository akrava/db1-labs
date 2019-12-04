-- Creating dictionary with bad words

CREATE TABLE IF NOT EXISTS prohibited_items_dict (
    id serial PRIMARY KEY,
    word varchar(255) NOT NULL
);

TRUNCATE prohibited_items_dict RESTART IDENTITY;
INSERT INTO prohibited_items_dict (word) VALUES ('aerosol'), ('gun'), ('batteries');

-- Trigger below

CREATE OR REPLACE function goods_trigger() returns trigger as $$
    declare
        description_with_time text;
        current_word prohibited_items_dict.word%TYPE;
    begin
        if old is not null and old.weight != new.weight then
            INSERT INTO reweightings (weight_before, weight_after, date_inspection, parcel_id)
                VALUES (old.weight, new.weight, current_timestamp, new.id);
        elseif old is null then
            description_with_time = coalesce(new.description, '') || ' added to db at: ' || current_timestamp::char(19);
            UPDATE goods SET description = description_with_time WHERE id = new.id;
        end if;
        for current_word in SELECT word FROM prohibited_items_dict loop
            if new.description ilike '%' || current_word || '%' then
                raise 'This item is prohibited';
            end if;
        end loop;
        return new;
        exception
            when no_data_found then
            when too_many_rows then
                raise 'Could not check description, try again later';
    end;
$$ language plpgsql;

DROP trigger IF EXISTS goods_helper on goods;
CREATE trigger goods_helper AFTER UPDATE OR INSERT on goods for each row EXECUTE procedure goods_trigger();
