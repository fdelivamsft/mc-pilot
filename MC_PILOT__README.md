# TESTING

### Try online
Admin: https://web-7nfnsupjf3azk-admin.azurewebsites.net/
Website: https://web-7nfnsupjf3azk.azurewebsites.net/

### Load data
Please upload the files campaigns.txt and influencers.txt in the admin website.

### Questions:

1. Commonwealth bank asked us to create a campaign for the new digital banking app in Singapore
2. Can you help me sarch for similar campaigns?

### Screenshot
![Testing screenshot](/docs/images/screenshot1.png)

![Testing screenshot 2](/docs/images/screenshot2.png)


# Development
### Upload new version:
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
