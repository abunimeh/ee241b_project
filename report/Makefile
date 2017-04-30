PAPER = main
TEX = $(wildcard *.tex)
BIB = ref.bib

all: $(PAPER).pdf


$(PAPER).pdf: $(TEX) $(BIB) $(EPS) $(DATA)
	pdflatex $(PAPER)
	bibtex $(PAPER)
	pdflatex $(PAPER)
	pdflatex $(PAPER)

%.pdf: %.eps
	epstopdf $<

clean:
	rm -f *.aux *.bbl *.blg *.log *.out $(PAPER).pdf

.PHONY: all clean
