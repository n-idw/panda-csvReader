# PANDA CSV-Reader

A python library originally designed for the [TrackML particle tracking challenge](https://sites.google.com/site/trackmlparticle/home). It is currently being used to read the hit and truth information of the [straw tube tracker (STT)](https://panda.gsi.de/article/straw-tube-tracker) extracted as CSV files from the [PandaRoot](https://fairroot.gsi.de/index.html%3Fq=node%252F7.html) simulation pipeline. The information of in the CSV files is then returned as [pandas](https://pandas.pydata.org/) data frames.

## Installation

First download the repository with git:

```bash
git clone https://github.com/n-idw/panda-csvReader.git
```

Then, the package can be installed as a user package:

```bash
pip install --user panda-csvReader
```

To make a local checkout of the repository available directly it can also be
installed in development mode:

```bash
pip install --user --editable panda-csvReader
```

In both cases, the package can be imported via `import trackml` without
additional configuration. In the later case, changes made to the code are
immediately visible without having to reinstall the package.

## Preparation

The simplest way to use this library is to write all relevant information of an event into four CSV files, systematically called

- `eventXXXXXXXXXX-hits.csv`
- `eventXXXXXXXXXX-cells.csv`
- `eventXXXXXXXXXX-truth.csv`
- `eventXXXXXXXXXX-particles.csv`

The Xs are placeholder for the event number meaning that the *hits* CSV file for the event with the event number 123 would be called `event0000000123-hits.csv`. In the following the information saved in the columns of each CSV file is listed and described.

### Hits

- `hit_id` : Identification number of a hit in the STT.
- `x,y,z` : Coordinates of the hit position in cm.
- `volume_id` : Identification number of the detector volume (currently always 9 for the STT).
- `layer_id` : Identification number of the straw tube layer.
- `module_id` : Identification number of the straw tube.

### Cells

- `hit_id` : Identification number of a hit in the STT.
- `depcharge` : Number of electrons deposited by a hit in a straw tube.
- `energyloss` : Approximatation of the measured energy loss in a straw tube calculated by dividing `depcharge` by $10^{6}$
- `volume_id` : Identification number of the detector volume (currently always 9 for the STT).
- `layer_id` : Identification number of the straw tube layer.
- `module_id` : Identification number of the straw tube.
- `sector_id` : Identification number of the STT sector.
- `isochrone` : Radius of the isochrone in cm.
- `skewed` : Indication of the polarity of a straw tube (0 = straight, 1 = +3°, -1 = -3°)

### Truth

- `hit_id` : Identification number of a hit in the STT.
- `tx,ty,tz,tT` : True coordinates of the interaction point in cm and time in ns corresponding to a hit in the STT.
- `tpx,tpy,tpz` : True momentum vector in GeV/c of the particle at the hit position.
- `weight` : Weighting of the hit.
- `particle_id` : Particle identification number of the particle responsible for the hit. This particle ID is used to get information about the particle from the *particles* CSV file.

### Particles

- `particle_id` : Same particle identification number as in the *truth* CSV file.
- `vx,vy,vz` : Coordinates of the point of origin / vertex of the particle in cm.
- `px,py,pz` : Initial momentum vector of the particle in GeV/c.
- `q` : Currently not used.
- `nhits` : Number of hits in all PANDA detector systems resulting from this particle.
- `pdgcode` : Monte-Carlo particle identification number according to the [PDG](https://pdg.lbl.gov/2024/mcdata/mass_width_2024.txt)
- `start_time` : Time of production of the particle in ns.
- `primary` : Indication if the particle comes from the simulated decay chain (1) or originates for, e.g., detector interaction (0).

The *truth* and *particles* CSV files can only be created with the information provided in a Monte-Carlo simulation sample and consequently not exist for experimental data.

Additional columns as well as completely new CSV file types, following the template `eventXXXXXXXXXX-{myType}.csv`, can be easily read by the utilities provided in this library.

## Usage

To read the data for one event from a MC sample simply use:

```python
from trackml.dataset import load_event

hits, cells, particles, truth = load_event('path/to/event000000123')
```

For experimental data where only the hit information is available use:

```python
from trackml.dataset import load_event

hits, cells = load_event('path/to/event000000456', parts=['hits', 'cells'])
```

To iterate over events in a dataset:

```python
from trackml.dataset import load_dataset

for event_id, hits, cells, particles, truth in load_dataset('path/to/dataset'):
    ...
```

To read a single event and compute additional columns derived from the
stored data:

```python
from trackml.dataset import load_event
from trackml.utils import add_position_quantities, add_momentum_quantities, decode_particle_id

# get the particles data
particles = load_event('path/to/event000000123', parts=['particles'])

# decode particle id into vertex id, generation, etc.
particles = decode_particle_id(particles)

# add vertex rho, phi, r
particles = add_position_quantities(particles, prefix='v')

# add momentum eta, p, pt
particles = add_momentum_quantities(particles)
```

The dataset path can be the path to a directory or to a zip file containing the
events `.csv` files. Each event is lazily loaded during the iteration. Options
are available to read only a subset of available events or only read selected
parts, e.g. only hits or only particles.

To generate a random test submission from truth information and compute the
expected score:

```python
from trackml.randomize import shuffle_hits
from trackml.score import score_event

shuffled = shuffle_hits(truth, 0.05) # 5% probability to reassign a hit
score = score_event(truth, shuffled)
```

All methods either take or return `pandas.DataFrame` objects. You can have a
look at the function docstrings for detailed information.

## Authors

The library was originally written by

*   Moritz Kiehn

with contributions from

*   Sabrina Amrouche
*   David Rousseau
*   Ilija Vukotic
*   Nimar Arora
*   Jon Nordby
*   Yerkebulan Berdibekov
*   Victor Estrade

and was forked by

* Nikolai in der Wiesche