from pydantic import BaseModel

""" 菜单与角色对应关系表 - 模块模型定义 """


class MenuRoleBody(BaseModel):
    menu_id: str
    role_id: str
