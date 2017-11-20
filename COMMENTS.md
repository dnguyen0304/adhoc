# adhoc_slcsp
Solution to the Ad Hoc "slcsp" problem.

## Getting Started
### Requirements
- build-essential
- Python 3.6.x

### Building
1. Unzip the package.
```
unzip adhoc_slcsp
```
2. Change the working directory.
```
cd adhoc_slcsp
```
3. Build the package.
```
python ./setup.py install
```

### Testing
1. Run the test suite.
```
python ./setup.py test
```

### Running
5. Run the application.
```
python ./main.py
```

## Design
```
Reader -> Pipeline 1 -> Pipeline 2 -> ... Pipeline n -> Writer
```
The source data is read into memory by `io.Reader`s and passes through n
computations by `functions.Pipeline`s. The processed data is written to
disk by `io.Writer`s.

The project is structured by dependency injection conventions. The factory and
`Application` are found in `main.py`.
