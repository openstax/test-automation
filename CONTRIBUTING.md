# :+1::tada: Thanks for Contributing! :tada::+1:

See [openstax/CONTRIBUTING.md](https://github.com/openstax/napkin-notes/CONTRIBUTING.md) for more information on how to contribute to openstax!

# Selenium readability trumps efficiency

For example, instead of compacting strings to: `/'/a[text()="'+username+'"]'` use one of the following:

- `'//a[text()="' + username + '"]'`    (spacing for readability)
- `'//a[text()="%s"]' % username`    (formatted replacement)
- `'//a[text()="{0}"]'.format(username)`    (positional formating)
- `'//a[text()="{}"]'.format(username)`    (positional formating again)
- `'//a[text()="{search_string}"]'.format(search_string=username)`    (variable replacement)
