CREATE TABLE "public"."influencers" ("id" uuid NOT NULL DEFAULT gen_random_uuid(), "name" text NOT NULL, "yt_url" text, "profile_img" uuid, "yt_description" text NOT NULL, "yt_channelinfo_jsonb" jsonb NOT NULL, "yt_last_updated" date NOT NULL, PRIMARY KEY ("id") );
CREATE EXTENSION IF NOT EXISTS pgcrypto;
