from .models import Questions, Themes


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
        # print('before before cycle', roots, children_ids, theme_ids)
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



