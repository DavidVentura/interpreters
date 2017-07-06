# Interpreter experiments

## one

Calculator which supports `+`, `-`, `*`, `/` and arbitrary nesting of `()`

The input is resolved first by solving all of the subexpressions
```
2*3*(1+2)*(2*(2*(2*2*(1+1)+1)+1)+1)+1

=> 2*3*3.0*(2*(2*(2*2*(1+1)+1)+1)+1)+1
2*3*3.0*(2*(2*(2*2*(1+1)+1)+1)+1)+1
=> 2*3*3.0*(2*(2*(2*2*2.0+1)+1)+1)+1
2*3*3.0*(2*(2*(2*2*2.0+1)+1)+1)+1
=> 2*3*3.0*(2*(2*9.0+1)+1)+1
2*3*3.0*(2*(2*9.0+1)+1)+1
=> 2*3*3.0*(2*19.0+1)+1
2*3*3.0*(2*19.0+1)+1
=> 2*3*3.0*39.0+1

```

and then solving each operation as decided by their weight:

```
2*3*3.0*39.0+1
=> (2*3), (3*3.0), (3.0*39.0), (39.0+1)
=> pick the first multiplication
=> replace
6*3.0*39.0+1
=> (6*3.0), (3.0*39.0), (39.0+1)
...
```
