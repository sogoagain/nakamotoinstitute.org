"""Initial migration

Revision ID: c57f673dad76
Revises:
Create Date: 2024-01-13 00:41:00.675849

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c57f673dad76"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum(
        "ar",
        "de",
        "en",
        "es",
        "fa",
        "fi",
        "fr",
        "he",
        "it",
        "ko",
        "pt-br",
        "ru",
        "zh-cn",
        name="locales",
    ).create(op.get_bind())
    sa.Enum("pdf", "epub", "mobi", "txt", name="documentformats").create(op.get_bind())
    op.create_table(
        "blog_series",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("chapter_title", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_blog_series")),
    )
    op.create_table(
        "document_formats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "format_type",
            postgresql.ENUM(
                "pdf", "epub", "mobi", "txt", name="documentformats", create_type=False
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_formats")),
        sa.UniqueConstraint(
            "format_type", name=op.f("uq_document_formats_format_type")
        ),
    )
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("granularity", sa.String(), nullable=False),
        sa.Column("doctype", sa.String(), nullable=False),
        sa.Column("has_math", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_documents")),
    )
    op.create_table(
        "file_metadata",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("hash", sa.String(), nullable=False),
        sa.Column("last_modified", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_file_metadata")),
    )
    op.create_table(
        "blog_posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("added", sa.Date(), nullable=True),
        sa.Column("original_url", sa.String(), nullable=True),
        sa.Column("original_site", sa.String(), nullable=True),
        sa.Column("series_id", sa.Integer(), nullable=True),
        sa.Column("series_index", sa.Integer(), nullable=True),
        sa.Column("has_math", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["series_id"],
            ["blog_series.id"],
            name=op.f("fk_blog_posts_series_id_blog_series"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_blog_posts")),
        sa.UniqueConstraint(
            "series_id", "series_index", name=op.f("uq_blog_posts_series_id")
        ),
    )
    op.create_table(
        "json_files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_metadata_id", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_metadata_id"],
            ["file_metadata.id"],
            name=op.f("fk_json_files_file_metadata_id_file_metadata"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_json_files")),
    )
    op.create_table(
        "markdown_content",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_content", sa.Text(), nullable=False),
        sa.Column("html_content", sa.Text(), nullable=False),
        sa.Column("file_metadata_id", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_metadata_id"],
            ["file_metadata.id"],
            name=op.f("fk_markdown_content_file_metadata_id_file_metadata"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_markdown_content")),
    )
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("sort_name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["markdown_content.id"], name=op.f("fk_authors_id_markdown_content")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_authors")),
        sa.UniqueConstraint("slug", name=op.f("uq_authors_slug")),
    )
    op.create_table(
        "blog_post_translations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "locale",
            postgresql.ENUM(
                "ar",
                "de",
                "en",
                "es",
                "fa",
                "fi",
                "fr",
                "he",
                "ko",
                "it",
                "pt-br",
                "ru",
                "zh-cn",
                name="locales",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("excerpt", sa.Text(), nullable=False),
        sa.Column("image_alt", sa.String(), nullable=True),
        sa.Column("translation_url", sa.String(), nullable=True),
        sa.Column("translation_site", sa.String(), nullable=True),
        sa.Column("translation_site_url", sa.String(), nullable=True),
        sa.Column("blog_post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["blog_post_id"],
            ["blog_posts.id"],
            name=op.f("fk_blog_post_translations_blog_post_id_blog_posts"),
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["markdown_content.id"],
            name=op.f("fk_blog_post_translations_id_markdown_content"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_blog_post_translations")),
        sa.UniqueConstraint(
            "blog_post_id",
            "locale",
            name=op.f("uq_blog_post_translations_blog_post_id"),
        ),
    )
    op.create_table(
        "blog_series_translations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column(
            "locale",
            postgresql.ENUM(
                "ar",
                "de",
                "en",
                "es",
                "fa",
                "fi",
                "fr",
                "he",
                "it",
                "ko",
                "pt-br",
                "ru",
                "zh-cn",
                name="locales",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("blog_series_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["blog_series_id"],
            ["blog_series.id"],
            name=op.f("fk_blog_series_translations_blog_series_id_blog_series"),
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["markdown_content.id"],
            name=op.f("fk_blog_series_translations_id_markdown_content"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_blog_series_translations")),
        sa.UniqueConstraint(
            "blog_series_id",
            "locale",
            name=op.f("uq_blog_series_translations_blog_series_id"),
        ),
        sa.UniqueConstraint("slug", name=op.f("uq_blog_series_translations_slug")),
    )
    op.create_table(
        "document_translations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "locale",
            postgresql.ENUM(
                "ar",
                "de",
                "en",
                "es",
                "fa",
                "fi",
                "fr",
                "he",
                "ko",
                "it",
                "pt-br",
                "ru",
                "zh-cn",
                name="locales",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("sort_title", sa.String(), nullable=True),
        sa.Column("display_title", sa.String(), nullable=True),
        sa.Column("subtitle", sa.String(), nullable=True),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("external", sa.String(), nullable=True),
        sa.Column("image_alt", sa.String(), nullable=True),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["documents.id"],
            name=op.f("fk_document_translations_document_id_documents"),
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["markdown_content.id"],
            name=op.f("fk_document_translations_id_markdown_content"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_translations")),
        sa.UniqueConstraint(
            "document_id", "locale", name=op.f("uq_document_translations_document_id")
        ),
    )
    op.create_table(
        "email_threads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["json_files.id"],
            name=op.f("fk_email_threads_file_id_json_files"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_email_threads")),
    )
    op.create_table(
        "episodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("duration", sa.String(), nullable=False),
        sa.Column("summary", sa.String(), nullable=False),
        sa.Column("notes", sa.String(), nullable=False),
        sa.Column("youtube_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["markdown_content.id"],
            name=op.f("fk_episodes_id_markdown_content"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_episodes")),
        sa.UniqueConstraint("slug", name=op.f("uq_episodes_slug")),
    )
    op.create_table(
        "forum_threads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["json_files.id"],
            name=op.f("fk_forum_threads_file_id_json_files"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_forum_threads")),
    )
    op.create_table(
        "quote_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["json_files.id"],
            name=op.f("fk_quote_categories_file_id_json_files"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_quote_categories")),
        sa.UniqueConstraint("slug", name=op.f("uq_quote_categories_slug")),
    )
    op.create_table(
        "skeptics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("name_slug", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("article", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("excerpt", sa.Text(), nullable=True),
        sa.Column("link", sa.String(), nullable=False),
        sa.Column("media_embed", sa.Text(), nullable=True),
        sa.Column("twitter_screenshot", sa.Boolean(), nullable=False),
        sa.Column("wayback_link", sa.String(), nullable=True),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"], ["json_files.id"], name=op.f("fk_skeptics_file_id_json_files")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_skeptics")),
    )
    op.create_table(
        "translators",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("slug", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["markdown_content.id"],
            name=op.f("fk_translators_id_markdown_content"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_translators")),
        sa.UniqueConstraint("slug", name=op.f("uq_translators_slug")),
    )
    op.create_table(
        "blog_post_authors",
        sa.Column("blog_post_id", sa.Integer(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
            name=op.f("fk_blog_post_authors_author_id_authors"),
        ),
        sa.ForeignKeyConstraint(
            ["blog_post_id"],
            ["blog_posts.id"],
            name=op.f("fk_blog_post_authors_blog_post_id_blog_posts"),
        ),
    )
    op.create_table(
        "blog_post_translators",
        sa.Column("blog_post_translation_id", sa.Integer(), nullable=True),
        sa.Column("translator_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["blog_post_translation_id"],
            ["blog_post_translations.id"],
            name=op.f(
                "fk_blog_post_translators_blog_post_translation_id_blog_post_translations"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["translator_id"],
            ["translators.id"],
            name=op.f("fk_blog_post_translators_translator_id_translators"),
        ),
    )
    op.create_table(
        "document_authors",
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
            name=op.f("fk_document_authors_author_id_authors"),
        ),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["documents.id"],
            name=op.f("fk_document_authors_document_id_documents"),
        ),
    )
    op.create_table(
        "document_document_formats",
        sa.Column("document_format_id", sa.Integer(), nullable=True),
        sa.Column("document_translation_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["document_format_id"],
            ["document_formats.id"],
            name=op.f(
                "fk_document_document_formats_document_format_id_document_formats"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["document_translation_id"],
            ["document_translations.id"],
            name=op.f(
                "fk_document_document_formats_document_translation_id_document_translations"
            ),
        ),
    )
    op.create_table(
        "document_translators",
        sa.Column("document_translation_id", sa.Integer(), nullable=True),
        sa.Column("translator_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["document_translation_id"],
            ["document_translations.id"],
            name=op.f(
                "fk_document_translators_document_translation_id_document_translations"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["translator_id"],
            ["translators.id"],
            name=op.f("fk_document_translators_translator_id_translators"),
        ),
    )
    op.create_table(
        "emails",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("satoshi_id", sa.Integer(), nullable=True),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("sent_from", sa.String(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("thread_id", sa.Integer(), nullable=False),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"], ["json_files.id"], name=op.f("fk_emails_file_id_json_files")
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"], ["emails.id"], name=op.f("fk_emails_parent_id_emails")
        ),
        sa.ForeignKeyConstraint(
            ["thread_id"],
            ["email_threads.id"],
            name=op.f("fk_emails_thread_id_email_threads"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_emails")),
        sa.UniqueConstraint("satoshi_id", name=op.f("uq_emails_satoshi_id")),
    )
    op.create_table(
        "forum_posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("satoshi_id", sa.Integer(), nullable=True),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("poster_name", sa.String(), nullable=False),
        sa.Column("poster_url", sa.String(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("nested_level", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("thread_id", sa.Integer(), nullable=False),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["json_files.id"],
            name=op.f("fk_forum_posts_file_id_json_files"),
        ),
        sa.ForeignKeyConstraint(
            ["thread_id"],
            ["forum_threads.id"],
            name=op.f("fk_forum_posts_thread_id_forum_threads"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_forum_posts")),
        sa.UniqueConstraint("satoshi_id", name=op.f("uq_forum_posts_satoshi_id")),
    )
    op.create_table(
        "quotes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("whitepaper", sa.Boolean(), nullable=False),
        sa.Column("email_id", sa.Integer(), nullable=True),
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["email_id"], ["emails.satoshi_id"], name=op.f("fk_quotes_email_id_emails")
        ),
        sa.ForeignKeyConstraint(
            ["file_id"], ["json_files.id"], name=op.f("fk_quotes_file_id_json_files")
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["forum_posts.satoshi_id"],
            name=op.f("fk_quotes_post_id_forum_posts"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_quotes")),
    )
    op.create_table(
        "quote_quote_categories",
        sa.Column("quote_id", sa.Integer(), nullable=True),
        sa.Column("quote_category_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["quote_category_id"],
            ["quote_categories.id"],
            name=op.f("fk_quote_quote_categories_quote_category_id_quote_categories"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["quote_id"],
            ["quotes.id"],
            name=op.f("fk_quote_quote_categories_quote_id_quotes"),
            ondelete="CASCADE",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("quote_quote_categories")
    op.drop_table("quotes")
    op.drop_table("forum_posts")
    op.drop_table("emails")
    op.drop_table("document_translators")
    op.drop_table("document_document_formats")
    op.drop_table("document_authors")
    op.drop_table("blog_post_translators")
    op.drop_table("blog_post_authors")
    op.drop_table("translators")
    op.drop_table("skeptics")
    op.drop_table("quote_categories")
    op.drop_table("forum_threads")
    op.drop_table("episodes")
    op.drop_table("email_threads")
    op.drop_table("document_translations")
    op.drop_table("blog_series_translations")
    op.drop_table("blog_post_translations")
    op.drop_table("authors")
    op.drop_table("markdown_content")
    op.drop_table("json_files")
    op.drop_table("blog_posts")
    op.drop_table("file_metadata")
    op.drop_table("documents")
    op.drop_table("document_formats")
    op.drop_table("blog_series")
    sa.Enum("pdf", "epub", "mobi", "txt", name="documentformats").drop(op.get_bind())
    sa.Enum(
        "ar",
        "de",
        "en",
        "es",
        "fa",
        "fi",
        "fr",
        "he",
        "ko",
        "it",
        "pt-br",
        "ru",
        "zh-cn",
        name="locales",
    ).drop(op.get_bind())
    # ### end Alembic commands ###
