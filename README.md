# Finding the Top Literary Agents from 2016, 2017, and 2018

The publishing industry can be difficult to navigate. This project is an attempt to find the most prominent literary agents using some simple scraping and relationship mapping.

## Methodology

The methodology is fairly simple and uses some shell commands to extract data.

### Best Fiction Lists

A Google search for "best fiction 2017" yields a decent number of URLs to bestseller lists. The content from these pages can be downloaded for parsing:

```
mkdir best-fiction-2017.data
cat best-fiction-2017.urls.txt | xargs -P8 -I {} sh -c 'curl {} > best-fiction-2017.data/$(echo {} | md5sum | cut -d\  -f1) || true'
```

The downloaded content can then be parsed by looking for "by Some Author" strings. This yields a number of spurious entries, but because we're mapping it to agent listings later on, it won't matter.

```
cat best-fiction-2017.data/* | grep -o 'by [A-Z][A-Za-z]\+ [A-Z][A-Za-z]\+' | cut -d\  -f2- | sort -u > best-authors-2017.txt
```

### Literary Agents List

The site, pw.org, has a good list of literary agents [specializing in literary fiction](https://www.pw.org/literary_agents?filter0=9677&field_electronic_submissions_value=All&items_per_page=All). I had to resort to writing Python code to clean and restructure the content. This list can be acquired with the following commands:

```
curl 'https://www.pw.org/literary_agents?filter0=9677&field_electronic_submissions_value=All&items_per_page=All' > literary-agents-pw-org.html
xmllint --html --xpath "//li[contains(@class, 'views-row')]" literary-agents-pw-org.html | xmllint --html --xpath '//text()' - | cut -d\: -f2 | sed 's/^[\ ]\+//g' > literary-agents-pw-org.txt
python literary_agent_parsing.py --input-file literary-agents-pw-org.txt | sort -u > literary-agents.txt
```

The final artifact is the `literary-agents.txt` file, which is a CSV file containing `author,agent,agency`. Again there are some spurious entries given HTML special characters, etc. You'll need to remove any entries starting with a `,`, i.e. agents with no represented authors.

### Joining Authors, Agents, and Agencies

Now that we have the `best-authors-2017.txt` and `literary-agents.txt` file, we can perform a simple `join` command to get the list of agents and agencies associated with the bestsellers of 2017:

```
join -t ',' best-authors-2017.txt literary-agents.txt
```

This yields the small list below:

Author | Agent | Agency
--- | --- | ---
Annie Proulx|Liz Darhansoff|Darhansoff Verrill Feldman Literary Agents
Celeste Ng|Julie Barer|The Book Group
Claire Messud|Georges Borchardt|Georges Borchardt
Colson Whitehead|Nicole Aragi|Aragi Inc.
Dan Chaon|Ren&Atilde;&copy;e Zuckerbrot|Massie & McQuilkin
Dexter Palmer|Susan Golomb|Writers House
Diksha Basu|Adam Eaglin|Cheney Associates LLC
Elizabeth Strout|Molly Friedrich|The Friedrich Agency LLC
Emma Cline|Bill Clegg|The Clegg Agency
Erik Larson|Gary Morris|David Black Agency
Gabrielle Zevin|Douglas Stewart|Sterling Lord Literistic Inc.
Jhumpa Lahiri|Eric Simonoff|William Morris Endeavor
Joshua Ferris|Julie Barer|The Book Group
Julie Buntin|Sarah Bowlin|Aevitas Creative Management
Lauren Groff|Bill Clegg|The Clegg Agency
Lidia Yuknavitch|Rayhan&Atilde;&copy; Sanders|Massie & McQuilkin
Maria Semple|Anna Stein|ICM Partners
Michael Chabon|Dan Kirschen|ICM Partners
Michael Chabon|Mary Evans|Mary Evans Agency
Neal Stephenson|Liz Darhansoff|Darhansoff Verrill Feldman Literary Agents
Ottessa Moshfegh|Bill Clegg|The Clegg Agency
Paul Auster|Carol Mann|Carol Mann Agency
Paul Yoon|Mitchell Waters|Curtis Brown Ltd.
Rachel Khong|Sarah Bowlin|Aevitas Creative Management
Samantha Hunt|PJ Mark|Janklow & Nesbit Associates
Sarah Perry|Susan Golomb|Writers House
Sophie Kinsella|Kimberly Witherspoon|Inkwell Management
Stephen King|Liz Darhansoff|Darhansoff Verrill Feldman Literary Agents
Thomas Mullen|Susan Golomb|Writers House
Weike Wang|Joy Harris|The Joy Harris Literary Agency Inc.
