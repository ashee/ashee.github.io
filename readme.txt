# Github pages Resume

## Generate PDF
The resume PDF is generated from the canonical `Amitava Shee.md` file with Pandoc and XeLaTeX:

```sh
bin/gen-pdf.sh
```

This writes `Amitava Shee Resume.pdf` in the repository root. Install the required tools on macOS with:

```sh
brew install pandoc
brew install --cask mactex-no-gui
```

The script also accepts optional source and output paths:

```sh
bin/gen-pdf.sh path/to/source.md path/to/output.pdf
```

## Website
This repo will automatically generate the site at https://ashee.github.io. 
A DNS CNAME entry has been setup in my AWS Route53 console to https://www.amitavashee.com
Please make sure to checkout GH pages settings at https://github.com/ashee/ashee.github.io/settings/pages

