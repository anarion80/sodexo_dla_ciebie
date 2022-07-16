# Sodexo Dla Ciebie Card Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

Sodexo Dla Ciebie - Custom Component for Home Assistant

The data source for this integration is [Sodexo Dla Ciebie](https://dlaciebie.sodexo.pl/) - Polish instance od Sodexo, provider of employee benefit cards.

The author of this project categorically rejects any and all responsibility for the card balance and other data that were presented by the integration.

# Installation
## HACS (Recommended)
This is an official HACS integration and can be added via HACS.

Assuming you have already installed and configured HACS, follow these steps:

1. Navigate to the HACS integrations page
2. Choose Integrations under HACS
3. Click the '+' button on the bottom of the page
4. Serch for "Sodexo Dla Ciebie", choose it, and click install in HACS
5. Ready! Now continue with the configuration.

## Manual
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `sodexo_dla_ciebie`.
4. Download _all_ the files from the `custom_components/sodexo_dla_ciebie/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant

# Configuration

## Through the interface
1. Navigate to `Settings > Devices & Services` and then click `Add Integration`
2. Search for `Sodexo Dla Ciebie`
3. Enter your credentials (e-mail and password)
4. Select if you want to import all cards, or only active ones
5. Repeat the procedure as many times as desired to include cards from other accounts

## Details

The integration pulls the current cards balance and presents as entity state. In addition, a few additional card details are pulled as entity attributes.

This is an example of a few cards added:
![example][exampleimg]

# Legal notice
This is a personal project and isn't in any way affiliated with, sponsored or endorsed by [Sodexo Poland](https://www.sodexo.pl/).

All product names, trademarks and registered trademarks in (the images in) this repository, are property of their respective owners. All images in this repository are used by the project for identification purposes only.

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[sodexo_dla_ciebie]: https://github.com/anarion80/sodexo_dla_ciebie
[buymecoffee]: https://www.buymeacoffee.com/anarion
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/blueprint.svg?style=for-the-badge
[commits]: https://github.com/anarion80/sodexo_dla_ciebie/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: sodexo.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-anarion80-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/v/release/anarion80/sodexo_dla_ciebie?style=for-the-badge
[releases]: https://github.com/anarion80/sodexo_dla_ciebie/releases
