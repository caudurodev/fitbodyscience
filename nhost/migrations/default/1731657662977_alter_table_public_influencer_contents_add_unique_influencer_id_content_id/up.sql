alter table "public"."influencer_contents" add constraint "influencer_contents_influencer_id_content_id_key" unique ("influencer_id", "content_id");
