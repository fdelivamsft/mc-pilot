### data guidelines

This example works only with two files:
- influencers.json
- campaigns.json

The category is important because of the filter used to search inside the DB:
{
  "search": "*",
  "select": "id,content,metadata,title,source,chunk",
  "filter": "category eq 0" ## 0 filter all the campaign, while 1 filters all the influencers
}

Please check the prompts to see how they were generated.
