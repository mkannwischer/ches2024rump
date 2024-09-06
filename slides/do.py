#!/usr/bin/env python3
import json
import os

s1 = [
    #("Rump Session Opening", "Matthias Kannwischer, Shivam Bhasin"),
    ("Program Chairs' Report", "Bo-Yin Yang, Francisco Rodriguez"),
    ("General Announcement", "Benedikt Gierlichs"),
    ("Artifact Chair Report \\& Awards", "Markku-Juhani O. Saarinen"),
    ("CHES Challenge (WhibOx) - Technical Wrap-up and Award", "Aleksei Udovenko")
]

b1 = [("Break", "BREAK\\\\ Come back at 21:10")]
s2 = [
    ("Real Rump Session Opening", "Matthias Kannwischer, Shivam Bhasin"),
    ("Don't hack hardware", "Jasper van Woudenberg"),
    ("tiny simon", "Patrick Schaumont"),
    ("We $<$3 LEDs", "Marno van der Maas"),
    ("OpenTitan After All (this time)", "Dom Rizzo"),
    ("Side Channel Attacks: Artificial Intelligence Vs Human Intelligence", "Morgane Guerreau"),
    ("Wanted AGAIN: Postdoc(s) and your vote(s)", "Bo-Yin Yang")
]
b2 = [("Break", "BREAK\\\\ Come back at 22:00")]

s3 = [
    ("New Records in Hardware S-Box Gate Count", "Colin O'Flynn"),
    ("Optimist OSE: The Fellowship of the Code", "Dev Manish Mehta, Evan Apinis, Trey Marcantonio"),
    ("Ask your doctor about sec-certs", "Jan Jancar"),
    ("A Game of Visas", "Diego F. Aranha"),
    ("On Non Constant-time Nonces", "Thomas Eisenbarth"),
    ("Hey it's 1999 again", "Markku-Juhani Saarinen, Nicky Mouha"),
    ("PQCrypto 2025", "Ruben Niederhagen"),
    ("EUCLEAK : Story of a Side-Channel Vulnerability", "Victor Lomné"),
    ("Future-proof cryptography", "Antoon Purnal"),
    ("1st Edition of the CASCADE Conference", "Pascal Sasdrich"),
    ("The PhD Student", "Georg Land"),
    #("Rump Session Closing & Awards", "Matthias Kannwischer, Shivam Bhasin")
]


talks = s1 + b1 + s2 + b2 + s3

def make_break_slide(msg):
    print("\\begin{frame}")
    print("\centering\Huge "+msg)
    print("\end{frame}")
#Slides that list the next speaker's name, their title, and the name of the following speaker, so they can get ready to come up
def make_interstitial_slide(title, curr_author_names, next_author_names):
    print("\\begin{frame}")
    print("\centering\Huge "+title+"\\\\")
    print("\\begin{center}")
    print("\Large "+curr_author_names+"\\\\")
    if next_author_names is not None:
        print("\large Next up: "+next_author_names+"\\\\")
    print("\end{center}")
    print("\end{frame}")

def make_includepdf(fname):
    print("\includepdf[pages=-]{"+fname+"}")

#The prefix of the talk PDF name, downloaded from HotCRP
PREAMBLE_FILE = "preamble.txt"


#Assemble the LaTeX file, with \includepdf statements for
#the PDF slides of each PID in the (reformatted) pid_order_from_csv string
def make_rump_session():
    with open(PREAMBLE_FILE, "r+") as preamble_file:
        latex_preamble = preamble_file.read()

    print(latex_preamble)

    talkNumber = 1
    for i in range(len(talks)):
        talk = talks[i]
        # print(talk)
        title, author = talk
        # print(author)
        if i < len(talks)-1:
            # print(talks[i+1])
            nexttitle, nextauthor = talks[i+1]
            if nexttitle == "Break":
                nextauthor = None
        else:
            nextauthor = None
        # print(nextauthor)
        if title == "Break":
            make_break_slide(author)
        else:
            make_interstitial_slide(title, author, nextauthor)
            talkFile = f"{talkNumber}.pdf"
            make_includepdf(talkFile)
            talkNumber += 1

    print("\\begin{frame}")
    print("\centering\Huge THE END!!!\\\\ Thank you to all the speakers!")
    print("\end{frame}")
    print("\end{document}")
    


if __name__=='__main__':
    make_rump_session()

    exit(0)
