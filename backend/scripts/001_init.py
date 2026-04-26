"""Migration initiale - création de toutes les tables

Revision ID: 001_init
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "wilayas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nom", sa.String(100), nullable=False),
        sa.Column("code", sa.String(2), nullable=False),
        sa.Column("region", sa.String(50)),
    )

    op.create_table(
        "filieres",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nom", sa.String(150), nullable=False),
        sa.Column("domaine", sa.String(80), nullable=False),
        sa.Column("duree_annees", sa.SmallInteger(), nullable=False),
        sa.Column("moyenne_min", sa.Numeric(4, 2), nullable=False),
        sa.Column("series_compatibles", postgresql.ARRAY(sa.Text()), server_default="{}"),
        sa.Column("interets_associes", postgresql.ARRAY(sa.Text()), server_default="{}"),
        sa.Column("debouches", sa.Text()),
        sa.Column("taux_emploi", sa.SmallInteger()),
        sa.Column("description", sa.Text()),
    )

    op.create_table(
        "utilisateurs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nom", sa.String(100), nullable=False),
        sa.Column("prenom", sa.String(100), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("num_dossier_bac", sa.String(20), unique=True),
        sa.Column("wilaya_id", sa.Integer(), sa.ForeignKey("wilayas.id")),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
    )
    op.create_index("ix_utilisateurs_email", "utilisateurs", ["email"])

    op.create_table(
        "profils_bac",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("utilisateur_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("utilisateurs.id"), unique=True),
        sa.Column("serie", sa.String(50), nullable=False),
        sa.Column("moyenne", sa.Numeric(4, 2), nullable=False),
        sa.Column("annee_bac", sa.SmallInteger()),
        sa.Column("interets", postgresql.ARRAY(sa.Text()), server_default="{}"),
    )

    op.create_table(
        "universites",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nom", sa.String(200), nullable=False),
        sa.Column("wilaya_id", sa.Integer(), sa.ForeignKey("wilayas.id")),
        sa.Column("type", sa.String(20)),
        sa.Column("site_web", sa.String(255)),
        sa.Column("latitude", sa.Numeric(9, 6)),
        sa.Column("longitude", sa.Numeric(9, 6)),
    )

    op.create_table(
        "offres",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("universite_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("universites.id")),
        sa.Column("filiere_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("filieres.id")),
        sa.Column("capacite", sa.Integer()),
        sa.Column("annee", sa.SmallInteger(), nullable=False),
        sa.Column("moyenne_derniere", sa.Numeric(4, 2)),
    )

    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("utilisateur_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("utilisateurs.id")),
        sa.Column("offre_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("offres.id")),
        sa.Column("score", sa.Numeric(5, 2)),
        sa.Column("rang", sa.SmallInteger()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "temoignages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("utilisateur_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("utilisateurs.id")),
        sa.Column("filiere_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("filieres.id")),
        sa.Column("contenu", sa.Text(), nullable=False),
        sa.Column("note", sa.SmallInteger()),
        sa.Column("approuve", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )


def downgrade():
    op.drop_table("temoignages")
    op.drop_table("recommendations")
    op.drop_table("offres")
    op.drop_table("universites")
    op.drop_table("profils_bac")
    op.drop_table("utilisateurs")
    op.drop_table("filieres")
    op.drop_table("wilayas")
