from .models import Questions, Themes
import json
# import sys

# sys.setrecursionlimit(25)


def get_theme_dicts_as_tree() -> list[list[dict]]:
    """
    returns entire tree of themes as nested list of dicts
    dict:{'theme_id': ..., 'name': ..., 'parent_id': ...}
    Returns:
        list[list[dict]]: nested list of dicts
    """
    roots = []
    k = 0

    def get_children(theme_dicts: list, i):
        i = i+1

        # print(i, 'roots', roots, 'theme_ids', theme_dicts)
        try:
            if len(theme_dicts) == 0 and i == 1:
                # print('in int if', theme_dicts)
                child_themes = Themes.objects.filter(parent_id=0)
                for child_theme in child_themes:
                    theme_dicts.append([child_theme.get_as_dict()])
                get_children(theme_dicts, i)
                # children_ids.append([child_theme.theme_id])
            else:
                for idx, theme_dict in enumerate(theme_dicts):
                    # print('in list if, idx = ', idx, 'theme_dict ', theme_dict)
                    child_themes = Themes.objects.filter(
                        parent_id=theme_dicts[idx][0]['theme_id'])

                    for child_theme in child_themes:
                        theme_dicts[idx].append([child_theme.get_as_dict()])
                    get_children(theme_dicts[idx][1:], i)
                    # children_ids.append(child_theme.theme_id)

        except Exception as e:
            print(e.args, "get_children not getting children")

    get_children(roots, k)
    return roots


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


def get_all_theme_ids():
    ids = []
    themes = Themes.objects.all()
    for theme in themes:
        ids.append(theme.theme_id)
    return ids


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
