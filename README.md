# Meg

## What is it

Meg is a rest helper, which helps to take a rest while working

It’s named in honour of [Meg White](http://en.wikipedia.org/wiki/Meg_White).

This app is very simple, it has no settings or parameters. I was really 
inspired by simple app named [Tomate](https://gitorious.org/tomate) and 
tried to follow its simplicity.

Meg is open source software, it’s distributed under the terms of BSD License.

## How to get it

Just clone repository and run app as `python2 src/meg.py`. Of course, 
you should have installed Python 2 and PyGTK (`python2` and `pygtk` packages 
for Arch Linux).

I’m not really interested in porting Meg to Windows, Mac OS X or whatever, sorry.

## How to use it

Using is very simple. When you run Meg, you should see lollipop icon in your 
tray (Tint, GNOME panel, etc.). If it is red, Meg is working, black — idle.

Clicking on icon is changing state of Meg. If it is working, you will 
receive sometimes small window about having rest.

There are two types of rest breaks: small (reminds you every 15 minutes, 
length of break is 30 seconds) and long (reminds you every 1 hour, 
length — 5 minutes). If you want to know when would be break, just point 
cursor on Meg icon.

Rest window has timer of break and “Skip” button. If you press it (or close 
the window) you’re going to meet Robot Devil! I’m joking, Meg just would 
think that you successfully had this rest (but your conscience would be guilty).
