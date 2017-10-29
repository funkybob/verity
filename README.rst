Verity
======

Verity provides Type and field as ways to build classes which will cast and
validate your incoming data.

Simply declare a sub-class of Type, with fields. Each field takes a callable,
which is used to validate/cast the incoming data of its name. It can optionally
also take a default value.

QuickStart
----------

.. code-block:: python

   from datetime import datetime
   from verity import Type, field

   def parse_date(value):
       return datetime.strptime(value, '%Y-%m-%d').date()

   class Person(Type):
       name = field(str)
       birthdate = field(parse_date)


.. code-block:: python

   >>> data = {'name': 'Bob', 'birthdate': '1980-12-21'}
   >>> person = Person(data)
   >>> person.birthdate
   datetime.date(1980, 12, 21)

Types are nestable:

.. code-block:: python

   class Food(Type):
       name = field(str)
       energy = field(float, default=0.0)


   class Person(Type):
       name = field(str)
       birthdate = field(parse_date)
       favourite_food = field(Food)


.. code-block:: python

   >>> data = {'name': 'Bob', 'birthdate': '1980-12-21', 'favourite_food': {'name': 'Pizza'}}
   >>> person = Person(**data)
   >>> person.favourite_food.name
   'Pizza'


Types can JSON-ify themselves

.. code-block:: python

   >>> person.__json__()
   {'name': 'Bob', 'birthdate': datetime.date(1980, 12, 21), 'favourite_food': <Food>}

Though it's not recurive.

However, it can cooperate with ``json_default``:

.. code-block:: python

   >>> from verity import json
   >>> json.dumps(person)
   '{"birthdate": "1980-12-21", "favourite_food": {"energy": 0.0, "name": "Pizza"}, "name": "Bob"}'

