# sipmarray

> Ricardo Peres, 2023

This pakacge provides a quick and easy way to get the goemetry of circular SiPM arrays. It was developed to know how many SiPM would be required to fully instrument a [DARWIN](https://darwin.physik.uzh.ch/)- or [XLZD](https://xlzd.org/)-size detector.

More SiPM unit options coming soon!

## Instalation
```bash
git clone git@github.com:ricmperes/sipmarray.git
cd sipmarray 
pip install .
```
For instal in editable source:
```bash
pip install -e .
```

## Usage

In a jupyter notebook simply `import sipmarray`. Take a look at the [docs](https://ricmperes.github.io/sipmarray/) and example notebook (really, the package is pretty simple and self-explanatory).

The package can be used from the terminal (from anywhere woop woop!) to quickly get a plot or coordinate geometry of a sipmarray or sipmunit. Check the `sipmarray/Do the following for more info: 
  * `sipmarray --help`
  * `sipmunit --help`
