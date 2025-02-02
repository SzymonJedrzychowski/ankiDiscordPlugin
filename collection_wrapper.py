from os import path

from anki.collection import Collection
from anki.decks import DeckManager


class CollectionWrapper:
    collection: Collection

    def __init__(self, file_path):
        self.collection = self.__read_collection_file(file_path)
        self.deck = None
        self.card = None

    def generate_welcome_message(self):
        data = self.__get_due()
        return '\n'.join(['Hello, info for today:',
                          f'To Review: {data.review_count}',
                          f'New Cards: {data.new_count}.',
                          'In decks:',
                          self.__get_due_decks_message()])

    def generate_decks_message(self):
        return '\n'.join(['Please select a deck:',
                          self.__get_due_decks_message()])

    def select_deck(self, message_argument):
        try:
            message_argument = int(message_argument)
        except:
            return f'Incorrect parameter: {message_argument}'

        decks = self.__get_decks()
        if len(decks) >= message_argument > 0:
            self.deck = self.collection.decks.get(decks[message_argument - 1].id)
            self.collection.decks.set_current(self.deck.get('id'))
            return f'Selected deck: {self.deck.get('id')} - {self.deck.get('name')}'

        return f'Deck number out of range: {message_argument}'

    def get_card(self):
        if not self.deck:
            return 'No deck selected.'

        self.card = self.collection.sched.getCard()

        if not self.card:
            return 'No cards left.'

        return self.card.note().fields[0]

    def verify_answer(self, answer):
        if not self.card:
            return 'There is no card to respond to.'

        answer = answer.strip()
        expected = self.card.note().fields[1]

        if answer == expected:
            self.collection.sched.answerCard(self.card, 1)
            self.card = None
            return 'Correct'
        else:
            self.collection.sched.answerCard(self.card, 4)
            self.card = None
            return f'Incorrect: {expected}'

    def __read_collection_file(self, file_path):
        if file_path.split('.')[-1] != 'anki2':
            raise ValueError(f'File with incorrect format: {file_path}')
        if not path.exists(file_path):
            raise FileNotFoundError(f'No file at path: {file_path}')

        return Collection(file_path)

    def __get_decks(self):
        return self.collection.decks.all_names_and_ids(skip_empty_default=True)

    def __get_due(self):
        return self.collection.sched.deck_due_tree()

    def __get_due_decks_message(self):
        data = self.__get_due()
        decks_data = [
            f'{index + 1}. {deck.name} - {deck.review_count} reviews and {deck.new_count} new'
            for index, deck in enumerate(data.children)]
        return '\n'.join(decks_data)
