import urllib.parse as up
import psycopg2
import json

f = open('./config.json')
data = json.load(f)

conn = psycopg2.connect(f"""dbname='{data['dbname']}' user='{data['user']}' host='{data['host']}' password='{data['password']}'""")


sql = """
CREATE TABLE personagem (
    personagem_id SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    fk_grupo_grupo_id SERIAL
);

CREATE TABLE shadow (
    codinome VARCHAR(200),
    fk_persona_persona_id SERIAL PRIMARY KEY
);

CREATE TABLE persona (
    persona_id SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    link_foto VARCHAR(5000)
);

CREATE TABLE atributo (
    atributo_id SERIAL PRIMARY KEY,
    nome VARCHAR(50)
);

CREATE TABLE arcana (
    arcana_id SERIAL PRIMARY KEY,
    nome VARCHAR(50)
);

CREATE TABLE interacao_elemento (
    interacao_id SERIAL PRIMARY KEY,
    nome_interacao VARCHAR(50)
);

CREATE TABLE persona_atributo (
    valor INTEGER,
    fk_atributo_atributo_id SERIAL,
    fk_persona_persona_id SERIAL
);

CREATE TABLE habilidade (
    habilidade_id SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    fk_atributo_atributo_id SERIAL,
    fk_intensidade_intensidade_id SERIAL,
    fk_elemento_elemento_id SERIAL
);

CREATE TABLE intensidade (
    intensidade_id SERIAL PRIMARY KEY,
    nome VARCHAR(50)
);

CREATE TABLE habilidade_persona (
    nivel INTEGER,
    fk_habilidade_habilidade_id SERIAL,
    fk_persona_persona_id SERIAL
);

CREATE TABLE personagem_persona (
    nivel INTEGER,
    fk_personagem_personagem_id SERIAL,
    fk_persona_persona_id SERIAL
);

CREATE TABLE crescimento_atributo (
    crescimento_id SERIAL PRIMARY KEY,
    nivel INTEGER,
    quantidade INTEGER,
    fk_persona_persona_id SERIAL,
    fk_atributo_atributo_id SERIAL
);

CREATE TABLE item (
    item_id SERIAL PRIMARY KEY,
    nome VARCHAR(50)
);

CREATE TABLE grupo (
    grupo_id SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    dinheiro INTEGER
);

CREATE TABLE elemento (
    elemento_id SERIAL PRIMARY KEY,
    nome VARCHAR(50)
);

CREATE TABLE reacao_elemental (
    fk_persona_persona_id SERIAL,
    fk_elemento_elemento_id SERIAL,
    fk_interacao_elemento_interacao_id SERIAL
);

CREATE TABLE persona_arcana (
    fk_persona_persona_id SERIAL,
    fk_arcana_arcana_id SERIAL
);

CREATE TABLE persona_habilidade (
    fk_habilidade_habilidade_id SERIAL
);

CREATE TABLE inventario (
    fk_grupo_grupo_id SERIAL,
    fk_item_item_id SERIAL
);

CREATE TABLE drop (
    fk_shadow_fk_persona_persona_id SERIAL,
    fk_item_item_id SERIAL
);
 
ALTER TABLE personagem ADD CONSTRAINT FK_personagem_2
    FOREIGN KEY (fk_grupo_grupo_id)
    REFERENCES grupo (grupo_id)
    ON DELETE CASCADE;
 
ALTER TABLE shadow ADD CONSTRAINT FK_shadow_2
    FOREIGN KEY (fk_persona_persona_id)
    REFERENCES persona (persona_id)
    ON DELETE CASCADE;
 
ALTER TABLE persona_atributo ADD CONSTRAINT FK_persona_atributo_1
    FOREIGN KEY (fk_atributo_atributo_id)
    REFERENCES atributo (atributo_id);
 
ALTER TABLE persona_atributo ADD CONSTRAINT FK_persona_atributo_2
    FOREIGN KEY (fk_persona_persona_id)
    REFERENCES persona (persona_id);
 
ALTER TABLE habilidade ADD CONSTRAINT FK_habilidade_2
    FOREIGN KEY (fk_atributo_atributo_id)
    REFERENCES atributo (atributo_id)
    ON DELETE CASCADE;
 
ALTER TABLE habilidade ADD CONSTRAINT FK_habilidade_3
    FOREIGN KEY (fk_intensidade_intensidade_id)
    REFERENCES intensidade (intensidade_id)
    ON DELETE CASCADE;
 
ALTER TABLE habilidade ADD CONSTRAINT FK_habilidade_4
    FOREIGN KEY (fk_elemento_elemento_id)
    REFERENCES elemento (elemento_id)
    ON DELETE CASCADE;
 
ALTER TABLE habilidade_persona ADD CONSTRAINT FK_habilidade_persona_1
    FOREIGN KEY (fk_habilidade_habilidade_id)
    REFERENCES habilidade (habilidade_id);
 
ALTER TABLE habilidade_persona ADD CONSTRAINT FK_habilidade_persona_2
    FOREIGN KEY (fk_persona_persona_id)
    REFERENCES persona (persona_id);
 
ALTER TABLE personagem_persona ADD CONSTRAINT FK_personagem_persona_1
    FOREIGN KEY (fk_personagem_personagem_id)
    REFERENCES personagem (personagem_id);
 
ALTER TABLE personagem_persona ADD CONSTRAINT FK_personagem_persona_2
    FOREIGN KEY (fk_persona_persona_id)
    REFERENCES persona (persona_id);
 
ALTER TABLE crescimento_atributo ADD CONSTRAINT FK_crescimento_atributo_2
    FOREIGN KEY (fk_persona_persona_id)
    REFERENCES persona (persona_id)
    ON DELETE CASCADE;
 
ALTER TABLE crescimento_atributo ADD CONSTRAINT FK_crescimento_atributo_3
    FOREIGN KEY (fk_atributo_atributo_id)
    REFERENCES atributo (atributo_id)
    ON DELETE CASCADE;
 
ALTER TABLE reacao_elemental ADD CONSTRAINT FK_reacao_elemental_1
    FOREIGN KEY (fk_persona_persona_id)
    REFERENCES persona (persona_id);
 
ALTER TABLE reacao_elemental ADD CONSTRAINT FK_reacao_elemental_2
    FOREIGN KEY (fk_elemento_elemento_id)
    REFERENCES elemento (elemento_id);
 
ALTER TABLE reacao_elemental ADD CONSTRAINT FK_reacao_elemental_3
    FOREIGN KEY (fk_interacao_elemento_interacao_id)
    REFERENCES interacao_elemento (interacao_id);
 
ALTER TABLE persona_arcana ADD CONSTRAINT FK_persona_arcana_1
    FOREIGN KEY (fk_persona_persona_id)
    REFERENCES persona (persona_id)
    ON DELETE SET NULL;
 
ALTER TABLE persona_arcana ADD CONSTRAINT FK_persona_arcana_2
    FOREIGN KEY (fk_arcana_arcana_id)
    REFERENCES arcana (arcana_id)
    ON DELETE SET NULL;
 
ALTER TABLE persona_habilidade ADD CONSTRAINT FK_persona_habilidade_1
    FOREIGN KEY (fk_habilidade_habilidade_id)
    REFERENCES habilidade (habilidade_id)
    ON DELETE RESTRICT;
 
ALTER TABLE inventario ADD CONSTRAINT FK_inventario_1
    FOREIGN KEY (fk_grupo_grupo_id)
    REFERENCES grupo (grupo_id)
    ON DELETE SET NULL;
 
ALTER TABLE inventario ADD CONSTRAINT FK_inventario_2
    FOREIGN KEY (fk_item_item_id)
    REFERENCES item (item_id)
    ON DELETE SET NULL;
 
ALTER TABLE drop ADD CONSTRAINT FK_drop_1
    FOREIGN KEY (fk_shadow_fk_persona_persona_id)
    REFERENCES shadow (fk_persona_persona_id)
    ON DELETE SET NULL;
 
ALTER TABLE drop ADD CONSTRAINT FK_drop_2
    FOREIGN KEY (fk_item_item_id)
    REFERENCES item (item_id)
    ON DELETE SET NULL;
"""
try:
    # create a new cursor
    cur = conn.cursor()
    # execute the INSERT statement
    cur.execute(sql)
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()