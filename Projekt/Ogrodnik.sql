PRAGMA foreign_keys = 1;
PRAGMA foreign_keys;

DROP TABLE "ogrodnik_user";

CREATE TABLE "ogrodnik_user"
(
    "user_id"               INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "nick"                  VARCHAR(64)     NOT NULL UNIQUE,
    "name"                  VARCHAR(256)    NOT NULL,
    "surname"               VARCHAR(256)    NOT NULL,
    "email"                 VARCHAR(256)    NOT NULL UNIQUE,
    "registration_date"     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_login"            TIMESTAMP,
    "password"              VARCHAR(512)    NOT NULL,
    "admin"                 BOOLEAN         DEFAULT FALSE
);

INSERT INTO "ogrodnik_user" (nick, name, surname, email, password, admin) VALUES ("admin", "admin", "admin", "admin@admin.pl", "5c784498fa613f29b1b5cbef397e006a49b2ede33ba1bfcd7379521178139a4d19d21cb280da182c1d679fae927982bb60bd80abb411a72de24578d9d6b023d6", 1);


DROP TABLE "ogrodnik_session";

CREATE TABLE "ogrodnik_session"
(
    "session_id"            VARCHAR(256)    NOT NULL UNIQUE,
    "atime"                 TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "data"                  TEXT
);

DROP TABLE "ogrodnik_garden";

CREATE TABLE "ogrodnik_garden"
(
    "garden_id"             INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id"               INTEGER         NOT NULL REFERENCES "ogrodnik_user" ON DELETE CASCADE,
    "name"                  VARCHAR(256)    NOT NULL,
    "creation_date"         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE "ogrodnik_field";

CREATE TABLE "ogrodnik_field"
(
    "field_id"              INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "garden_id"             INTEGER         NOT NULL REFERENCES "ogrodnik_garden" ON DELETE CASCADE,
    "x"                     INTEGER         NOT NULL,
    "y"                     INTEGER         NOT NULL
);

DROP TABLE "ogrodnik_plant";

CREATE TABLE "ogrodnik_plant"
(
    "plant_id"              INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id"               INTEGER         REFERENCES "ogrodnik_user" ON DELETE SET NULL, -- kto dodał roślinę do bazy
    "name"                  VARCHAR(256)    NOT NULL
);

DROP TABLE "ogrodnik_product";

CREATE TABLE "ogrodnik_product"
(
    "product_id"            INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id"               INTEGER         REFERENCES "ogrodnik_user" ON DELETE SET NULL, -- kto dodał produkt do bazy
    "name"                  VARCHAR(256)    NOT NULL UNIQUE
);

DROP TABLE "ogrodnik_placement";

CREATE TABLE "ogrodnik_placement"
(
    "placement_id"          INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "plant_id"              INTEGER         NOT NULL REFERENCES "ogrodnik_plant" ON DELETE CASCADE,
    "name"                  VARCHAR(256)    NOT NULL,
    "comment"               TEXT,
    "placement_date"        TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "finish_date"           TIMESTAMP
);

DROP TABLE "ogrodnik_placement_field";

CREATE TABLE "ogrodnik_placement_field"
(
    "placement_id"          INTEGER         NOT NULL REFERENCES "ogrodnik_placement" ON DELETE CASCADE,
    "field_id"              INTEGER         NOT NULL REFERENCES "ogrodnik_field" ON DELETE CASCADE,
    CONSTRAINT "distinct"   UNIQUE ("placement_id", "field_id")
);

DROP TABLE "ogrodnik_placement_product";

CREATE TABLE "ogrodnik_placement_product"
(
    "placement_product_id"  INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "placement_id"          INTEGER         NOT NULL REFERENCES "ogrodnik_placement" ON DELETE CASCADE,
    "product_id"            INTEGER         NOT NULL REFERENCES "ogrodnik_product" ON DELETE CASCADE,
    "production_date"       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "count"                 INTEGER         NOT NULL DEFAULT 1
);

DROP TABLE "ogrodnik_shop";

CREATE TABLE "ogrodnik_shop"
(
    "shop_id"               INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id"               INTEGER         REFERENCES "ogrodnik_user" ON DELETE SET NULL, -- kto dodał sklep do bazy
    "name"                  VARCHAR(256)    NOT NULL,
    "address"               VARCHAR(256)    NOT NULL,
    CONSTRAINT "valid"      UNIQUE ("name", "address")
);

DROP TABLE "ogrodnik_warehouse_product";

CREATE TABLE "ogrodnik_warehouse_product"
(
    "warehouse_product_id"  INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id"               INTEGER         NOT NULL REFERENCES "ogrodnik_user" ON DELETE CASCADE,
    "product_id"            INTEGER         NOT NULL REFERENCES "ogrodnik_product" ON DELETE CASCADE,
    "count"                 INTEGER         NOT NULL DEFAULT 1,
    "obtained_date"         TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "placement_id"          INTEGER         REFERENCES "ogrodnik_placement" ON DELETE RESTRICT,
    "shop_id"               INTEGER         REFERENCES "ogrodnik_shop" ON DELETE RESTRICT,
    "comment"               TEXT,
    "price"                 REAL            NOT NULL DEFAULT 0,
    CONSTRAINT "valid"      CHECK (("shop_id" IS NOT NULL AND "placement_id" IS NULL) OR ("shop_id" IS NULL AND "placement_id" IS NOT NULL))
);

DROP TABLE "ogrodnik_event";

CREATE TABLE "ogrodnik_event"
(
    "event_id"              INTEGER         PRIMARY KEY AUTOINCREMENT NOT NULL,
    "placement_id"          INTEGER         NOT NULL REFERENCES "ogrodnik_placement" ON DELETE CASCADE,
    "name"                  VARCHAR(256)    NOT NULL,
    "description"           TEXT            NOT NULL,
    "from_date"             TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "to_date"               TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "end_date"              TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "frequency"             INTEGER         NOT NULL DEFAULT 0
);

DROP TABLE "ogrodnik_event_requirement";

CREATE TABLE "ogrodnik_event_requirement"
(
    "event_id"              INTEGER         NOT NULL REFERENCES "ogrodnik_event" ON DELETE CASCADE,
    "product_id"            INTEGER         NOT NULL REFERENCES "ogrodnik_product" ON DELETE CASCADE,
    CONSTRAINT "distinct"   UNIQUE ("event_id", "product_id")
);
