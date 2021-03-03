EMVCo QR Payment Plugin
==========================

This is a plugin for `pretix`_. 

Manual payment plugin with embded merchanted-presented `EMVCo QR Code <https://www.emvco.com/emv-technologies/qrcodes/>`_.
This plugin is fully compatible with most, if not all, Thai mobile banking apps.

Its configuration may be difficult to understand as it requires you to understand the EMVCo QR protocol,
but feel free to send questions if needed.

Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository, eg to ``local/pretix-emvcoqr``.

3. Activate the virtual environment you use for pretix development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.


License
-------


Copyright 2020-21 Panawat Wong-klaew

Released under the terms of the Apache License 2.0



.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
