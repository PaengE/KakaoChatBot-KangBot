def remove_tags(list_w_tags):
    return list(map(lambda n : n.get_text(), list_w_tags))