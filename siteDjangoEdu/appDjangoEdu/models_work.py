"""This module connects web application with database

"""
import json
from .models import Questions, Themes


def get_theme_dicts_as_json_string():
    """
    returns entire tree of themes as json string

    {"root":
        [
            {'theme' :{'theme_id': ..., 'name': ..., 'parent_id': ..., 'q_count': ...}, 
             'nested':[{'theme': ... , 'nested': ... }, 
                       {'theme': ... , 'nested': ... }]
            }, 
            {...}
        ]    
    }
    Returns:
        list[list[dict]]: nested list of dicts
    """

    roots = {'nested': []}
    all_theme = Themes.objects.filter(theme_id=0)[0]
    t_dict = all_theme.get_as_dict()
    q_count = all_theme.get_q_count()
    t_dict['q_count'] = q_count
    t_dict['parent_id'] = -1

    roots['theme'] = t_dict
    k = 0

    def get_children(theme_dicts: list[dict], i):
        i = i + 1
        # print(i, 'roots', roots, '\n theme_dicts', theme_dicts)
        try:
            if i == 1:
                # print('---\nin int if', theme_dicts)
                child_themes = Themes.objects.filter(parent_id=0)
                for child_theme in child_themes:
                    q_count = child_theme.get_q_count()
                    t_dict = child_theme.get_as_dict()
                    t_dict['q_count'] = q_count

                    theme_dicts['nested'].append({
                        'theme': t_dict,
                        'nested': []
                    })
                get_children(theme_dicts["nested"], i)

            else:
                try:
                    for theme_dict in theme_dicts:
                        # print('---\nin list if, idx = ', idx, '\n theme_dict ', theme_dict)
                        child_themes = Themes.objects.filter(
                            parent_id=theme_dict['theme']['theme_id'])

                        for child_theme in child_themes:
                            q_count = child_theme.get_q_count()
                            t_dict = child_theme.get_as_dict()
                            t_dict['q_count'] = q_count

                            theme_dict['nested'].append({
                                'theme': t_dict,
                                'nested': []
                            })

                        get_children(theme_dict['nested'], i)
                except Exception as e:
                    print(e.args, "error in list if")

        except Exception as e:
            print(e.args, "get_children not getting children")

    get_children(roots, k)
    json_data = json.dumps(roots, indent=2, ensure_ascii=False,)
    return json_data


def get_questions(theme_id: int) -> list[dict]:
    """returns questions on given theme 
    Args:
        theme_id (int): given theme id
    Returns:
        list[dict]: [{'question_id': ..., 'question': ..., 'answer': ..., 'theme_id': ...}]
    """
    questions = []
    theme_qs = Questions.objects.filter(theme_id=theme_id)
    for theme_q in theme_qs:
        theme_dict = theme_q.get_as_dict()
        theme_dict["theme_name"] = Themes.objects.get(theme_id=theme_id).name
        questions.append(theme_dict)

    return questions


def get_theme_by_id(idx: int) -> dict:
    """returns theme as dictionary

    Args:
        idx (int): index of theme

    Returns:
        dict: {"theme_id": ..., "name": ..., "parent_id": ...}
    """
    theme = Themes.objects.get(theme_id=idx)
    theme_dict = theme.get_as_dict()
    return theme_dict


def write_new_question(theme_id: int, new_question: str, new_answer: str) -> None:
    """add new question entry to the database
    Args:
        theme_id (int): 
        new_question (str): 
        new_answer (str): 
    """

    q = Questions(question=new_question, answer=new_answer, theme_id=theme_id)
    q.save()
    print(q)
