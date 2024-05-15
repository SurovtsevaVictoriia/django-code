from .models import Questions, Themes
# import sys

# sys.setrecursionlimit(25)


def get_subthemes(theme_id: int) -> list[int]:
    """return list of all-level child themes

    Args:
        theme_id (int): id of the given theme

    Returns:
        list[int]: list of ids of children in order of discovery
    """
    roots = []
    children_ids = []

    def get_children(theme_ids):

        print('before before cycle', id(roots),
              id(children_ids), id(theme_ids))
        roots.extend(children_ids)
        children_ids.clear()
        # print('before cycle', roots, children_ids, theme_ids)
        try:
            if type(theme_ids) == int:
                child_themes = Themes.objects.filter(parent_id=theme_ids)
                for child_theme in child_themes:
                    children_ids.append(child_theme.theme_id)
            else:
                if len(theme_ids) >= len(Themes.objects.all()) or len(theme_ids) == 0:
                    print('length exceeded:', theme_ids)
                    return

                for theme_id in theme_ids:
                    child_themes = Themes.objects.filter(parent_id=theme_id)
                    for child_theme in child_themes:
                        children_ids.append(child_theme.theme_id)

            # print('after cycle', roots, children_ids, theme_ids)

        except Exception as e:
            print(e.args, "get_children not getting children")

        get_children(children_ids.copy())

    get_children(theme_id)
    return roots


def get_themes_as_tree() -> list:
    """returns entire tree of theme ids as nested list

    Returns:
        list: nested list such as [0, [1, [3]], [2]]
    """

    roots = [0]
    k = 0

    def get_children(theme_ids: list, i):
        i = i+1

        print(i, 'roots', roots, 'theme_ids', theme_ids)
        try:
            if type(theme_ids[0]) == int:
                print('in int if', theme_ids[0])
                child_themes = Themes.objects.filter(parent_id=theme_ids[0])
                for child_theme in child_themes:
                    theme_ids.append([child_theme.theme_id])
                get_children(theme_ids[1:], i)
                # children_ids.append([child_theme.theme_id])
            else:
                for idx, theme_id in enumerate(theme_ids):
                    print('in list if, idx = ', idx, 'theme_id ', theme_id)
                    child_themes = Themes.objects.filter(
                        parent_id=theme_ids[idx][0])
                    for child_theme in child_themes:
                        theme_ids[idx].append([child_theme.theme_id])
                    get_children(theme_ids[idx][1:], i)
                    # children_ids.append(child_theme.theme_id)

        except Exception as e:
            print(e.args, "get_children not getting children")

    get_children(roots, k)
    return roots


def get_questions(theme_id: int) -> list[dict]:
    """returns questions on given theme and all the subthemes
    Args:
        theme_id (int): given theme id
    Returns:
        list[dict]: [{'question_id': ..., 'question': ..., 'answer': ..., 'theme_id': ...}]
    """
    theme_ids = [theme_id]
    theme_ids.extend(get_subthemes(theme_id))
    questions = []
    for t_id in theme_ids:
        theme_qs = Questions.objects.filter(theme_id=t_id)
        for theme_q in theme_qs:
            questions.append(theme_q.get_as_dict())

    return questions
