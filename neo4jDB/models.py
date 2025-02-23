from neomodel import StructuredNode, StringProperty, RelationshipTo

class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    friends = RelationshipTo('Person', 'FRIEND')