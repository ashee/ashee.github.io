# Github pages Resume

## Generate profile artifacts
Profile facts live in `profile.md`. Generate the website Markdown, LinkedIn profile Markdown, static site, and resume PDF from that file with:

```sh
bin/gen-profile-artifacts.py
```

This writes the generated site, LinkedIn profile, default resume, and chronological resume under `pub/`. Install the required tools on macOS with:

```sh
brew install pandoc
brew install --cask mactex-no-gui
```

To generate only the chronological resume PDF, run:

```sh
bin/gen-pdf.sh
```

## Website
This repo will automatically generate the site at https://ashee.github.io. 
A DNS CNAME entry has been setup in my AWS Route53 console to https://www.amitavashee.com
Please make sure to checkout GH pages settings at https://github.com/ashee/ashee.github.io/settings/pages
