# Mike's Metropolis

[https://alephnaughtpix.github.io/mikes_metropolis/](https://alephnaughtpix.github.io/mikes_metropolis/)

## Faithful recreation of my first ever web site from the mid 1990s.

This is my first ever website, dating from round about the time I was at a student at Glasgow University, and slightly afterwards. The website was originally hosted on my own personal student account at Glasgow University Computing Services, and then migrated to **[Grelb](https://web.archive.org/web/19970120205629/http://grelb.src.gla.ac.uk:8000/)** (Glasgow Research and Educational Linux Box). 

The website dates from early March 1995 to December 1996, so it's got HTML and design elements to match! Actually, it was pretty good for the time, but if you look under the hood, you'll see loads of tables, font directives, center tags, the odd use of the blink tag, animated GIFs, and other things that would make a modern web designer cry. (In a nice way!) It's alsomostly hand coded in text editor, although I was already starting to use CGI-bin scripts for things like visitor counter, and by this time, I was staring to write Perl scripts to auto generate some listing pages.

I started this project after I discovered that my old website had been [archived more or less intact](https://web.archive.org/web/19970121022359/http://grelb.src.gla.ac.uk:8000/~mjames/default.html) by [The Wayback Machine](https://web.archive.org/), so I thought it would be a cool thing to bring it back to life, and to keep it as faithful as possible to the original. 

## How I did it

* Navigating through my old website using the Wayback Machine, I saved all the pages using the Chrome plugin **[Save Page WE](https://chromewebstore.google.com/detail/save-page-we/dhhpefjklgkmgeafimnjhojgjamoafof?pli=1)**. This saves the page as a single HTML file with images saved as a data URI.
* I then wrote a Python script to clean out the Wayback Machine code, fix the links for the local pages, and extract the images from the data URIs. You can see the script at `[scripts/source_parse.py](scripts/source_parse.py)`.
* The script does the vast majority of restoring the website, but I still had to go through each page and fix a few things by hand. 
* Finally, I added some Jekyll configuration so that the site could be hosted on GitHub Pages. There's not much to the configuration, as I just want to it copy the existing pages and assets to the right place, and I'm certainly not wanting Jekyll to generate the HTML, as that would defeat the purpose of the exercise! 


