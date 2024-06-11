### data guidelines

This example works only with two files:
- influencers.txt
- campaigns.txt

The name is important because of the filter used to search inside the DB:
{
  "search": "*",
  "select": "id,content,metadata,title,source,chunk",
  "filter": "title eq '/documents/campaigns.txt'"
}

Please check the prompts to see how they were generated.
