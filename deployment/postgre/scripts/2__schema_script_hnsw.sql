\c ragdb ragdb_mgmt_user;

-- Types
create type rag.source_type as enum ('SIGRID_DOCS', 'SLACK', 'SHAREPOINT', 'CONFLUENCE', 'SALESFORCE');

alter type rag.source_type owner to ragdb_mgmt_user;

create type rag.classification_label_type as enum ('PUBLIC', 'SENSITIVE', 'CONFIDENTIAL');

alter type rag.classification_label_type owner to ragdb_mgmt_user;

-- Documents
create table rag.documents
(
    id                        bigserial
        primary key,
    created_at                timestamp,
    updated_at                timestamp,
    name                      text,
    content                   text,
    metadata                  jsonb,
    reference_uri             text,
    indexed_at                timestamp default CURRENT_TIMESTAMP not null,
    source_type               source_type                         not null,
    classification_label_type classification_label_type           not null,
    full_path                 text
        constraint documents_full_path_unique_key
            unique
);

alter table rag.documents
    owner to ragdb_mgmt_user;

grant select on rag.documents to chatbot_read_user;

grant delete, insert, select, update on rag.documents to document_ingestion_write_user;

-- Text segments

create table rag.text_segments
(
    id          bigserial
        primary key,
    document_id bigint
        references rag.documents
            on delete cascade,
    content     text,
    metadata    jsonb,
    embedding   vector(1024)
);

-- Create HNSW index
CREATE INDEX ON rag.text_segments USING hnsw (embedding vector_cosine_ops);

alter table rag.text_segments
    owner to ragdb_mgmt_user;

grant select on rag.text_segments to chatbot_read_user;

grant delete, insert, select, update on rag.text_segments to document_ingestion_write_user;

