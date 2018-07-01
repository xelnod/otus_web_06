# Otus Web 06 ORM

This is a simple ORM made by S.Zenchenko for «OTUS Web» Lessons while studying

## Getting Started

### Prerequisites

- Python 3.6+
- Virtualenv
- Pip


### Installing

Make a new virtualenv (you may as well not if you know what you're doing)

```
$ virtualenv -p python3 otus_web_06
```

Clone this repo

```
$ git clone https://github.com/xelnod/otus_web_06.git
```


Install requirements

```
$ pip install -r requirements.txt
```
## Using

### Creating tables
```
>>> from example import SimpleExampleModel
>>> ExampleModel.sync_table
``` 
Creates table for model. Will drop the old table if it already exists and create a new one.

### Select
Simple:
```
>>> SimpleExampleModel.select()
```
Will select all fields on all entries. However, you can specify desired fields:
```
>>> SimpleExampleModel.select(fields=('integer_field', 'text_field', limit=2)
```
Simple filtering is also supported:
```
>>> SimpleExampleModel.select(id=1)
>>> SimpleExampleModel.select(text_field='foo', integer_field=4)
```

### Insert
```
>>> SimpleExampleModel.insert(text_field='foo', integer_field=1)
```
Foreign keys are supported:
```
>>> from example import ExampleModelWithFk
>>> ExampleModelWithFk.insert(fk_field=1, text_field='bar')
```
### Update
You must provide primary key value on table in order to perform an update:
```
>>> SimpleExampleModel.update(1, text_field='bar')
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
