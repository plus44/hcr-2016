# Human-Centred Robotics 2016

## Xavier Laguerta-Soler, Periklis Korkontzelos, Nathan Warner, Mihnea Rusu
## {xl5512, pk1913, njw13, mr3313}@ic.ac.uk

Our project is about building an interactive story-telling robot that reads (and turns the pages of) physical books to children :baby:. Our robot **PiNAOqio** uses the [NAO robot](https://www.ald.softbankrobotics.com/en/cool-robots/nao) from SoftBank Robotics to interact with the reader through speech and gestures. An additional hardware rig was designed and built to turn the pages of books and to accommodate a camera for capturing the open leaf. 

As this was first and foremost a research project, we set out to test the hypotheses proposed in our initial report, the [design report](docs/reports/design-report.pdf). Evaluation sessions were held, where participants were presented with 3 different instances of our system with varying degrees of capability and were read a short passage by each. In response, their task was to complete a brief questionnaire.

The full system is comprised of the following components: a laptop to interface with NAO, the robot and to perform optical character recognition (OCR) on the book picture; a Raspberry Pi to control the page-turning mechanism; an iPhone (6 or higher) to photograph the open book, and a server on the cloud to enable communication between the different platforms. As will be apparent to the reader, our system architecture ended up being quite different (and more complex) in the final report to what we initially envisioned in the design report, mainly due to complications with the OCR setup.

Ultimately the project was a success - the high-risk components namely the page-turning mechanism and OCR functioned to a high standard and the results of our research suggested the proposed hypotheses.

## Contents

This repository is composed of the following directories:
  - **[app](app)** iOS app source code and Carthage dependencies
  - **[docs](docs)** System startup documentation and reports written for this project (including the individual reports)
  - **[eval](eval)** Evaluation questionnaires handed out to the participants of our study and a Matlab script to determine the results of our experiment
  - **[scripts](scripts)** A number of useful, but maybe messier scripts for quick or intermediate testing
  - **[sdk](sdk)** The correct version of the NAOqi SDK that works with Python.
  - **[src](src)** Source code (in Python) for all individual elements of the system, along with a pip requirements file for setting up (a partially working) virtual environment. Each component is meant to have a copy of its respective subdirectory. The [phone](src/phone) component is only a networking-enabled dummy, as the real phone component is the iOS app.
  - **[photo](photo)** Test photographs of various book poses and lightings (for OCR) taken throughout the course of our project, along with a dedicated file, *[latest.jpeg](photo/latest.jpeg)*, that the laptop client updates while it's running, with fresh images received from the phone.

Link to the Python library used for [speech](https://pypi.python.org/pypi/SpeechRecognition/), which is not included in our virtual environment due to platform mish-mash :disappointed:.

Link to the [video](https://en.wikipedia.org/wiki/HTTP_404).
