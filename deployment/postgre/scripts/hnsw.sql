\c ragdb ragdb_mgmt_user;

-- Create HNSW index
CREATE INDEX ON rag.text_segments USING hnsw (embedding vector_cosine_ops);


