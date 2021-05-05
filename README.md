# Impfbot

Impfbot is a Python scripts which checks periodically for available vaccination appointments against the SARS-CoV-2 / COVID-19 coronavirus on [impfterminservice.de](https://impfterminservice.de) which is used in most German federal states.

![Impfbot in action](impfbot.gif)

## Requirements

- Python 3
- Google Chrome

## Setup

```sh
pip install .
```

## Usage

1. First copy and rename the `resources/config.ini.example` to `resources/config.ini`.
2. Then add your post codes and transfer codes (if available) to the config file. If you don't have transfer codes, just enter `x` or some invalid code.
3. Then start the Python script:

```sh
python impfbot
```

## Credits

- [Alarm sound](https://freesound.org/people/guitarguy1985/sounds/54048/) by guitarguy1985
