from typing import Dict, Optional

from django import template

register = template.Library()


@register.simple_tag
def tabindex(match_row: int, set_id: str, offset: int):
    return (match_row-1) * 12 + int(set_id) * 4 + offset


@register.simple_tag
def get_score(set_dict: Dict[int, Dict[int, Dict[str, Optional[int]]]], match_id: int, set_id: str, score_type: str):
    value = set_dict[match_id][int(set_id)].get(score_type)
    return str(value) if value is not None else ""
