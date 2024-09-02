-- DROP TABLE public.article_infos;

CREATE TABLE public.article_infos (
	article_uuid varchar(40) NOT NULL,
	article_title varchar(200) NULL,
	article_author varchar(200) NULL,
	article_publish_date varchar(200) NULL,
	article_pe_type varchar(200) NULL,
	article_link varchar(200) NULL,
	article_content text NULL,
	article_txt_path varchar(200) NULL,
	create_datetime timestamptz NULL,
	CONSTRAINT article_infos_pkey PRIMARY KEY (article_uuid),
	CONSTRAINT article_infos_pkey2 UNIQUE (article_title, article_author, article_publish_date, article_pe_type)
);