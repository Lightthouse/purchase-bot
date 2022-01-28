import emoji


class StringFormat:

    @staticmethod
    def purchases_list(purchases):
        if not purchases:
            return emoji.emojize('Список пуст :sad_but_relieved_face:')

        purchases = purchases if isinstance(purchases, list) else [purchases]

        result_string = 'ID СТОИМОСТЬ НАЗВАНИЕ\n'
        purchases = [p[:3] for p in purchases]
        for p in purchases:
            result_string += f'{p}\n'
        return result_string

    @staticmethod
    def categories_list(categories):
        if not categories:
            return emoji.emojize('Список пуст :sad_but_relieved_face:')

        categories = categories if isinstance(categories, list) else [categories]

        result_string = 'КОД НАЗВАНИЕ ПСЕВДОНИМЫ\n'
        for c in categories:
            result_string += f'{c}\n'
        return result_string

