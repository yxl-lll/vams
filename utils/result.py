from fastapi.encoders import jsonable_encoder
from datetime import datetime

# 添加自定义编码器
custom_encoder = {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}

class Result:
    """ 结果数据结构 """
    @staticmethod
    def success(*, code: int = 0, data: None, total: int = 0, msg: str = "ok"):
        """ 成功响应数据结构 """
        return {
            "code": code,
            "data": jsonable_encoder(data, custom_encoder=custom_encoder),
            "total": total,
            "count": total,
            "msg": msg,
            "success": True
        }
    @staticmethod
    def encoder(data: None):
        return jsonable_encoder(data, custom_encoder=custom_encoder)
    @staticmethod
    def fail(*, code: int = 1, data: None, msg: str = "err"):
        """ 失败响应数据结构 """
        return {
            "code": code,
            "data": jsonable_encoder(data),
            "msg": msg,
            "success": False
        }
    @staticmethod
    def generate_tree_menu(menus, jj: bool=False):
        
        """ 生成树形菜单 """
        menu_list = []
        for menu in menus:
            menu["title"] = menu['menu_name']
            menu["parentId"] = menu['p_id']
            menu["nodeId"] = menu['id']
            menu["checkArr"] = "{\"type\": \"0\", \"checked\": \"0\"}"
            if jj == True:
                del menu['updated_at']
                del menu['created_at']
                del menu['menu_status']
                menu_list.append(menu)
            else:
                menu_list.append(menu)
                
        menu_dict = {}
        for menu in menu_list:
            menu_dict[menu["id"]] = menu
            menu_dict[menu["id"]]["children"] = []

        tree_menu = []
        for menu in menu_list:
            if menu["type"] == 3 and jj == True:
                continue
            if menu["p_id"] == '0':
                menu["isParent"] = True
                tree_menu.append(menu)
            else:
                menu_dict[menu["p_id"]]["isParent"] = True
                menu_dict[menu["p_id"]]["children"].append(menu)  # type: ignore
        return tree_menu
