# Finding the Top Literary Agents from 2016, 2017, and 2018

The publishing industry can be difficult to navigate. This project is an attempt to find the most prominent literary agents using some simple scraping and relationship mapping.

## Methodology

The methodology is fairly simple and uses some bash commands to extract data.

### Best Fiction Lists

A Google search for "best fiction 2017" yields a decent number of URLs to bestseller lists. The content from these pages can be downloaded for parsing:

```
mkdir best-fiction-2017.data
cat best-fiction-2017.urls.txt | xargs -P8 -I {} sh -c 'curl {} > best-fiction-2017.data/$(echo {} | md5sum | cut -d\ -f1) || true'
```

The downloaded content can then be parsed by looking for the string "by Some Author". This yields a number of spurious entries, but because we're mapping it to agent listings later on, it won't matter.

```
cat best-fiction-2017.data/* | grep -o 'by [A-Z][A-Za-z]\+ [A-Z][A-Za-z]\+' | cut -d\ -f2- | sort -u > best-authors-2017.txt
```

### Literary Agents List

The site, pw.org, has a good list of literary agents [specializing in literary fiction](https://www.pw.org/literary_agents?filter0=9677&field_electronic_submissions_value=All&items_per_page=All). This list can be scraped with the following commands:

```
curl 'https://www.pw.org/literary_agents?filter0=9677&field_electronic_submissions_value=All&items_per_page=All' > literary-agents-pw-org.html
xmllint --html --xpath "//li[contains(@class, 'views-row')]" literary-agents-pw-org.html | xmllint --html --xpath '//text()' - | cut -d\: -f2 | sed 's/^[\ ]\+//g' > literary-agents-pw-org.txt
```
