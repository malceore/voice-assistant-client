# Whisper Voice Assistant Client

This project holds the code and automation scripts for the client of my always listening voice assistant. It leverages Snowboyhot word for the wakeword and Whipser server for complex language transcription. Additionally it can be managed using Mozilla Webthing's Gateway portal which is a locally hosted smart home service and integrate's with it's features. The goal of this project is to give an alternative to closed source, cloud based voice asssitant spyware that allows for the customization of hotwords to be whatever you want. 

![Webthings_Sample](/Screenshot_2020-10-19_07:58:00.png)

## Getting Started

Disclaimer: This project is still in ongoing beta, support is highly limited.

## Installing

Please clone the latest source onto your Linux-based OS, I've tested this on most Raspberry Pi instances aswell as a Lubuntu Laptop. In the scripts directory you will see a 'reinstall' script, review and execute this script to install prereqs. This repository is simply the 'client' software, you will also need to install Whipser Server and Pocketpshinx on a heavier server or VPS which has it's installation described in the below repository.
https://github.com/malceore/whisper

After you've completed the install you will need to update the IP internally to point at your local whisper server. The service will open a new connection everytime the hotword is triggered in order to do Speech-to-text transcription. After that you can execute the run.sh script, this starts both the always listening service as well as the webthings service. Currently the hotword is 'Bijou', the name of my assistant, but my hotwords directory has some more precreated hotwords for you t try. If you are using Mozilla Gateway you can now add the assistant as another smart thing and I have provided an Icon that I use in the root of the repository.
 

## I want to contribute

Yeah feel free to create PRs for things and I'll review them when I can. But since the best automation is the kind you write for yourself it may just be more valuable too create your models and your own skills.
