\c ragdb ragdb_mgmt_user;

-- Create ivfflat index
CREATE INDEX ON rag.text_segments USING ivfflat (embedding vector_cosine_ops) WITH (lists = 175);


