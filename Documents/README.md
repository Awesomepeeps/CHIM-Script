# Documents and Presentations

## Requirments
In order to properly compile the .tex gile into a readable PDF document, texlive must be installed. For the .odp and .odt LiberOffice must be installed

```shell
sudo apt install texlive-latex-recommended texlive-latex-extra
```
```shell
sudo apt install libreoffice
```

## Compiling Presentation

Run the following command to compile the presentation:

```shell
pdflatex chim-xpt_presentation.tex
```
Make sure that all files that are in the Images folder are in the same locations at the .tex file when compiling otherwise it will not compile

## Opening Document and Side Project

Download the Side_Project_Electronics.odp and Enhancing_CHIM-XPT_Paper.odt and open them in LibreOffice
