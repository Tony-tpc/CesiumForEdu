from neomodel import StructuredNode, StringProperty, RelationshipTo, UniqueProperty

# 测试类
class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    friends = RelationshipTo('Person', 'FRIEND')

# 专题（最高级别）
class Topic(StructuredNode):
    name = StringProperty(unique_index=True)
    first_level_branches = RelationshipTo('FirstLevelBranch', 'HAS_BRANCH')

# 一级分支
class FirstLevelBranch(StructuredNode):
    name = StringProperty(unique_index=True)
    topic = RelationshipTo(Topic, 'BELONGS_TO')
    second_level_branches = RelationshipTo('SecondLevelBranch', 'HAS_BRANCH')

# 二级分支
class SecondLevelBranch(StructuredNode):
    name = StringProperty(unique_index=True)
    first_level_branch = RelationshipTo(FirstLevelBranch, 'BELONGS_TO')
    third_level_branches = RelationshipTo('ThirdLevelBranch', 'HAS_BRANCH')

# 三级分支
class ThirdLevelBranch(StructuredNode):
    name = StringProperty(unique_index=True)
    second_level_branch = RelationshipTo(SecondLevelBranch, 'BELONGS_TO')
    fourth_level_branches = RelationshipTo('FourthLevelBranch', 'APPLICATION')

# 四级分支
class FourthLevelBranch(StructuredNode):
    name = StringProperty(unique_index=True)
    third_level_branch = RelationshipTo('ThirdLevelBranch', 'BELONGS_TO')
