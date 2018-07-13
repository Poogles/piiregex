# PiiRegex  [![Build Status](https://travis-ci.org/Poogles/piiregex.svg?branch=master)](https://travis-ci.org/Poogles/piiregex)

This wouldn't have been possible with [CommonRegex](https://github.com/madisonmay/CommonRegex).  Thanks!

Attempt to find PII in regex either using a specific PII type, or search through
everything available.

Pull requests welcome!

Install via pip.
```sh
pip install piiregex
```


Tests are available through pytest.

```sh
pip install -r dev_requirements.text
pytest -vv
```


Usage
------

```python    
>>> from piiregex import PiiRegex
>>> parsed_text = PiiRegex("""John, please get that article on www.linkedin.com to me by 5:00PM 
                               on Jan 9th 2012. 4:00 would be ideal, actually. If you have any 
                               questions, You can reach me at (519)-236-2723x341 or get in touch with
                               my associate at harold.smith@gmail.com""")
>>> parsed_text.times
['5:00PM', '4:00']
>>> parsed_text.dates
['Jan 9th 2012']
>>> parsed_text.phones
['(519)-236-2727']
>>> parsed_text.phones_with_exts
['(519)-236-2723x341']
>>> parsed_text.emails
['harold.smith@gmail.com']
```
    
Alternatively, you can generate a single PiiRegex instance and use it to parse multiple segments of text.

```python
>>> parser = PiiRegex()
>>> parser.times("When are you free?  Do you want to meet up for coffee at 4:00?")
['4:00']
```
    
Finally, all regular expressions used are publicly exposed. 

```python
>>> from piiregex import email
>>> import re
>>> text = "...get in touch with my associate at harold.smith@gmail.com"
>>> re.sub(email, "anon@example.com", text)
'...get in touch with my associate at anon@example.com'
```

```python
>>> from piiregex import time
>>> for m in time.finditer("Does 6:00 or 7:00 work better?"):
>>>     print(m.start(), m.group())
5 6:00 
13 7:00 
```

Most importantly (for our use case) any_match iterates through all regexes to
match anything.

```python
>>> from piiregex import PiiRegex
>>> parsed_text = PiiRegex("07123 123123") # should match a UK phone number. 
>>> parsed_text.any_match()
True
```

Please note that this module is currently English/US and UK specific.  Due to
the European nature of GDPR though this is being expanded.  PRs are welcome.


Supported Methods/Attributes
-----------------------------

  - `obj.dates`, `obj.dates()`
  - `obj.times`, `obj.times()`
  - `obj.phones`, `obj.phones()`
  - `obj.phones_with_exts`, `obj.phones_with_exts()`
  - `obj.links`, `obj.links()`
  - `obj.emails`, `obj.emails()`
  - `obj.ips`, `obj.ips()`
  - `obj.ipv6s`, `obj.ipv6s()`
  - `obj.prices`, `obj.prices()`
  - `obj.hex_colors`, `obj.hex_colors()`
  - `obj.credit_cards`, `obj.credit_cards()`
  - `obj.btc_addresses`, `obj.btc_addresses()`
  - `obj.street_addresses`, `obj.street_addresses()`
  - `obj.postcodes`, `obj.postcodes()`
  - `obj.ukphones`, `obj.ukphones()`
