# MC_PILOT
Please read original README_original.MD

This repo is based on a chat with your data accelerator: [Azure-Samples/chat-with-your-data-solution-accelerator](https://github.com/Azure-Samples/chat-with-your-data-solution-accelerator)

The content of this repo's fork is for demonstration purpose of the capabilities of Azure OpenAI, Azure AI Search, Document AI and many other AI tools in supporting advertisment use cases. The code provided should not be used in production and it is not supported or mantained.

# TESTING

### Try online
Admin: https://web-7nfnsupjf3azk-admin.azurewebsites.net/
Website: https://web-7nfnsupjf3azk.azurewebsites.net/

### Load data
Please upload the files campaigns.txt and influencers.txt in the admin website.

### Questions:

1. Hi! What can you do for me?
2. Commonwealth bank asked us to create a campaign for the new digital banking app in Singapore. The campaign should be creative and focused to young adults.
3. can you help me find the most similar campaigns done in the past?
4. can you suggest me if the instagrammer @glamMaddox can be a good influencer for the Commonwealth bank campaign?

### Screenshot
![Testing screenshot](/docs/images/screenshot1.png)

![Testing screenshot 2](/docs/images/screenshot2.png)


# Development

Please follow instruction in docs/LOCAL_DEVELOPMENT.md

### Upload new version:
cd code
azd deploy web

### Run locally:
1. launch frontend web:
cd code/frontend
npm install --global typescript
npm install --global vite

npm uninstall tsc
npm install -D typescript

npm run build
tsc && vite --host
http://localhost:5173/

2. launch Fronted API via debugging
or
cd code
poetry run flask run
