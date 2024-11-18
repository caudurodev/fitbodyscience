alter table "public"."content" alter column "html_jsonb" drop not null;
alter table "public"."content" add column "html_jsonb" text;
