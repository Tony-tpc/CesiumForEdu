from django.http import JsonResponse
from rest_framework.decorators import api_view
from neo4jDB.models import Person, Topic, FirstLevelBranch, SecondLevelBranch, ThirdLevelBranch, FourthLevelBranch

# 测试方法
def get_person(request, name):
    person = Person.nodes.get(name=name)
    return JsonResponse({"name": person.name})


def create_branch(branch_data, parent, level):
    """递归创建分支节点并建立关系"""
    branch_name = branch_data.get("name")

    if level == 1:
        branch, _ = FirstLevelBranch.nodes.get_or_create(name=branch_name)
        parent.first_level_branches.connect(branch)
    elif level == 2:
        branch, _ = SecondLevelBranch.nodes.get_or_create(name=branch_name)
        parent.second_level_branches.connect(branch)
    elif level == 3:
        branch, _ = ThirdLevelBranch.nodes.get_or_create(name=branch_name)
        parent.third_level_branches.connect(branch)
    elif level == 4:
        branch, _ = FourthLevelBranch.nodes.get_or_create(name=branch_name)
        parent.fourth_level_branches.connect(branch)
    else:
        return None  # 超过四级分支则不创建

    # 递归处理子分支
    for child in branch_data.get("children", []):
        create_branch(child, branch, level + 1)

# 创建知识图谱
@api_view(['POST'])
def create_graph(request):
    try:
        data = request.data  # 获取 JSON 数据
        topic_name = data.get("topic_name")
        branches = data.get("branches", [])

        if not topic_name:
            return JsonResponse({"error": "专题名称不能为空"}, status=400)

        # 创建 Topic 节点
        topic, _ = Topic.nodes.get_or_create(name=topic_name)

        # 递归创建分支
        for branch in branches:
            create_branch(branch, topic, level=1)

        return JsonResponse({"message": "知识图谱创建成功", "topic": topic_name}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# 递归序列化分支节点
def serialize_branch(branch):
    data = {
        "name": branch.name,
        "children": []
    }
    if hasattr(branch, 'first_level_branches'):  # 处理 Topic -> FirstLevelBranch
        data["children"] = [serialize_branch(child) for child in branch.first_level_branches.all()]
    elif hasattr(branch, 'second_level_branches'):  # 处理 FirstLevelBranch -> SecondLevelBranch
        data["children"] = [serialize_branch(child) for child in branch.second_level_branches.all()]
    elif hasattr(branch, 'third_level_branches'):  # 处理 SecondLevelBranch -> ThirdLevelBranch
        data["children"] = [serialize_branch(child) for child in branch.third_level_branches.all()]
    elif hasattr(branch, 'fourth_level_branches'):  # 处理 ThirdLevelBranch -> FourthLevelBranch
        data["children"] = [serialize_branch(child) for child in branch.fourth_level_branches.all()]

    return data

@api_view(['POST'])
def get_graph(request):
    topic_name = request.data.get("topic_name")
    try:
        topic = Topic.nodes.get(name=topic_name)
    except Topic.DoesNotExist:
        return JsonResponse({"error": "标题不存在"}, status=404)

    # 递归获取完整的知识图谱
    graph_data = serialize_branch(topic)

    return JsonResponse({"graph": graph_data}, json_dumps_params={'ensure_ascii': False}, safe=False)
