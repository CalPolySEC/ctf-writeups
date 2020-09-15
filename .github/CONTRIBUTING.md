## Introduction
Welcome to Cal Poly's White Hat Club's CTF Write-Up Repository! If you're reading this, it probably means you solved a challenge, and you are writing a write so others can learn. So, first off, congradulations, you earned it!

## Rules
1. Only write write-ups challenges you solved or that someone on the team has asked you to write (i.e. do not get your solution wholly off the internet, and then write a write-up).
2. Write your documents using markdown.
    * If you are unfamiliar with markdown [this is a good cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Here-Cheatsheet).
3. Follow the pull request template when attempting to make a pull request.
4. Follow the formatting subrules.
    ### Formatting
    1. The folder containing the write-ups should be named after the CTF and the year.
        * For example, the folder containing write-ups for PicoCTF 2018 should be: ````picoCTF18````
        * Folder names must use __camel case__.
    2. The name of all write-up files must use __camel case__.
        * The ````README.md```` file for the folder is an exception to this rule.
        * Any pull requests on the ````LICENSE```` file or any files in the ````.github```` folder are an exception to this rule.
    3. All associated, non-markdown files should be placed in a subfolder named ````assets````
        * Asset file names should be prefixed with the challenge name.
        * Asset files __do not__ have to use camel case if following another naming convention such as snake case for Python files.
    4. The folder containing the write-ups must contain a README.md
        * This file must contain:
            * The __full CTF name__,
            * The year,
            * And a bulleted list of formatted links to all write-up markdown files.
                * This list should be sorted by category then by point value then by alphabetical order
                * The links should be named `challenge name - point value`

An example file structure for picoCTF19:
```
writeups
└── picoCTF19
     ├── assets
     │    └── handyShellcodeCallGraph.png
     ├── handyShellCode.md
     └── README.md
```
