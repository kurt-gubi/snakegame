BUILD_DIR = build

FILES = $(wildcard *.tex *.py)
BUILD_FILES = $(patsubst %,${BUILD_DIR}/%,${FILES})

LATEX=xelatex
LATEX_FLAGS=-shell-escape -interaction=nonstopmode

.PHONY: all

all: tutorial.pdf

${BUILD_DIR}:
	mkdir -p ${BUILD_DIR}

${BUILD_DIR}/%.tex: %.tex
	./jinja2 --latex < $< > $@

${BUILD_DIR}/%.py: %.py
	ln -sf ../$< $@

tutorial.pdf: ${BUILD_DIR}/tutorial.tex ${BUILD_FILES}
	cd "${BUILD_DIR}" && \
	${LATEX} ${LATEX_FLAGS} tutorial && \
	${LATEX} ${LATEX_FLAGS} tutorial && \
	${LATEX} ${LATEX_FLAGS} tutorial
	mv -f "${BUILD_DIR}/tutorial.pdf" tutorial.pdf
