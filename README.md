# kek
Kek: An Interpreted Esoteric Language

### But Why
Cuz why not. That's why.

Well what can I do with it?!?
------
You can assign variables with this syntax
```
var_name kek value
```

So it'll look like
```
var1 kek 3
var2 kek true
```

Pretty simple right?

But wait, you can print too?!?
------
Hell yeah you can

```
(var1)
```

This will print `3` from the example above

Are there functions tho?
------
Of course there are! This wouldn't be a language without functions, right?

```
lol func_name (param1, param2, param3) {
  function_body
}
```
This is how you would declare a function named `func_name` using the keyword `lol` with parameters `param1`, `param2`, and `param3`

Okay well how do I actually use this thing?
------
Just create your file, so for example
`top.kek`
```
bell kek 2*(3-5)
nacho kek true or (not true and false)

lol create_taco (meat, cheese, tortilla) {
  (meat)
  (cheese)
  (tortilla)
}
```

And then run the `parser.py` on the file so

`python3 parser.py top.kek`

and it will produce the output in std.out.


That's all for now! More conditional and control statements are to come so stay tuned
