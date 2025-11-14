from datetime import datetime, date
from typing import Any
from pydantic import BaseModel
from sqlalchemy import Table

class FixQuery:
    @staticmethod
    def query(model: BaseModel, val: Any, instance: Table, total_query: Any, query: Any):
        d_val = val.dict()
        for field in model.__fields__:
            if d_val[field] is not None and d_val[field] != '':
                field_val = d_val[field]
                if isinstance(field_val, int):
                    total_query = total_query.where(instance.c[field] == field_val)
                    query = query.where(instance.c[field] == field_val)
                elif isinstance(field_val, str):
                    fields = field_val.split('#')
                    if len(fields) == 1:
                        total_query = total_query.where(instance.c[field] == field_val)
                        query = query.where(instance.c[field] == field_val)
                    else:
                        match fields[1]:
                            case "like":
                                total_query = total_query.where(instance.c[field].like(f"%{fields[0]}%"))
                                query = query.where(instance.c[field].like(f"%{fields[0]}%"))
                            case "in":
                                in_val = fields[0].split(",")
                                total_query = total_query.where(instance.c[field].in_(in_val))
                                query = query.where(instance.c[field].in_(in_val))
                            case "bt":
                                between_val = fields[0].split(",")
                                total_query = total_query.where(instance.c[field].between(between_val[0],between_val[1]))
                                query = query.where(instance.c[field].between(between_val[0],between_val[1]))

                elif isinstance(field_val, str):
                    total_query = total_query.where(instance.c[field] == field_val)
                    query = query.where(instance.c[field] == field_val)
                elif isinstance(field_val, date):
                    total_query = total_query.where(instance.c[field] == field_val)
                    query = query.where(instance.c[field] == field_val)
                elif isinstance(field_val, datetime):
                    pass
        return total_query, query
    