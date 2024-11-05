# Evaluate
## Overview
Technical screener puzzle

### Time taken
60 Minutes total

### Method used
I broke down the task into 3 steps, tokenisation, parsing, evaluation

#### Tokenisation
This step has zero error correction and is mainly used to make numbers a single token, 
and remove any unneeded formatting such as white space

#### Parsing
This step validates the grammar and parses it into a highly ordered format for fast and reliable evaluation.
The intermediate format is roughly based on a recursive Polish notation, an example is included below

```python
4 + (12 / (1 * 2))

[
    '+', 
    '4', 
    [
        '/', 
        '12', 
        [
            '*', 
            '1', 
            '2'
        ]
    ]
]
```

#### Evaluation
Once the intermediate format is made it can be quickly recursively evaluated. With two cases, a basis case where it
is a number and another where it is list of 3 items representing an operation.